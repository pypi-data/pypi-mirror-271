



https://gautam75.medium.com/unlocking-the-power-of-rag-fusion-53437e77d9c2


#####
   query ---> Generate Similar query --> do RAG on similar query. 
   



def dataset_custom_map_v1(dataset_name):
    """Converts a Hugging Face dataset to a Parquet file.
    Args:
        dataset_name (str):  name of  dataset.
        mapping (dict):  mapping of  column names. Defaults to None.
    """
    dataset = datasets.load_dataset(dataset_name)

    df
    # print(dataset)
    for key in dataset:
        df = pd.DataFrame(dataset[key])
        if mapping is not None:
            df = df.rename(columns=mapping)
        # print(df.head)



ksize=1000
kmax = int(len(df) // ksize) +1
for k in range(0, kmax):
    log(k)
    dirouk = f"{dirout}/{df}_{k}.parquet"
    pd_to_file( df.iloc[k*ksize:(k+1)*ksize, : ], dirouk, show=0)




## Recommended Imports
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    NamedSparseVector,
    NamedVector,
    SparseVector,
    PointStruct,
    SearchRequest,
    SparseIndexParams,
    SparseVectorParams,
    VectorParams,
    ScoredPoint,
)

## Creating a collection
client.create_collection(
    collection_name,
    vectors_config={
        "text-dense": VectorParams(
            size=1024,  # OpenAI Embeddings
            distance=Distance.COSINE,
        )
    },
    sparse_vectors_config={
        "text-sparse": SparseVectorParams(
            index=SparseIndexParams(
                on_disk=False,
            )
        )
    },
)

## Creating Points
points = []
for idx, (text, sparse_vector, dense_vector) in enumerate(
    zip(product_texts, sparse_vectors, dense_vectors)
):
    sparse_vector = SparseVector(
        indices=sparse_vector.indices.tolist(), values=sparse_vector.values.tolist()
    )
    point = PointStruct(
        id=idx,
        payload={
            "text": text,
            "product_id": rows[idx]["product_id"],
        },  # Add any additional payload if necessary
        vector={
            "text-sparse": sparse_vector,
            "text-dense": dense_vector,
        },
    )
    points.append(point)

## Upsert
client.upsert(collection_name, points)






def zzz_fastembed_embed_v2(wordlist: list[str], size=128, model=None) -> List:
    """pip install fastembed
    Docs:

         BAAI/bge-small-en-v1.5 384   0.13
         BAAI/bge-base-en       768   0.14
         sentence-transformers/all-MiniLM-L6-v2   0.09

        ll= list( qdrant_embed(['ik', 'ok']))

        ### https://qdrant.github.io/fastembed/examples/Supported_Models/
        from fastembed import TextEmbedding
        import pandas as pd
        pd.set_option("display.max_colwidth", None)
        pd.DataFrame(TextEmbedding.list_supported_models())

    """
    # from fastembed.embedding import FlagEmbedding as Embedding
    #
    # if model is None:
    #     model = Embedding(model_name=model_name, max_length=size)

    vectorlist = list(model.embed(wordlist))
    return vectorlist


# def zzz_test_qdrant_dense_search():  # moved to benchmark function
#     """
#         Unit test for search
#
#
#        Time performance
#
#     """
#     # create query df in ztmp directory
#     collection_name = "hf-dense-3"
#     dirtmp = "ztmp/df_search_test.parquet"
#
#     if not os.path.exists(dirtmp):
#         # df = pd_fake_data(nrows=1000, dirout=None, overwrite=False)
#         df = pd_read_file("norm/*/df_0.parquet")
#         # pick thousand random rows
#         search_df = df.sample(1000)
#         pd_to_file(search_df, dirtmp)
#     else:
#         search_df = pd_read_file(dirtmp)
#
#     model_type = "stransformers"
#     model_id = "sentence-transformers/all-MiniLM-L6-v2"  ### 384,  50 Mb
#     model = EmbeddingModel(model_id, model_type)
#
#     for i, row in search_df.iterrows():
#         # print(row)
#         id = row["id"]
#         query = row["body"][:300]
#         results = qdrant_dense_search(query, collection_name=collection_name,
#                                       model=model, topk=5)
#         top_5 = [scored_point.id for scored_point in results]
#         try:
#             assert len(results) > 0
#             assert id in top_5
#         except AssertionError:
#             log(f"Query: {query}")
#             log(f"id: {id}")
#             log(f"Top 5: {top_5}")
#             raise AssertionError

# def zzz_test_datasets_convert_kaggle_to_parquet():
#     """test function for converting Kaggle datasets to Parquet files
#     """
#     dataset_name = "gowrishankarp/newspaper-text-summarization-cnn-dailymail"
#     mapping = {"comment_text": "body", "toxic": "cat1"}
#     datasets_convert_kaggle_to_parquet(dataset_name, dirout="kaggle_datasets", mapping=mapping)
#     assert os.path.exists(f"kaggle_datasets/{dataset_name}.parquet")
#     # pd = pd_read_file(f"kaggle_datasets/{dataset_name}.parquet")
#     # print(pd.columns)


def zzz_torch_sparse_vectors_calc(texts: list, model_id: str = None):
    """Compute sparse vectors from a list of texts
    texts: list: list of texts to compute sparse vectors
    model_id: str: name of  model to use
    :return: list of tuples (indices, values) for each text


    """

    # Initialize tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForMaskedLM.from_pretrained(model_id)

    # Tokenize all texts
    tokens_batch = tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
    # Forward pass through  model
    with torch.no_grad():
        output = model(**tokens_batch)

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
    indices_list = [indices.numpy().flatten().tolist() for indices in indices_list]
    # for each tensor in  batch, get  values of  non-zero elements
    values = [
        max_vals[i][indices].numpy().tolist() for i, indices in enumerate(indices_list)
    ]

    return list(zip(indices_list, values))


def zzz_torch_sparse_map_vector(cols: List, weights: List, model_id=None):
    """Extracts non-zero elements from a given vector and maps these elements to their human-readable tokens using a tokenizer.  function creates and returns a sorted dictionary where keys are  tokens corresponding to non-zero elements in  vector, and values are  weights of these elements, sorted in descending order of weights.

     function is useful in NLP tasks where you need to understand  significance of different tokens based on a model's output vector. It first identifies non-zero values in  vector, maps them to tokens, and sorts them by weight for better interpretability.

    Args:
    vector (torch.Tensor): A PyTorch tensor from which to extract non-zero elements.
    tokenizer:  tokenizer used for tokenization in  model, providing  mapping from tokens to indices.

    Returns:
    dict: A sorted dictionary mapping human-readable tokens to their corresponding non-zero weights.
    """
    tokenizer = AutoTokenizer.from_pretrained(model_id)

    # Map indices to tokens and create a dictionary
    idx2token = {idx: token for token, idx in tokenizer.get_vocab().items()}
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









pip install qdrant-client
pip install qdrant_openapi_client



from qdrant_client import QdrantClient
from qdrant_client.http.models import CollectionConfig, Distance, FieldIndexOperations, OptimizersConfig, WalConfig
from qdrant_openapi_client.models.models import VectorParams

# Initialize the Qdrant client with embedded mode
client = QdrantClient(embedded=True, storage_path="/path/to/storage")

# Create a collection with specific configuration
collection_name = "my_embedded_collection"
vector_dim = 128
collection_config = CollectionConfig(
    vector_size=vector_dim,
    distance=Distance.COSINE,
    optimizers_config=OptimizersConfig(
        wal=WalConfig(
            wal_capacity_mb=32,
            wal_segments_ahead=0
        )
    )
)
client.recreate_collection(collection_name, collection_config)

# Insert points into the collection
points = [
    {"id": 1, "vector": [0.1]*vector_dim, "payload": {"name": "point1"}},
    {"id": 2, "vector": [0.2]*vector_dim, "payload": {"name": "point2"}}
]
client.upsert_points(collection_name, points)

# Search for points
query_vector = [0.15]*vector_dim
search_params = {"top": 10}
results = client.search(collection_name, query_vector, search_params)

# Print search results
for result in results:
    print(f"ID: {result['id']}, Distance: {result['distance']}, Payload: {result['payload']}")

# Delete the collection
client.drop_collection(collection_name)






""" 
######### Ressources


https://medium.com/gopenai/improved-rag-with-llama3-and-ollama-c17dc01f66f6








"""