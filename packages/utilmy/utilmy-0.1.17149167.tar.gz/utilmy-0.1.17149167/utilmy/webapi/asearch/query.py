""" 

 # usage : 
      python query.py query_create_synthetic   --dirdata ztmp/bench --dataset ag_news --nfile 10 --nquery 100 >> ztmp/bench/ag_news/query/prompt_examples.txt


### summarize

    A) DSPy : initial prompt ---> Optim --> final prompt (Saved in DPSy model file).
           Optimizer (ie Prompt engineering)  Not inference.

      Prompt IS Model dependant : QWaen, GPT 3.6 , GPT 4.0  (can be similar.... but not same.)

       Append to promnpt storage csv



    B) At inference (Deterimnistic in Prompt)
      1 fixed promp_template
         filed with { value }
              --> send to API XXXX
              --> Get the answers
   
   Inference Structure:
      csv file on disk as Storage of ALL promptS (for all kind of tasks/queries)

       id_prompt, prompt_template, prompt_examples, prompt_arg, prompt_origin, task_name, model_name_full, dt,  api_endpoint, info_json,  ...
                                                                                           Openai/GPT3.5
                                                                                            Qwen 8gb 

     prompt_store(pomrpt, )  ### append to csv 


      prompt_template:
          You are and assistant.  Query is {queries}.  side info is {side_info}


      prompt_args:
          { "args" : { 
                "queries":   ("str", "this is an query"),
                "side_info": ("str", "this is an side info"),
          }         


prompt_example:
      [ " You are and assistant.  Query is Who is presndient.  side info is  my side info.  ", ... ]

    --> history of all prompts --> You have all --> Crooss easily, debug, transparent.


### At inference
   Pick one prompt from csv --  by ID
   fill the { value }  
    --> send it to the API




codeium
             





"""
import os
import fire
from utilmy import pd_read_file, pd_to_file, os_makedirs, glob_glob
import dspy

global turbo


def dspy_init():
    global turbo
    # initialize dspy module
    model_name = "gpt-3.5-turbo"
    # model_name = "gpt-4"
    turbo = dspy.OpenAI(model=model_name)
    dspy.settings.configure(lm=turbo)

dspy_init()


def prompt_create_actual(prompt_template:dict, prompt_values:dict):
     import copy
     prompt_actual = copy.deepcopy(prompt_template)
     for key, val in prompt_values.items():
         prompt_template = prompt_template.replace(f"{key}", val)
     return prompt_actual


def query_get_answer_from_llm(prompt_dict:dict, framework="DSPY", model_id="gpt-3.5-turbo", verbose=0):
    """   
        ask phind.com

    """

    if framework == "llamaIndex":
        prompt_template = prompt_dict["prompt_template"]
        prompt_actual:str = prompt_create_actual(prompt_template, prompt_values



        return dspy.Predict(prompt_dict, model=model_id)

    if framework == "DSPY":
        prompt = prompt_dict["prompt"]
        return dspy.Predict(prompt_dict, model=model_id)




def query_create_synthetic(dirdata: str = "ztmp/bench", dataset: str = "ag_news", 
                           nfile: int = 1, nquery: int = 1,
                           use_existing=1):
    """
    Generate synthetic queries via LLM
    """
    global turbo

    ### Inference
    prompt0 = PromptStorage(dirstorage=dirstorage) ### prompts/prompt_hist.csv
    prompt_dict = prompt0.get_prompt(prompt_id= prompt_id)  ## user decide whihc om
    ###

    ### Dpsy
    model_path = f"{dirdata}/{dataset}/query/query_model"
    os_makedirs(model_path)    
    q_model = QuestionGenerator()
    q_model.save(model_path)

    ###
    dirout = f"{dirdata}/{dataset}/query/df_synthetic_search.csv"


    if os.path.exists(dirout) and use_existing>0:
        df_query = pd_read_file(dirout)

    else:
        df = pd_read_file(f"{dirdata}/norm/{dataset}/*/df*.parquet", nfile=nfile)  ##  Real Dataset
        df["len"] = df["body"].apply(lambda x: len(x.split()))
        
        # filter out rows with body length < 100 words
        df = df[df["len"] > 100]
        nquery = min(nquery, len(df))
        
        # pick  random rows
        df_query = df.sample(nquery)
        
        # generate synthetic queries
        # df_query["queries"] = df_query["body"].apply(lambda x: q_model(x).answer)
        df_query["queries"] = df_query["body"].apply(lambda x: q_model(x).answer)
        
        df_query = df_query[["id", "body", "queries"]]
        # print(df_query["queries"].head())
        pd_to_file(df_query, f"{dirout}")

    ### You need to save the prompt, and config of the LLM

    # print last llm query/output, for debugging purposes
    turbo.inspect_history(n=1)
    return df_query




 class PromptStorage(self, dirstorage):
    def  __init__(self, dirstorage):

    self.df  = None 

    ### Fixes column names
    self.cols = ["prompt_id", "prompt_template", "prompt_examples", "prompt_arg", "prompt_origin", "task_name", "model_id", "dt", "api_endpoint", "info_json"]


    load(self): 
      self.df =  pd_read_csv(self.dirstorage)
      assert self.df[ self.cols].shape

      append(self, prompt_template, model_id, prompt_args, prompt_examples=None, task_name=None, info_json=None): 

       dfnew = {ci : "" for ci in self. cols }

       ### Codeium  and Phind in VScode
       dfnew["prompt_id"] = self.promptid_create()

       dfnew["prompt_template"] = prompt_template
       dfnew["model_id"] = model_id
       dfnew["prompt_args"] = prompt_args
       if prompt_examples is not None:
           dfnew["prompt_examples"] = prompt_examples
       if task_name is not None:
           dfnew["task_name"] = task_name
       if info_json is not None:
           dfnew["info_json"] = info_json
    
       dfnew = pd.dataFrame(dfnew)    

       self.df = pd.concat([self.df, dfnew], ignore_index=True)

       self.save()

     def save(self): ### Be carful comprotn ####, tab, | .... 
        pd.to_csv(self.df, self.dirstorage, sep="@@@") 


     def get_prompt(self, prompt_id: str,) --> dict: 
        #### external
        dfi = self.df[ self.df["prompt_id"] == prompt_id ]
        ddict = dfi.to_dict()

        return {"prompt_template": "", "model_id": "", "prompt_args": "", "prompt_examples": "", "task_name": "", "info_json": ""}

     def promptid_create(self):
        id YMD 20240401-{4digits}
             ymd= date_now(fmt="%Y%m%d", return_vale="str")
             prompt_id = f"{ymd}-{random.randint(100, 999)}"










############################################################################################
# build signature and specify input and output details in docstrings and description
class GenerateSyntheticQueries(dspy.Signature):
    """You are a helpful assistant. Given the following document, 
       generate a list of synthetic questions that could be answered by referring to the information provided in the document. 
       Ensure that the questions are clear, concise, and that their answers can be directly inferred from the document text.
    """
    document = dspy.InputField(desc="a document to generate queries from")
    queries = dspy.OutputField(
        desc="list of 10 queries separated by '@@'.")


class QuestionGenerator(dspy.Module):
    def __init__(self, sep="@@"):
        super().__init__()
        self.generate_answer = dspy.Predict(GenerateSyntheticQueries)
        self.sep= sep

    def forward(self, document):
        prediction = self.generate_answer(document=document)
        if self.sep not in prediction.queries:
            queries = prediction.queries.split("\n")
            # remove numbered prefix from queries
            # queries = [q.split(". ")[1] for q in queries]
            prediction.queries = "@@".join(queries)

        # queries = prediction.queries.split("")
        return dspy.Prediction(document=document, answer=prediction.queries)


if __name__ == '__main__':
    fire.Fire()

