# import tensorflow as tf
# import tensorflow_hub as hub

from transformers import (
  TokenClassificationPipeline,
  AutoModelForTokenClassification,
  AutoTokenizer,
)
from transformers.pipelines import AggregationStrategy
import numpy as np

from keybert import KeyBERT

def extractor(txt):
  # Define keyphrase extraction pipeline
  class KeyphraseExtractionPipeline(TokenClassificationPipeline):
      def __init__(self, model, *args, **kwargs):
          super().__init__(
              model=AutoModelForTokenClassification.from_pretrained(model),
              tokenizer=AutoTokenizer.from_pretrained(model),
              *args,
              **kwargs
          )

      def postprocess(self, model_outputs):
          results = super().postprocess(
              model_outputs=model_outputs,
              aggregation_strategy=AggregationStrategy.SIMPLE,
          )
          return np.unique([result.get("word").strip() for result in results])
  # Load pipeline
  model_name = "ml6team/keyphrase-extraction-kbir-inspec"
  extractor = KeyphraseExtractionPipeline(model=model_name)

  l1 = []
  for x in extractor(txt):
    l1.append(x)
  
  kw_model = KeyBERT(model='all-mpnet-base-v2')
  keywords = kw_model.extract_keywords(txt,keyphrase_ngram_range=(1, 3), stop_words='english')  
  for x in keywords:
    l1.append(x[0])
  # module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
  # model = hub.load(module_url)
  # print("Keyword done")
  # l1 = remove_similar_words(l1,model)
  return l1  

# def cosine_similarity_calc(vec_1,vec_2):
  
#   sim = np.dot(vec_1,vec_2)/(np.linalg.norm(vec_1)*np.linalg.norm(vec_2))
  
#   return sim
# def remove_similar_words(list1,model):
  #print ("module %s loaded" % module_url)
  # def embed(input):
  #   return model(input)
  # message_embeddings = embed(list1)
  # #print(list1,message_embeddings)
  # fin_list = []
  # c_list = [0 for i in range(len(list1))]
  # for i in range(len(list1)):
  #   if(c_list[i]==0):
  #     fin_list.append(list1[i])
  #     for j in range(i+1,len(list1)):
  #       if(cosine_similarity_calc(message_embeddings[i],message_embeddings[j])>0.8):
  #         #print(message_embeddings[i],message_embeddings[j],cosine_similarity_calc(message_embeddings[i],message_embeddings[j]))
          
  #         list1[j]=1
  # fin_list = [i for i in fin_list if i != 1]
  # return fin_list