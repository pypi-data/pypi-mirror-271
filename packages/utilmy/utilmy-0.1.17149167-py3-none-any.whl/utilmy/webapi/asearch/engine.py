# -*- coding: utf-8 -*-
"""
    #### Install
        pip install -r py39.txt
        pip install fastembed==0.2.6 loguru --no-deps


    #### ENV variables
        export HF=
        export
        export torch_device='cpu'
        #### Test

            python  engine.py test_qdrant_dense
            python  engine.py test_qdrant_sparse
            python engine.py test_tantivy




    #### Benchmarks:
            sudo docker run -d -p 6333:6333     -v ~/.watchtower/qdrant_storage:/qdrant/storage:z     qdrant/qdrant
            alias py2="python engine.py "

            py2 bench_v1_create_indexes --dirdata_root ztmp/bench/
            py2 bench_v1_run  --dirout ztmp/bench/   --topk 5


            ### Bench
            tantivy : v1  6ms
            Sparse :      23ms
            Dense:        30 ms
            
            ag_news index timings:
            records: 127600
            dense stransformers vectors: 9m28s
            dense fastembed vectors:
            sparse vectors: 9819/12760


    #### Dataset
        https://www.kaggle.com/datasets/gowrishankarp/newspaper-text-summarization-cnn-dailymail


        https://www.kaggle.com/datasets/gowrishankarp/newspaper-text-summarization-cnn-dailymail

        https://zenn.dev/kun432/scraps/1356729a3608d6


        https://huggingface.co/datasets/big_patent


        https://huggingface.co/datasets/ag_news


    #### Flow
        HFace Or Kaggle --> dataset in RAM--> parquet (ie same columns)  -->  parquet new columns (final)


        Custom per text data
        title  :   text
        body   :    text
        cat1   :    string   fiction / sport /  politics
        cat2   :    string     important / no-important
        cat3   :    string
        cat4   :    string
        cat5   :    string
        dt_ymd :    int     20240311


"""
import warnings

warnings.filterwarnings("ignore")
import os, pathlib, uuid, time, traceback
from typing import Any, Callable, Dict, List, Optional, Sequence, Union
from box import Box  ## use dot notation as pseudo class

import pandas as pd, numpy as np, torch
import tantivy

from qdrant_client import QdrantClient
from qdrant_client import models
from qdrant_client.http.models import PointStruct

from fastembed import TextEmbedding
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForMaskedLM
from ranx import Qrels, Run, fuse

import datasets

from utilmy import pd_read_file, os_makedirs, pd_to_file, date_now, glob_glob
from utilmy import log, log2


######################################################################################
def test_all():
    ### python engine2.py test_all
    test_qdrant_dense()
    test_qdrant_sparse()
    test_tantivy()
    test_fusion_search()


def test_qdrant_dense(nrows=20):
    """
    python engine.py test_qdrant_dense_create_index    
    """
    dirtmp = "ztmp/df_test.parquet"
    test_df = pd_fake_data(nrows=nrows, dirout=dirtmp, overwrite=False)

    model_type = "stransformers"
    model_id = "sentence-transformers/all-MiniLM-L6-v2"
    server_url = ":memory:"  ### "http://localhost:6333"
    collection_name = "my-documents"

    client = QdrantClient(server_url)

    qdrant_dense_create_index(
        dirin=dirtmp,
        server_url=server_url,
        collection_name=collection_name,
        coltext="body",
        model_id=model_id,
        model_type=model_type,
        client=client
    )
    model = EmbeddingModel(model_id, model_type)

    # pick random query from the test dataframe
    query = test_df.sample(1)["body"].values[0]
    results = qdrant_dense_search(
        query,
        server_url=server_url,
        collection_name=collection_name,
        model=model,
        client=client
        # category_filter={"categories": "Fiction"},
    )
    results = [
        ((scored_point.payload), scored_point.score)
        for scored_point in results
        if scored_point.score > 0
    ]
    log(f"len(results):{len(results)}")
    assert len(results) > 0


def test_qdrant_sparse(nrows=30):
    """test function for sparse qdrant indexing"""
    dirtmp = "ztmp/df_test.parquet"
    test_df = pd_fake_data(nrows=nrows, dirout=dirtmp, overwrite=False)

    model_id = "naver/efficient-splade-VI-BT-large-doc"
    model_type = "stransformers"
    server_url = ":memory:"  ### "http://localhost:6333"
    collection_name = "my-documents"

    client = QdrantClient(server_url)

    qdrant_sparse_create_index(
        dirin=dirtmp,
        collection_name="my-sparse-documents",
        model_id=model_id,
        client=client
    )
    # pick random query from the test dataframe
    query = test_df.sample(1)["body"].values[0]

    model = EmbeddingModelSparse(model_id)
    results = qdrant_sparse_search(
        query,
        # category_filter={"categories": "Fiction"},
        collection_name="my-sparse-documents",
        model=model,
        client=client
    )

    results = [
        ((scored_point.payload), scored_point.score)
        for scored_point in results
        if scored_point.score > 0
    ]
    # print(results)
    log(f"len(results):{len(results)}")
    assert len(results) > 0


def test_tantivy(nrows=50):
    """test function for tantivy indexing"""
    dirtmp = "ztmp/df_test.parquet"
    dirindex = "ztmp/tantivy_index"
    if not os.path.exists(dirtmp):
        test_df = pd_fake_data(nrows=nrows, dirout=dirtmp, overwrite=False)
        pd_to_file(test_df, dirtmp)
    else:
        test_df = pd_read_file(dirtmp)

    tantivy_index_documents(
        dirin=dirtmp, datapath=dirindex, kbatch=10, colsused=["title", "body"]
    )
    # pick random query from the test dataframe
    query = test_df.sample(1)["body"].values[0]

    query = query.replace("\n", " ")
    results = tantivy_search(query=query, datapath=dirindex)
    log(f"len(results):{len(results)}")
    assert len(results) > 0


def test_fusion_search():
    """test function for fusion search"""
    # get results from qdrant sparse search
    dirtmp = "ztmp/df_test.parquet"
    test_df = pd_read_file(dirtmp)
    # pick random query from the test dataframe
    query = test_df.sample(1)["body"].values[0]
    query = query.replace("\n", " ")

    server_url = ":memory:"
    # index in memory data for later retrieval
    client = QdrantClient(server_url)
    qdrant_sparse_create_index(
        dirin=dirtmp,
        client=client
    )
    v1_results = qdrant_sparse_search(query, client=client)
    v1 = fusion_postprocess_qdrant(v1_results)
    # collect ids from  results
    v1_ids = list(v1.keys())

    # get results from tantivy search
    v2_results = tantivy_search(query=query)
    v2 = fusion_postprocess_tantivy(v2_results)
    # collect ids from  results
    v2_ids = list(v2.keys())

    fusion_results = fusion_search(query=query, method="rrf", client=client)

    search_ids = set(v1_ids).union(v2_ids)
    fusion_ids = set(fusion_results["q1"].keys())
    # check if  ids from  two search results are  same as ids from fusion search
    # log(f"{search_ids.difference(fusion_ids)}")
    assert search_ids.difference(fusion_ids) == set()


def test_hf_dataset_to_parquet():
    """test function for converting Hugging Face datasets to Parquet files"""
    name = "ag_news"
    splits = ["train", "test"]
    dataset_hf_to_parquet(name, dirout="hf_datasets", splits=splits)
    # read the parquet files
    for split in splits:
        assert os.path.exists(f"hf_datasets/{name}_{split}.parquet")
        # pd = pd_read_file(f"hf_datasets/{dataset_name}_{split}.parquet")
        # print(pd.columns)


#####################################################################################


#####################################################################################
########## Dense Vector creation
class EmbeddingModel:
    def __init__(self, model_id, model_type, device: str = "", embed_size: int = 128):
        self.model_id = model_id
        self.model_type = model_type

        self.device = torch_getdevice(device)

        if model_type == "stransformers":
            self.model = SentenceTransformer(model_id, device=self.device)
            self.model_size = self.model.get_sentence_embedding_dimension()

        elif model_type == "fastembed":
            self.model = TextEmbedding(model_name=model_id, max_length=embed_size)
            self.model_size = self.model.get_embedding_size()

        else:
            raise ValueError(f"Invalid model type: {model_type}")

    def embed(self, texts: List):
        if self.model_type == "stransformers":
            vectors = list(self.model.encode(texts))
        elif self.model_type == "fastembed":
            vectors = list(self.model.embed(texts))
        return vectors


class EmbeddingModelSparse:
    def __init__(self, model_id: str = "", max_length: int = 512):
        """ """
        # Initialize tokenizer and model
        self.device = torch_getdevice()
        self.max_length = max_length
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForMaskedLM.from_pretrained(
            model_id, device_map=self.device
        )

    def embed(self, texts):
        # Tokenize all texts
        if isinstance(texts, np.ndarray):
            # convert to list
            texts = texts.tolist()
        tokens_batch = self.tokenizer(
            texts,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=self.max_length,
        )
        # Forward pass through  model
        tokens_batch.to(device=self.device)
        with torch.no_grad():
            output = self.model(**tokens_batch)

        # Extract logits and attention mask
        logits = output.logits
        attention_mask = tokens_batch["attention_mask"]

        # ReLU and weighting
        relu_log = torch.log(1 + torch.relu(logits))
        weighted_log = relu_log * attention_mask.unsqueeze(-1)

        # Compute max values
        max_vals, _ = torch.max(weighted_log, dim=1)
        # log(f"max_vals.shape: {max_vals.shape}")

        # for each tensor in  batch, get  indices of  non-zero elements
        indices_list = [torch.nonzero(tensor, as_tuple=False) for tensor in max_vals]
        indices_list = [
            indices.cpu().numpy().flatten().tolist() for indices in indices_list
        ]
        # for each tensor in  batch, get  values of  non-zero elements
        values = [
            max_vals[i][indices].cpu().numpy().tolist()
            for i, indices in enumerate(indices_list)
        ]

        return list(zip(indices_list, values))

    def decode_embedding(self, cols: list, weights) -> dict:
        """Decodes the embedding from indices and values."""
        # Map indices to tokens and create a dictionary
        idx2token = {idx: token for token, idx in self.tokenizer.get_vocab().items()}
        token_weight_dict = {
            idx2token[idx]: round(weight, 2) for idx, weight in zip(cols, weights)
        }

        # Sort  dictionary by weights in descending order
        sorted_token_weight_dict = {
            k: v
            for k, v in sorted(
                token_weight_dict.items(), key=lambda item: item[1], reverse=True
            )
        }

        return sorted_token_weight_dict


#####################################################################################
########## Qdrant Dense Vector Indexing
def qdrant_collection_exists(qclient, collection_name):
    collections = qclient.get_collections()
    collections = {coll.name for coll in collections.collections}
    return collection_name in collections


def qdrant_dense_create_collection(
        qclient, collection_name="documents", size: int = None
):
    """
    Create a collection in qdrant
    :param qclient: qdrant client
    :param collection_name: name of  collection
    :param size: size of  vector
    :return: collection_name
    """
    if not qdrant_collection_exists(qclient, collection_name):
        qclient.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=size, distance=models.Distance.COSINE
            ),
        )
        log(f"created collection:{collection_name}")
    return collection_name


def qdrant_dense_index_documents(
        qclient,
        collection_name: str,
        df: pd.DataFrame,
        colscat: List = None,  ## list of categories field
) -> None:
    """Indexes documents from a pandas DataFrame into a qdrant collection.
    Args:
        qclient:  qdrant client.
        collection_name:  name of  collection.
        df:  DataFrame containing  documents.
        colscat: list of fields to be indexed

    """
    colscat = (
        [ci for ci in df.columns if ci not in ["vector"]]
        if colscat is None
        else colscat
    )

    assert df[["id", "vector"]].shape
    # log(df)

    # Convert documents to points for insertion into qdrant.
    points = [
        PointStruct(
            id=row["id"],  # Use existing id if available, else generate new one.
            vector=row["vector"].tolist(),  # Numpy ---> List, Vector of  document.
            payload={ci: row[ci] for ci in colscat},  ### Category filtering values
        )
        for i, row in df.iterrows()
    ]

    vector_size = len(points[0].vector)  # Get  size of  vectors.

    # Create collection if not existing.
    qdrant_dense_create_collection(
        qclient, collection_name=collection_name, size=vector_size)

    # Index documents.
    qclient.upsert(collection_name=collection_name, points=points)
    log("qdrant upsert done: ", collection_name, qclient.count(collection_name), )


def qdrant_dense_create_index(
        dirin: str,
        server_url: str = ":memory:",
        collection_name: str = "my-documents",
        colscat: List = None,  ## list of categories field
        coltext: str = "body",
        model_id=None,
        model_type=None,
        batch_size=100,
        client=None
) -> None:
    """Create a qdrant index from a parquet file.

    dirin: str: path to  parquet file
    server_url: str: url path to  qdrant server
    coltext: str: column name of  text column
    model_id: str: name of  embedding model to use
    model_type: str: type of  embedding model
    batch_size: int: batch size for embedding vectors
    (ID_k, text_k)

    """
    # df = pd_read_file(path_glob=dirin, verbose=True)
    flist = glob_glob(dirin)
    log("Nfiles: ", len(flist))

    ##### Load model
    model = EmbeddingModel(model_id, model_type)
    client = QdrantClient(server_url) if client is None else client
    qdrant_dense_create_collection(client, collection_name, size=model.model_size)
    for i, fi in enumerate(flist):
        dfi = pd_read_file(fi)

        ### Create embedding vectors batchwise
        kmax = int(len(dfi) // batch_size) + 1
        for k in range(0, kmax):
            dfk = dfi.iloc[k * batch_size: (k + 1) * batch_size, :]
            if len(dfk) <= 0:
                break
            # get document vectors
            dfk["vector"] = model.embed(dfk[coltext].values)

            # insert documents into qdrant
            assert dfk[["id", "vector"]].shape
            qdrant_dense_index_documents(
                client, collection_name, colscat=colscat, df=dfk
            )


def qdrant_dense_search(query,
                        topk: int = 20,
                        category_filter: dict = None,
                        server_url: str = ":memory:",
                        collection_name: str = "my-documents",
                        model: EmbeddingModel = None,
                        client=None,
                        ) -> List:
    """
    Search a qdrant index
    query: str: query to search
    server_url: str: url path to  qdrant server
    collection_name: str: name of  collection to search
    model_id: str: name of  embedding model to use

    Schema
         title, body ,  cat1, cat2, cat2
          ("cat2name" : "myval"  )

    """
    client = QdrantClient(server_url) if client is None else client
    # model = EmbeddingModel(model_id, model_type)
    query_vector: list = model.embed([query])
    query_filter = qdrant_query_createfilter(category_filter)

    # log(client.count(collection_name))
    result: list = client.search(
        collection_name=collection_name,
        query_vector=query_vector[0],
        query_filter=query_filter,
        limit=topk,
    )
    # log([scored_point.payload["categories"] for scored_point in search_result])
    # log(f"#search_results:{len(search_result)}")
    return result


def qdrant_query_createfilter(
        category_filter: Dict = None,
) -> Union[None, models.Filter]:
    """Create a query filter for Qdrant based on  given category filter.
    Parameters:
        category_filter (Dict[str, Any], optional): A dictionary representing  category filter. Defaults to None.

    Returns:
        Union[None, models.Filter]:  query filter created based on  category filter, or None if  category filter is None.
    """
    query_filter = None
    if category_filter:
        catfilter = []
        for catname, catval in category_filter.items():
            xi = models.FieldCondition(
                key=catname, match=models.MatchValue(value=catval)
            )
            catfilter.append(xi)
        query_filter = models.Filter(should=catfilter)
    return query_filter


####################################################################################
######### Qdrant Sparse Vector Engine :
def qdrant_sparse_create_collection(
        qclient, collection_name="documents", size: int = None
):
    """Create a collection in qdrant
    :param qclient: qdrant client
    :param collection_name: name of  collection
    :param size: size of  vector
    :return: collection_name
    """
    if not qdrant_collection_exists(qclient, collection_name):
        vectors_cfg = {}  # left blank in case of sparse indexing
        sparse_vectors_cfg = {
            "text": models.SparseVectorParams(
                index=models.SparseIndexParams(
                    on_disk=True,
                )
            )
        }
        qclient.create_collection(
            collection_name=collection_name,
            vectors_config=vectors_cfg,
            sparse_vectors_config=sparse_vectors_cfg,
        )
        log(f"created sparse collection:{collection_name}")
    return collection_name


def qdrant_sparse_index_documents(
        qclient, collection_name, df: pd.DataFrame, colscat: list = None
):
    # covert documents to points for insertion into qdrant

    colscat = (
        [ci for ci in df.columns if ci not in ["vector"]]
        if colscat is None
        else colscat
    )
    points = [
        models.PointStruct(
            id=doc["id"],
            payload={key: doc[key] for key in colscat},
            # Add any additional payload if necessary
            vector={
                "text": models.SparseVector(indices=doc.vector[0], values=doc.vector[1])
            },
        )
        for i, doc in df.iterrows()
    ]

    # Create collection if not existing
    # qdrant_sparse_create_collection(qclient, collection_name=collection_name)
    # Index documents
    try:
        qclient.upsert(collection_name=collection_name, points=points)
    except Exception as err:
        print(traceback.format_exc())


def qdrant_sparse_create_index(
        dirin: str,
        server_url: str = ":memory:",
        collection_name: str = "my-sparse-documents",
        colscat: list = None,
        coltext: str = "body",
        model_id: str = "naver/efficient-splade-VI-BT-large-doc",
        batch_size: int = 5,
        client=None,
) -> None:
    """
    Create a qdrant sparse index from a parquet file
    dirin: str: path to  parquet file
    server_url: str: url path to  qdrant server
    coltext: str: column name of  text column
    model_id: str: name of  sparse embedding model to use
    """
    flist = glob_glob(dirin)
    log("Nfiles: ", len(flist))

    ##### Load model
    model = EmbeddingModelSparse(model_id)
    client = QdrantClient(server_url) if client is None else client
    qdrant_sparse_create_collection(client, collection_name)
    for i, fi in enumerate(flist):
        dfi = pd_read_file(fi)
        ### Create embedding vectors batchwise
        kmax = int(len(dfi) // batch_size) + 1
        for k in range(0, kmax):
            dfk = dfi.iloc[k * batch_size: (k + 1) * batch_size, :]
            if len(dfk) <= 0:
                break
            # get document vectors
            dfk["vector"] = model.embed(dfk[coltext].values)

            # insert documents into qdrant
            assert dfk[["id", "vector"]].shape
            qdrant_sparse_index_documents(
                client, collection_name, colscat=colscat, df=dfk
            )


def qdrant_sparse_search(query: str,
                         category_filter: dict = None,
                         server_url: str = ":memory:",
                         collection_name: str = "my-sparse-documents",
                         model: EmbeddingModelSparse = None,
                         model_id_default: str = "naver/efficient-splade-VI-BT-large-doc",
                         topk: int = 10,
                         client=None
                         ) -> List:
    """Search a qdrant index
    query: str: query to search
    server_url: str: url path to  qdrant server
    collection_name: str: name of  collection to search
    model_id: str: name of  embedding model to use
    """
    client = QdrantClient(server_url) if client is None else client
    model = EmbeddingModelSparse(model_id_default) if model is None else model
    result = model.embed([query])
    query_indices, query_values = result[0]

    query_dict = model.decode_embedding(query_indices, query_values)
    # log(f"query_dict:{query_dict}")

    query_filter = qdrant_query_createfilter(category_filter)

    query_vector = models.NamedSparseVector(name="text",
                                            vector=models.SparseVector(indices=query_indices, values=query_values, ),
                                            )

    # Searching for similar documents
    search_results: List = client.search(collection_name=collection_name,
                                         query_vector=query_vector,
                                         # query_filter=query_filter,
                                         with_vectors=True,
                                         limit=topk,
                                         )
    return search_results


##############################################################################
##  Tantivy Engine
def tantivy_index_get(datapath: str = "./ztmp/tantivy_index", schema_name: str = None):
    if schema_name is None:
        schema = tantivy_schema_get_default()
    else:
        ### Load  function to create  schema only by name string.
        from utilmy import load_function_uri

        schema_builder_fun = load_function_uri(schema_name)
        schema = schema_builder_fun()

    # create datastore
    os_makedirs(datapath)

    index_disk = tantivy.Index(schema, path=str(datapath))
    return index_disk


def tantivy_schema_get_default():
    schema_builder = tantivy.SchemaBuilder()
    schema_builder.add_text_field("title", stored=True, index_option="basic")
    schema_builder.add_text_field("body", stored=True, index_option="basic")
    schema_builder.add_text_field("id", stored=True, index_option="basic")
    schema_builder.add_text_field("categories", stored=True, index_option="basic")
    schema_builder.add_text_field("cat1", stored=True, index_option="basic")
    schema_builder.add_text_field("cat2", stored=True, index_option="basic")
    schema_builder.add_text_field("cat3", stored=True, index_option="basic")
    schema_builder.add_text_field("cat4", stored=True, index_option="basic")
    schema_builder.add_text_field("cat5", stored=True, index_option="basic")
    schema_builder.add_text_field("fulltext", index_option="position")

    schema = schema_builder.build()
    return schema


def tantivy_index_documents(
        dirin: str,
        datapath: str = None,
        kbatch: int = 10,
        colsused=None,
        db_sep: str = " @ ",
        db_heap_size: int = 50_0000_000,
        db_max_threads: int = 1,
) -> None:
    """Indexes documents into a Tantivy index.
    Args:
        dirin (str):  directory containing  documents to be indexed.
        datapath (str, optional):  path to  Tantivy index. Defaults to None.
        kbatch (int, optional):  batch size for committing documents to  index. Defaults to 10.
        colsused (List, optional):  list of columns to use for indexing. Defaults to None.
        db_sep (str, optional):  separator to use for concatenating text columns. Defaults to " @ ".
        db_heap_size (int, optional):  heap size for  Tantivy index. Defaults to 50_0000_000.
        db_max_threads (int, optional):  maximum number of threads for  Tantivy index. Defaults to 1.

    Returns:
        None
    """
    df = pd_read_file(path_glob=dirin)

    # create index schema if not already existing
    index_disk = tantivy_index_get(datapath)
    writer = index_disk.writer(heap_size=db_heap_size, num_threads=db_max_threads)

    textcols = (
        [col for col in df.columns if col not in ("id",)]
        if colsused is None
        else colsused
    )

    #### Insert inside  index
    for k, row in df.iterrows():
        # log(type(doc.categories))
        fulltext = db_sep.join(
                [str(row[col]) for col in textcols]
            )  # .title, row.body, " ".join(row.categories)])
        writer.add_document(
            tantivy.Document(
                title=row["title"],
                body=row["body"],
                id=int(row["id"]),
                # categories=row.categories if "categories" in row else "",
                fulltext=fulltext,
            )
        )

        if k % kbatch == 0:
            log("Commit:", k)
            writer.commit()

    writer.commit()
    writer.wait_merging_threads()


def tantivy_search(datapath: str = "./ztmp/tantivy_index", query: str = "", topk: int = 10):
    """Search a tantivy index
    datapath: str: path to  tantivy index
    query: str: query to search
    size: int: number of results to return
    :return: list of tuples (score, document) where document is a dictionary of  document fields
    """
    index = tantivy_index_get(datapath)
    # query_parser = reader.query_parser(["title", "body"], default_conjunction="AND")
    searcher = index.searcher()
    # print(f"Searching for: {query}")
    try:
        query = index.parse_query(query, ["fulltext"])
        results = searcher.search(query, topk).hits
        # log(results)
        score_docs = [
            (score, searcher.doc(doc_address)) for score, doc_address in results
        ]
        return score_docs
    except Exception as err:
        print(traceback.format_exc())
        return []


###############################################################################
def fusion_search(query="the", method="rrf", client=None) -> Dict:
    """Perform a fusion search using  given query and method.
    Args:
        query (str):  query to search for. Defaults to "the".
        method (str):  method to use for merging  results. Defaults to "rrf".

    Returns:
        Dict:  merged ranking results.

     Loose Coupling and Clear/Indentify coupling  between  code components.
     "id"  columns must in  dataframe

    """
    v1_results = qdrant_sparse_search(query, client=client)
    v1 = fusion_postprocess_qdrant(v1_results)

    v2_results = tantivy_search(query=query)
    v2 = fusion_postprocess_tantivy(v2_results)

    vmerge: Dict = ranx_merge_ranking(method, v1, v2)
    return vmerge


def fusion_postprocess_qdrant(results: List, colid="id") -> Dict:
    """Postprocess  search results from a sparse qdrant search.
    Args:
        results (List):  search results.

    Returns:
        List:  search results after postprocessing.
    """
    v1 = {
        str(scored_point.payload[colid]): scored_point.score for scored_point in results
    }
    # log(f"v1:{v1}")
    return v1


def fusion_postprocess_tantivy(results: List, colid="id") -> Dict:
    """Postprocess  search results from a tantivy search.
    Args:
        results (List):  search results.

    Returns:
        List:  search results after postprocessing.
    """
    v2 = {str(doc.get_all(colid)[0]): score for score, doc in results}
    # log(f"v2:{v2}")
    return v2


def ranx_merge_ranking(
        method="rrf",
        v1: Dict = None,
        v2: Dict = None,
) -> Dict:
    """Merge two rankings using  specified fusion method.

    Args:
        method (str, optional):  fusion method to use. Defaults to "rrf".
        v1 (Dict, optional):  first ranking to merge. Defaults to None.
        v2 (Dict, optional):  second ranking to merge. Defaults to None.

    Returns:
        Dict:  merged ranking results.
    Example:
        >>> v1 = {"d1": 0.5, "d2": 0.8, "d3": 0.3}
        >>> v2 = {"d1": 0.9, "d2": 0.2, "d3": 0.7}
        >>> ranx_merge_ranking(method="rrf", v1=v1, v2=v2)
        {'q1': {'d1': 0.5, 'd2': 0.8, 'd3': 0.3}}
    """
    run1 = Run.from_dict({"q1": v1})
    run2 = Run.from_dict({"q1": v2})

    # Fuse rankings using Reciprocal Rank Fusion (RRF)
    fused_run = fuse([run1, run2], method=method)
    log(f"run1:{run1}")
    log(f"run2:{run2}")
    log(fused_run)
    fused_run = dict(fused_run)
    return fused_run


###################################################################################
###################################################################################
def dataset_hf_to_parquet(
        name, dirout: str = "hf_datasets", splits: list = None, mapping: dict = None
):
    """Converts a Hugging Face dataset to a Parquet file.
    Args:
        dataset_name (str):  name of  dataset.
        dirout (str):  output directory.
        mapping (dict):  mapping of  column names. Defaults to None.
    """
    dataset = datasets.load_dataset(name)
    # print(dataset)
    if splits is None:
        splits = ["train", "test"]

    for key in splits:
        split_dataset = dataset[key]
        output_file = f"{dirout}/{name}/{key}.parquet"
        df = pd.DataFrame(split_dataset)
        log(df.shape)
        if mapping is not None:
            df = df.rename(columns=mapping)

        # Raw dataset in parquet
        pd_to_file(df, output_file)


def dataset_kaggle_to_parquet(
        name, dirout: str = "kaggle_datasets", mapping: dict = None, overwrite=False
):
    """Converts a Kaggle dataset to a Parquet file.
    Args:
        dataset_name (str):  name of  dataset.
        dirout (str):  output directory.
        mapping (dict):  mapping of  column names. Defaults to None.
        overwrite (bool, optional):  whether to overwrite existing files. Defaults to False.
    """
    # download dataset and decompress
    kaggle.api.dataset_download_files(name, path=dirout, unzip=True)

    df = pd_read_file(dirout + "/**/*.csv", npool=4)
    if mapping is not None:
        df = df.rename(columns=mapping)

    pd_to_file(df, dirout + f"/{name}/parquet/df.parquet")


def dataset_agnews_schema_v1(
        dirin="./**/*.parquet", dirout="./norm/", batch_size=1000
) -> None:
    """Standardize schema od a dataset"""
    flist = glob_glob(dirin)

    cols0 = ["text", "label"]

    for ii, fi in enumerate(flist):
        df = pd_read_file(fi, npool=1)
        log(ii, df[cols0].shape)

        #### New columns
        ### Schame : [ "id", "dt", ]
        n = len(df)
        dtunix = date_now(returnval="unix")
        df["id"] = [uuid_int64() for i in range(n)]
        df["dt"] = [int(dtunix) for i in range(n)]

        df["body"] = df["text"]
        del df["text"]

        df["title"] = df["body"].apply(lambda x: x[:50])
        df["cat1"] = df["label"]
        del df["label"]
        df["cat2"] = ""
        df["cat3"] = ""
        df["cat4"] = ""
        df["cat5"] = ""

        fname = fi.split("/")[-1]
        fout = fname.split(".")[0]  # derive target folder from source filename

        dirouti = f"{dirout}/{fout}"
        pd_to_file_split(df, dirouti, ksize=batch_size)


def pd_to_file_split(df, dirout, ksize=1000):
    kmax = int(len(df) // ksize) + 1
    for k in range(0, kmax):
        log(k, ksize)
        dirouk = f"{dirout}/df_{k}.parquet"
        pd_to_file(df.iloc[k * ksize: (k + 1) * ksize, :], dirouk, show=0)


##########################################################################
def np_str(v):
    return np.array([str(xi) for xi in v])


def torch_getdevice(device=None):
    if device is None or len(str(device)) == 0:
        return os.environ.get("torch_device", "cpu")
    else:
        return device


def uuid_int64():
    """## 64 bits integer UUID : global unique"""
    return uuid.uuid4().int & ((1 << 64) - 1)


def pd_fake_data(nrows=1000, dirout=None, overwrite=False, reuse=True) -> pd.DataFrame:
    from faker import Faker

    if os.path.exists(str(dirout)) and reuse:
        log("Loading from disk")
        df = pd_read_file(dirout)
        return df

    fake = Faker()
    dtunix = date_now(returnval="unix")
    df = pd.DataFrame()

    ##### id is integer64bits
    df["id"] = [uuid_int64() for i in range(nrows)]
    df["dt"] = [int(dtunix) for i in range(nrows)]

    df["title"] = [fake.name() for i in range(nrows)]
    df["body"] = [fake.text() for i in range(nrows)]
    df["cat1"] = np_str(np.random.randint(0, 10, nrows))
    df["cat2"] = np_str(np.random.randint(0, 50, nrows))
    df["cat3"] = np_str(np.random.randint(0, 100, nrows))
    df["cat4"] = np_str(np.random.randint(0, 200, nrows))
    df["cat5"] = np_str(np.random.randint(0, 500, nrows))

    if dirout is not None:
        if not os.path.exists(dirout) or overwrite:
            pd_to_file(df, dirout, show=1)

    log(df.head(1), df.shape)
    return df


def pd_fake_data_batch(nrows=1000, dirout=None, nfile=1, overwrite=False) -> None:
    """Generate a batch of fake data and save it to Parquet files.

    python engine.py  pd_fake_data_batch --nrows 100000  dirout='ztmp/files/'  --nfile 10

    """

    for i in range(0, nfile):
        dirouti = f"{dirout}/df_text_{i}.parquet"
        pd_fake_data(nrows=nrows, dirout=dirouti, overwrite=overwrite)


###################################################################################################
if __name__ == "__main__":
    import fire

    fire.Fire()

""" 


"""
