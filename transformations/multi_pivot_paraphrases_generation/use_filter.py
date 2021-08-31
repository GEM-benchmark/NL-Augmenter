import tensorflow_hub as hub
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

""" Remove semantically unrelated paraphrases by computing Universal Sentence Encoder embeddings cosine similiraity score """

def load_use_model(model_name="https://tfhub.dev/google/universal-sentence-encoder-large/5"):
    """
    Load Universal Sentence Encoder model
    :param model_name: name of the USE model to load
    :return an USE model
    """
    
    model = hub.load(model_name)
    return model


def get_use_embedding(paraphrases_list, embed, reference_sentence):
    """
    Get Universal Sentence Encoder embeddings
    :param paraphrases_list: python list on which to apply embedding, Key initial sentence and value is a set of paraphrases
    :param embed: Universal Sentence Encoder model instance
    :param reference_sentence: reference sentence with which the paraphrases are compared
    :return a python dictionary whre not semantically unrelated paraphrases are removed
    """

    response = set()
    key_embedding = embed([reference_sentence]) #initial sentence USE embedding
    a=np.reshape(key_embedding,(1,-1))

    for candidate in paraphrases_list:
        candidate_embedding = embed([candidate]) #candidate parpahrase USE embedding
        b=np.reshape(candidate_embedding,(1,-1))
        cos_lib = cosine_similarity(a,b)
        b = 0
        if cos_lib > 0.5:
            response.add(candidate)

    return response

def test():
    print("Load USE ")
    embed = load_model("https://tfhub.dev/google/universal-sentence-encoder-large/5")
    print("... done")

    d = {'how does covid-19 spread':["how does it spread","book a flight from lyon to sydney",'i feel cold']}
    r = get_embedding(d,embed)
    print(r)

if __name__ == '__main__':
    test()