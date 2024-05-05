"""

git clone https://github.com/arita37/myutil.git
cd myutil
git checkout devtorch

git pull --all


#### Model to use Deberta V3 for multi label classifier
  
https://github.com/rohan-paul/LLM-FineTuning-Large-Language-Models/blob/main/Other-Language_Models_BERT_related/Deberta-v3-large-For_Kaggle_Competition_Feedback-Prize/deberta-v3-large-For_Kaggle_Competition_Feedback-Prize.ipynb

https://github.com/rohan-paul/LLM-FineTuning-Large-Language-Models/blob/main/Other-Language_Models_BERT_related/DeBERTa_Fine_Tuning-for_Amazon_Review_Dataset_Pytorch.ipynb



#### Gliner






### Working folder
cd utilmy/webapi/asearch/nlp/


### in your Local PC : store dataset big ffiles
   mkdir -p ztmp
  ztmp/data/... Big Files...

   "ztmp" is gitignore ---> Wont commit ok, in your local

   dirdata="ztmp/data/#

   utilmy/webapi/asearch/nlp/ztmp/  --> wont be committed.



### working files

    sentiment.py
    ner.py


#### Dataset :
   News dataset
        https://huggingface.co/datasets/ag_news




        https://zenn.dev/kun432/scraps/1356729a3608d6

        https://huggingface.co/datasets/big_patent


  NER and Classification on News Dataset.


##### Task
     https://huggingface.co/datasets/ag_news
   AgNews ---> Add new label columns Manually label2, label3
         put random category.
         Small dataset ---> code working.  100 samples is enough.
         

   1) Fine tuning for classification on newsDatast
       Use  Sentence Transformers  ( deberta V3  or)
        Add task Head to fine tune
       text --> category

     English only.
     Save model + fine tune part on disk

     Generate the embedding for the text.
          ( I have only in fine tuned embedding)

      Dataset
        id,
        text,



        label1,  Integer cat
        label2,  Integer cat
        label3,  Integer cat

          model.predict(text) --->  { "label1": "cat", "label2": "subcat", "label3": "subsubcat" }


     Mutil Label classifier Head Classifier :
        label1 :  cata, catb, catc
        label2 :  subcat1, subcat2, subcat3
        label3 :  subsubcat1, subsubcat2, subsubcat3



1) sentences transformers   : More customization for Loss.



2) setfit library : very fast fine tuning with only Classifier loss
  for LLM,
      Sentence Transformers is generally better for a wide range of tasks
      involving sentence embeddings and similarity measures due to its flexibility
      and extensive model support.

      SetFit, however, is optimized for simplicity and efficiency
      in fine-tuning text classification models on small datasets.
      Choose Sentence Transformers for versatility and broader applications, or SetFit for efficient text classification with limited data.

      Sentence Transformers: https://www.sbert.net/
      SetFit: https://huggingface.co/docs/setfit/index



pip install utilmy python-box fire


df =  pd_read_file("/**/myfile.parquet")

pd_to_file(df, "myfolder/myfile.parquet")


Do not spend time on accuracy
  jsut need the code working.



https://colab.research.google.com/github/NielsRogge/Transformers-Tutorials/blob/master/BERT/Fine_tuning_BERT_(and_friends)_for_multi_label_text_classification.ipynb




""" 
from utilmy import pd_read_file, os_makedirs, pd_to_file, date_now, glob_glob
from utilmy import log, log2


def test123(val=""):
   print("ok")




import torch
import torch.nn as nn
from transformers import BertModel
from sentence_transformers import SentenceTransformer

class MultiLabelMultiClassModel(nn.Module):
    def __init__(self, num_labels_list):
        super().__init__()
        self.bert = SentenceTransformer('bert-base-uncased').bert
        self.classification_heads = nn.ModuleList([
            nn.Linear(self.bert.config.hidden_size, num_labels) for num_labels in num_labels_list
        ])

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        pooled_output = outputs.pooler_output
        logits = [head(pooled_output) for head in self.classification_heads]
        return logits

# Example usage:
model = MultiLabelMultiClassModel(num_labels_list=[3, 4])  # Assuming 3 classes for the first label set, 4 for the second
input_ids = torch.tensor([[101, 1024, 102]])  # Example input
attention_mask = torch.tensor([[1, 1, 1]])    # Example attention mask
logits = model(input_ids, attention_mask)


###################################################################################################
if __name__ == "__main__":
    import fire
    fire.Fire()
    ### python classifier.py  test123   --val" myval"
