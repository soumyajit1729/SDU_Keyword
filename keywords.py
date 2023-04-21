import pke
import tensorflow as tf
import tensorflow_hub as hub
import random
# from transformers import (
#   TokenClassificationPipeline,
#   AutoModelForTokenClassification,
#   AutoTokenizer,
# )
# from transformers.pipelines import AggregationStrategy
import numpy as np

from keybert import KeyBERT

def cosine_similarity_calc(vec_1,vec_2):
  
  sim = np.dot(vec_1,vec_2)/(np.linalg.norm(vec_1)*np.linalg.norm(vec_2))
  
  return sim
  
def remove_similar_words(list1,model):
  #print ("module %s loaded" % module_url)
  def embed(input):
    return model(input)
  message_embeddings = embed(list1)
  #print(list1,message_embeddings)
  fin_list = []
  c_list = [0 for i in range(len(list1))]
  for i in range(len(list1)):
    if(c_list[i]==0):
      fin_list.append(list1[i])
      for j in range(i+1,len(list1)):
        if(cosine_similarity_calc(message_embeddings[i],message_embeddings[j])>0.5):
          #print(message_embeddings[i],message_embeddings[j],cosine_similarity_calc(message_embeddings[i],message_embeddings[j]))
          
          list1[j]=1
  fin_list = [i for i in fin_list if i != 1]
  return fin_list

def get_words(txt):
  ns= set()
  res = txt.split()
  for x in res:
    ns.add(x.lower().strip(",? :/."))
  return ns


def extractor5(text):
  ans=[]

  

  
  # # Define keyphrase extraction pipeline
  # class KeyphraseExtractionPipeline(TokenClassificationPipeline):
  #     def __init__(self, model, *args, **kwargs):
  #         super().__init__(
  #             model=AutoModelForTokenClassification.from_pretrained(model),
  #             tokenizer=AutoTokenizer.from_pretrained(model),
  #             *args,
  #             **kwargs
  #         )

  #     def postprocess(self, model_outputs):
  #         results = super().postprocess(
  #             model_outputs=model_outputs,
  #             aggregation_strategy=AggregationStrategy.SIMPLE,
  #         )
  #         return np.unique([result.get("word").strip() for result in results])
  # # Load pipeline
  # model_name = "ml6team/keyphrase-extraction-kbir-inspec"
  # extractor = KeyphraseExtractionPipeline(model=model_name)

  # for x in extractor(text):
  #   ans.append(x)
  
    # initialize keyphrase extraction model, here TopicRank
  extractor = pke.unsupervised.TopicRank()

  # load the content of the document, here document is expected to be a simple 
  # test string and preprocessing is carried out using spacy
  extractor.load_document(input=text, language='en')

  # keyphrase candidate selection, in the case of TopicRank: sequences of nouns
  # and adjectives (i.e. `(Noun|Adj)*`)
  extractor.candidate_selection()

  # candidate weighting, in the case of TopicRank: using a random walk algorithm
  extractor.candidate_weighting()

  # N-best selection, keyphrases contains the 10 highest scored candidates as
  # (keyphrase, score) tuples
  keyphrases = extractor.get_n_best(n=10)
  
  for (x1,x2) in keyphrases:
    ans.append(x1.capitalize())

  kw_model = KeyBERT(model='all-mpnet-base-v2') 
  keywords = kw_model.extract_keywords(text,keyphrase_ngram_range=(1, 1), stop_words='english')  
  for x in keywords:
    ans.append(x[0].capitalize())

  module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
  model = hub.load(module_url)
  ans = remove_similar_words(ans,model)

  chk_set = get_words(text)
  ans1 = []
  for x in ans:
    flag=1
    for z in x.lower().split():
      if z not in chk_set:
        flag=0
        break
    if flag:
      ans1.append(x.capitalize())
      
  # random.shuffle(ans1)
  # if len(ans1)>15:
  #   ans1 = ans1[0:15]
  return ans1