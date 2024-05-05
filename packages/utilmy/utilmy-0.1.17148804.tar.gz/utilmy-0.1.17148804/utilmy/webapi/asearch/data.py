# -*- coding: utf-8 -*-
"""
    #### Install
        cd myutil 
        cd utilmy/webapi/asearch/
        pip install -r pip/py39_full.txt
        pip install fastembed==0.2.6 loguru --no-deps


    #### ENV variables
        export HF_TOKEN=
]

    ##### Usage : 
            cd utilmy/webapi/asearch/
            mkdir -p ./ztmp

            python data.py run_convert --name "ag_news"  --diroot  "./ztmp/hf_datasets/"   



    ##### Flow
        HFace Or Kaggle --> dataset in RAM--> parquet (ie same columns)  -->  parquet new columns (final)
        Example :   
             huggingface.co/datasets/valurank/News_Articles_Categorization
             {name}-{dataset_name}

              ### MetaData JSON saved here
                       ---> ztmp/hf_data/meta/valurank-News_Articles_Categorization.json"

              ### Data saved here:
                       ---> ztmp/hf_data/data/valurank-News_Articles_Categorization/train/df.parquet"
                       ---> ztmp/hf_data/data/valurank-News_Articles_Categorization/test/df.parquet"



       Target Schema is  SCHEMA_GLOBAL_v1 



    #### Dataset TODO:

        https://huggingface.co/datasets/ashraq/financial-news-articles

        https://huggingface.co/datasets/big_patent

        https://huggingface.co/datasets/cnn_dailymail



    ### Dataset Done
        https://huggingface.co/datasets/ag_news


    #### Dataset Done in Google Drtice
       https://drive.google.com/drive/folders/1Ggzl--7v8xUhxr8a8zpRtgh2fI9EXxoG?usp=sharing



    ##### Infos
        https://huggingface.co/datasets/big_patent/tree/refs%2Fconvert%2Fparquet/a/partial-train

        https://zenn.dev/kun432/scraps/1356729a3608d6




"""
import warnings
warnings.filterwarnings("ignore")
import os, pathlib, uuid, time, traceback, copy, json
from box import (Box, BoxList,  )
from typing import Any, Callable, Dict, List, Optional, Sequence, Union
import pandas as pd, numpy as np, torch
import mmh3

import datasets

from utilmy import pd_read_file, os_makedirs, pd_to_file, date_now, glob_glob
from utilmy import log, log2


######################################################################################
#### All dataset has normalized columns : simplify training
SCHEMA_GLOBAL_v1 = [
    ("id_global",  "int64", "global unique ID"),
    ("id_dataset", "int64", "global unique ID of the dataset"),

    ("id_local", "int64", "local ID"),
    ("dt", "float64", "Unix timestamps"),

    ("title", "str", " Title "),
    ("summary", "str", " Summary "),
    ("body", "str", " Summary "),
    ("info_json", "str", " Extra info in JSON string format "),

    ("cat1", "str", " Category 1 or label "),
    ("cat2", "str", " Category 2 or label "),
    ("cat3", "str", " Category 3 or label "),
    ("cat4", "str", " Category 4 or label "),
    ("cat5", "str", " Category 5 or label "),
]



#### JSON saved on in  dirdata_meta/
meta_json =Box({
  "name"             : "str",
  "name_unique"      : "str",
  "url"              : "str",
  "nrows"            : "int64",
  "columns"          : "list",
  "columns_computed" : "list",  ### Computed columns from original
  "lang"             : "list",  ## list of languages
  "description_full" : "str",
  "description_short": "str",
  "tasks"            : "list",  ## List of tasks
  "info_json"        : "str",   ## JSON String to store more infos
  "dt_update"        : "int64", ## unix

})


####################################################################################
def run_convert(name="ag_news", diroot: str = "./ztmp/hf_datasets", 
                splits: list = None, schema_fun: str = "schema_agnews"
):
    """Converts a Hugging Face dataset to a Parquet file + JSON File
    Args:
        dataset_name (str):  name of  dataset.
        dirout (str):  output directory.

     python data.py run_convert --name "ag_news"  --diroot  "./ztmp/hf_datasets/"   

    DatasetDict({
        train: Dataset({
            features: ['text', 'label'],
            num_rows: 120000
        })
        test: Dataset({
            features: ['text', 'label'],
            num_rows: 7600
        })
    })

    """
    name2 = name.replace("/","-")
    splits = ["train", "test"]     if splits is None else splits

    ### from utilmy import load_function_uri
    convert_fun = globals()[ schema_fun ]  #load_function_uri(f"data.py:{schema_fun}")

    cc = copy.deepcopy(meta_json)
    cc.name = name
    cc.name_unique = name2
  
    log("###### Loading dataset ")
    dataset     = datasets.load_dataset(name)
    cc.metadata = hf_dataset_meta_todict(dataset)

    nrows=0    
    for key in splits:
        df = pd.DataFrame(dataset[key])
        df = convert_fun(df, meta_dict=cc)
        log(list(df.columns), df.shape)
        nrows += len(df)

        dirout = f"{diroot}/{name2}/{key}/df.parquet"
        pd_to_file(df, dirout,show=1)

    ##### meta
    cc.dt_update = int(time.time())
    cc.url       = name
    cc.nrows     = nrows
    cc.columns   = list(df.columns)


    from utilmy import json_save
    json_save(dict(cc), f"{diroot}/meta/{name2}.json")




def box_to_dict(box_obj):

    from box import (Box, BoxList,  )
    if isinstance(box_obj, Box):
        box_obj = {k: box_to_dict(v) for k, v in box_obj.items()}

    elif isinstance(box_obj, dict):
        return {k: box_to_dict(v) for k, v in box_obj.items()}
    elif isinstance(box_obj, list):
        return [box_to_dict(v) for v in box_obj]

    return str(box_obj) 


def hf_dataset_meta_todict(dataset):
   metadata = { "split": [] } 
   for split in dataset.keys():  ### Train
      ##### Convert metadata to dictionary
      mdict = {key: value for key, value in dataset[split].info.__dict__.items()}
      metadata[split] = mdict
      metadata["split"].append(split)

   return metadata   





#######################################################################################
######## Custom Schema ################################################################
def hash_mmh64(xstr: str) -> int:
    # pylint: disable=E1136
    return mmh3.hash64(str(xstr), signed=False)[0]


def schema_agnews(df:pd.DataFrame, meta_dict:dict=None) -> pd.DataFrame:
    """Convert columns/ schema output a dataset
    pd_to_file(df, "ztmp/hf_data/ag_news/train/df.parquet")

    schema_agnews(df)

    """
    # from utilmy.utilmy_base import hash_mmh64

    cols0 = ["text", "label"]
    log(df[cols0].shape)

    url = meta_dict["url"]

    #### Taget columns
    n = len(df)
    dtunix = float(date_now(returnval="unix"))
    dataset_idhash  =  hash_mmh64(url) 

    df["id_global"]  = [uuid_int64() for i in range(n)]
    df["id_dataset"] = dataset_idhash
    df["dt"] = dtunix


    ###### Custom mapping ###########################
    df["id_local"]  = -1
    df["title"]     = df["text"].apply(lambda x: " ".join(x.split(" ")[:7]) )
    df["summary"]   = ""
    df["body"]      = df["text"]  ; del df["text"]
    df["info_json"] = df.apply(lambda x: json.dumps({}), axis=1)
    df["cat1"]      = df["label"] ; del df["label"]
    df["cat2"]      = ""
    df["cat3"]      = ""
    df["cat4"]      = ""
    df["cat5"]      = ""

    cols1 = [x[0] for x in  SCHEMA_GLOBAL_v1 ] 
    df = df[cols1]
    return df



































#######################################################################################
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
        df["cat6"] = ""
        df["cat7"] = ""
        df["cat8"] = ""
        df["extra_json"] = ""

        fname = fi.split("/")[-1]
        fout = fname.split(".")[0]  # derive target folder from source filename

        dirouti = f"{dirout}/{fout}"
        pd_to_file_split(df, dirouti, ksize=batch_size)


def pd_to_file_split(df, dirout, ksize=1000):
    kmax = int(len(df) // ksize) + 1
    for k in range(0, kmax):
        log(k, ksize)
        dirouk = f"{dirout}/df_{k}.parquet"
        pd_to_file(df.iloc[k * ksize : (k + 1) * ksize, :], dirouk, show=0)



##########################################################################
def np_str(v):
    return np.array([str(xi) for xi in v])


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



