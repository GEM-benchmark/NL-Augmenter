import random
import string
import concurrent.futures

from transformers import MarianMTModel,MarianTokenizer

from .easy_nmt import load_easynmt_model,get_easynmt_translation
from .use_filter import load_use_model,get_use_embedding
from .constants import HUGGINGFACE_MARIANMT_MODELS_TO_LOAD, EASYNMT_MODEL_NAME

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

# methods to print colored text in the terminal
def pr_green(text):
    """ Pring text in green color font"""
    print("\033[92m{}\033[00m" .format(text))

def pr_gray(text):
    """ Pring text in gray color font"""
    print("\033[7m{}\033[00m" .format(text))

class MultiPivotParaphrasesGeneration(SentenceOperation):
    """
    This transformation generates a list of paraphrases for an English sentence by leveraging Pivot-Transaltion approach.
    Pivot-Transaltion is an approach where a sentence in a source language is translated to a foreign language called the pivot language then
    translated back to the source language to get a paraprhase candidate, e.g. translate an English sentence to French, then translate back to English.

    The paraphrases generation is divided into two step:
    - Step 1: paraphrases Candidate Over-generation by leveraging Pivot-Transaltion. At this step, we generate a Pool of possible parparhases.
    - Step 2: apply a candidate selection over the Pool of paraphrases, since the pool can contain semantically unrelated or duplicate paraphrases.
      We leverage Embedding Model such as Universal Sentence Encoder~(USE) to disqualify candidate paraphrases from the pool, by computing the Cosine Similarity socres of the
      USE Embeddings between the reference sentence and the candidate paraphrase. Let R = USE_Embeding(reference_english_sentence) and P = USE_Embeding(candidate):
        - if Cosine(R,P) < alpha => the candidate is semantically unrelated and then removed from the final list of paraphrases
        - if Cosine(R,P) > beta => the candidate is a duplication and then removed from the final list of paraphrases
        - By default Alpha=0.5 and Beta=0.95, we set the value as suggested by [Parikh et al.](https://arxiv.org/pdf/2004.03484.pdf) works
    
    Please refer to the test.json for all of the test cases catered.
    
    This transformation translates an English sentence to a list of predefined languages using Huggingface MariamMT and EasyNMT as Machine Transaltion models.
    - The transformation support Two Pivot-Transaltion Level.
        - If Pivot-level = 1 => Transalte to only one foreign language. e.g. English -> French -> English  ||  English -> Arabic -> English  ||  English -> japanese -> English
        - If Pivot-level = 2 => Transalte to only Two foreign language. e.g. English -> French -> Arabic -> English  ||  English -> Russian -> Chinese -> English
    """
    
    tasks = [
        TaskType.QUESTION_GENERATION,
        TaskType.TEXT_TO_TEXT_GENERATION
    ]
    languages = ["en"]
    keywords = ["lexical", "rule-based", "syntactic","highly-meaning-preserving","transformer-based","tokenizer-required","high-generations"]
    heavy = True


    def __init__(self, seed=0 , pivot_level=1):
        """
        Generate parpahrases for an English sentence by Leveraging pivot transaltion
        :param pivot_level: integer that indicate the pivot language level, single-pivot or multi-pivot range,1 =single-pivot, 2=double-pivot, 0=apply single and double
        """

        super().__init__(seed)
        self.pivot_level = pivot_level
        self.models = self.concurrent_model_loader()
        self.use_embed_model = None

    def generate(self, sentence:str, candidate_selection = True):
        """
        Generate a list of paraphrases for sentence
        :param sentence: English sentence to be paraprhased
        :param candidate_selection: remove semantiically unrelate paraphrases cadidates using USE_Embedding_Cosine_Similarity scores. False: don't apply candidate selction | True: apply 
        :return list of paraphrases
        """

        paraphrases = self.multi_translate(sentence,self.models)

        if candidate_selection:
            #load_use_model
            if not self.use_embed_model:
                pr_gray("Load Universal Sentence Encoder Model:")
                use_model_name = "https://tfhub.dev/google/universal-sentence-encoder-large/5"
                self.use_embed_model = load_use_model(use_model_name)
                pr_green("... done")

            #compute cosine similarity scores to remove semantically unrelated candidates
            pr_gray("Start paraphrases candidate selection:")
            paraphrases = get_use_embedding(paraphrases, self.use_embed_model, sentence)

            pr_green("... done")
        
        return paraphrases

    def translate(self,utterance,model,tok,trg="NONE"):
        """
        Translate a single sentence
        :param utterance: sentence to translate
        :param model: transformers Marian Machine Transaltion Model(MarianMTModel)
        :param tok: transformers Marian Tokenizer module(MarianTokenizer)
        :param trg: target language - set value when using en-ROMANCE model - trg=>>fr<<|>>it<<|>>es<<|>>pt<<
        :return Translated utterance 
        """
        if trg != 'NONE':
            utterance = '>>'+trg+'<<  '+utterance
        # translated = model.generate(**tok.prepare_translation_batch([utterance]))#old version transformers==3.0.0
        translated = model.generate(**tok(utterance, return_tensors="pt", padding=True))
        result = [tok.decode(t, skip_special_tokens=True) for t in translated]

        result = result[0]

        # check token indices sequence length is longer than the specified maximum sequence length max_length=512
        if len(result) > 512:
            result = result[:512]
        return result


    def multi_translate(self,utterance,model):
        """
        Translate sentence
        :param utterance: sentence to translate
        :param model_list: dictionary containing marianMT model, key: model name - value: list containing respectively  Model and tokenizer.  e.g. {'en2ROMANCE':[model,tekenizer]}
        :return list of utterance translations
        """
        response = set()

        if self.pivot_level == 0 or self.pivot_level == 1:#one pivot language
            # Translate to Italian
            tmp = self.translate(utterance,model['en2romance'][0],model['en2romance'][1],trg="it")
            tmp = self.translate(tmp,model['romance2en'][0],model['romance2en'][1])#translate back to English
            response.add(tmp)

            # Translate to French
            tmp = self.translate(utterance,model['en2romance'][0],model['en2romance'][1],trg="fr")
            tmp = self.translate(tmp,model['romance2en'][0],model['romance2en'][1])#translate back to English
            response.add(tmp)

            # Translate to Spanish
            tmp = self.translate(utterance,model['en2romance'][0],model['en2romance'][1],trg="es")
            tmp = self.translate(tmp,model['romance2en'][0],model['romance2en'][1])#translate back to English
            response.add(tmp)

            # Translate to Portuguese
            tmp = self.translate(utterance,model['en2romance'][0],model['en2romance'][1],trg="pt")
            tmp = self.translate(tmp,model['romance2en'][0],model['romance2en'][1])#translate back to English
            response.add(tmp)

            # Translate to Romanian
            tmp = self.translate(utterance,model['en2romance'][0],model['en2romance'][1],trg="ro")
            tmp = self.translate(tmp,model['romance2en'][0],model['romance2en'][1])#translate back to English
            response.add(tmp)

            # Translate to German
            tmp = self.translate(utterance,model['en2de'][0],model['en2de'][1])
            tmp = self.translate(tmp,model['de2en'][0],model['de2en'][1])#translate back to English
            response.add(tmp)

            # Translate to Russian
            tmp = self.translate(utterance,model['en2ru'][0],model['en2ru'][1])
            tmp = self.translate(tmp,model['ru2en'][0],model['ru2en'][1])#translate back to English
            response.add(tmp)

            # Translate to Arabic
            tmp = self.translate(utterance,model['en2ar'][0],model['en2ar'][1])
            tmp = get_easynmt_translation( tmp, model['easy_nmt'], 'en', 'ar') # translate back to English with EasyNMt 
            response.add(tmp)

            # Translate to Chinese
            tmp = self.translate(utterance,model['en2zh'][0],model['en2zh'][1])
            tmp = self.translate(tmp,model['zh2en'][0],model['zh2en'][1])#translate back to English
            response.add(tmp)

            # Translate to Japanese
            tmp = self.translate(utterance,model['en2jap'][0],model['en2jap'][1])
            tmp = get_easynmt_translation( tmp, model['easy_nmt'], 'en', 'ja') # translate back to English with EasyNMt 
            response.add(tmp)
            
        if self.pivot_level == 0 or self.pivot_level == 2:# two pivot language
            # Translate Spanish => Russian = > English
            tmp = self.translate(utterance,model['en2romance'][0],model['en2romance'][1],trg="es")
            tmp = get_easynmt_translation( tmp, model['easy_nmt'], 'ru', 'es') # translate to Russian with EasyNMt
            tmp = self.translate(tmp,model['ru2en'][0],model['ru2en'][1])#translate back to English
            response.add(tmp)

            # Translate Japanese => Spanish = > English
            tmp = self.translate(utterance,model['en2jap'][0],model['en2jap'][1])#translate to Japanese
            tmp = get_easynmt_translation( tmp, model['easy_nmt'], 'es', 'ja') # translate to Spanish with EasyNMt
            tmp = self.translate(tmp,model['romance2en'][0],model['romance2en'][1])#translate back to English
            response.add(tmp)

            # Translate Japanese => Italian = > English
            tmp = self.translate(utterance,model['en2jap'][0],model['en2jap'][1])#translate to Japanese
            tmp = get_easynmt_translation( tmp, model['easy_nmt'], 'it', 'ja') # translate to Italian with EasyNMt
            tmp = self.translate(tmp,model['romance2en'][0],model['romance2en'][1])#translate back to English
            response.add(tmp)

            # Translate Arabic => German = > English
            tmp = self.translate(utterance,model['en2ar'][0],model['en2ar'][1])#translate to Arabic
            tmp = get_easynmt_translation( tmp, model['easy_nmt'], 'de', 'ar') # translate to German with EasyNMt 
            tmp = self.translate(tmp,model['de2en'][0],model['de2en'][1])#translate back to English
            response.add(tmp)

            # Translate Chinese => German = > English
            tmp = self.translate(utterance,model['en2zh'][0],model['en2zh'][1])#translate to Chinese
            tmp = get_easynmt_translation( tmp, model['easy_nmt'], 'de', 'zh') # translate to German with EasyNMt 
            tmp = self.translate(tmp,model['de2en'][0],model['de2en'][1])#translate back to English
            response.add(tmp)

            # Translate German => Arabic = > English
            tmp = self.translate(utterance,model['en2de'][0],model['en2de'][1])#translate to German
            tmp = get_easynmt_translation( tmp, model['easy_nmt'], 'ar', 'de') # translate to Arabic with EasyNMt 
            tmp = get_easynmt_translation( tmp, model['easy_nmt'], 'en', 'ar') # translate to English with EasyNMt
            response.add(tmp)

            # Translate German => Chinese = > English
            tmp = self.translate(utterance,model['en2de'][0],model['en2de'][1])#translate to German
            tmp = get_easynmt_translation( tmp, model['easy_nmt'], 'zh', 'de') # translate to Chinese with EasyNMt 
            tmp = self.translate(tmp,model['zh2en'][0],model['zh2en'][1])# translate back to English
            response.add(tmp)

            # Translate German => Japanese = > English
            tmp = self.translate(utterance,model['en2de'][0],model['en2de'][1])#translate to German
            tmp = get_easynmt_translation( tmp, model['easy_nmt'], 'ja', 'de') # translate to Chinese with EasyNMt 
            tmp = get_easynmt_translation( tmp, model['easy_nmt'], 'en', 'ja') # translate to English with EasyNMt 
            response.add(tmp)

        return list(response)

    def translate_list(self,sentences,model):
        """
        Translate a List of sentences
        :param sentences: reference sentences to paraprhases in Python List, list of refenrence sentences
        :param model_list: dictionary containing marianMT model, key: model name - value: list containing respectively  Model and tokenizer.  e.g. {'en2ROMANCE':[model,tekenizer]}
        :return Python dictionary containing translsation, Key are initial sentence and vaule are a set of translations
        """

        paraphrases = dict()
        for sentence in sentences:
            tmp = self.multi_translate(sentence,model,self.pivot_level)
            paraphrases[sentence]=tmp
        
        return paraphrases

    def get_model(self,param):
        """
        Load Hugginface marian Machine Translator model and tokenizer
        :param param: Huggingface MarianMt Helsinki-NLP/{model_name} to load (https://huggingface.co/Helsinki-NLP); param[0]=label - param[1]=model_name
        :return a tuple result = (Huggingface MarianMt Model, Marian MT Tokenizer, Marian MT label)
        """

        mt_model = MarianMTModel.from_pretrained(param[1]) #param[0]=label ; param[1]=model_name to load
        mt_tokenizer = MarianTokenizer.from_pretrained(param[1]) #load tokenizer
        return mt_model,mt_tokenizer,param[0]

    def concurrent_model_loader(self):
        """
        Return a List of Huggingface Marian MT model, same as load_model but load concurrently
        :return Python dictionary - key: model name - value: list containing respectively MarianModel and MarianTokenizer e.g. {'en2ru':[model,tokenizer]}
        """
        response = dict()

        pr_gray("Load Huggingface MarianMT models")

        # load HuggingFace Marian MT model and tokenizer concurrently through thread 
        with concurrent.futures.ThreadPoolExecutor() as executor:

            # results = [executor.submit(get_model2,model_name) for model_name in models_to_load.values()]
            results = executor.map( self.get_model, HUGGINGFACE_MARIANMT_MODELS_TO_LOAD )

            # unpack and add MarianMT model, MarianMT tokenizer and label
            for model,tokenizer,label in results:
                response[label] = [model,tokenizer]
            
            pr_green("... done")
        
        #load EasyNMT nodel
        pr_gray("Load UKPLab Easy-NMT model")

        easy_model = load_easynmt_model( EASYNMT_MODEL_NAME )
        response['easy_nmt'] = easy_model

        pr_green("... done")

        return response


# if __name__ == '__main__':
#     import json
#     from TestRunner import convert_to_snake_case

#     tf = MultiPivotParaphrasesGeneration()

#     sentences = ['How does COVID-19 spread?',
#         'Book a flight from Lyon to Sydney?',
#         'Reserve an Italian Restaurant near Paris',
#         'how many 10 euros are worth in dollars',
#         'which company makes the ipod?',
#         'what states does the connecticut river flow through?',
#         'in which tournaments did west indies cricket team win the championship?']
    
#     pr_gray("Start paraphrases Generation:")

#     test_cases = []
#     for sentence in sentences:
#         test_cases.append({
#             "class": tf.name(),
#             "inputs": {"Reference sentence": sentence}, "outputs": [{"Paraphrase": o} for o in tf.generate(sentence)]}
#         )
    
#     pr_green("... done")

#     json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
    
#     print(json.dumps(json_file, indent=2))
