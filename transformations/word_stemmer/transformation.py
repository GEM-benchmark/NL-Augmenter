import re

from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
from nltk.stem.snowball import SnowballStemmer

from nltk.tokenize import sent_tokenize, word_tokenize

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

porter = PorterStemmer()

def stem_text(text, max_outputs = 1):
    tokenized_text = word_tokenize(text)
    stemmed = [porter.stem(word) for word in word_tokenize(raw_text)]
    
    detokenized_text = " ".join(stemmed)
    res_text = re.sub(r'\s([?,.!"](?:\s|$))', r'\1', detokenized_text)
    
    return res

class SimpleWordStemmer(SentenceOperation):
    """
    This class offers method for applying a simple word stemmer to transform
    the text. Stemming is the process of producing morphological variants of 
    a root/base word.

    For example: 
    A word stemmer reduces the words “chocolates”, “chocolatey”, “choco” to 
    the root word, “chocolate” and “retrieval”, “retrieved”, “retrieves” reduce 
    to the stem “retrieve”.
    
    Attributes:

    """
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
    ]
    languages = ["en"]
    heavy = True

    def __init__(self, seed = 0, max_outputs = 1):
        super().__init__(seed, max_outputs =  max_outputs)

    def generate(self, raw_text: str):
        pertubed_text = stem_text(
            text = raw_text,
            max_outputs = self.max_outputs
        )

        return pertubed_text

'''
# Sample code to demonstrate:

if __name__ == '__main__':
    import json
    from TestRunner import convert_to_snake_case
    tf = SimpleWordStemmer(max_outputs = 1)
    sentence = "Andrew finally returned the French book to Chris that I bought last week"
    test_cases = []
    for sentence in ["Andrew finally returned the French book to Chris that I bought last week",
                     "Sentences with gapping, such as Paul likes coffee and Mary tea, lack an overt predicate to indicate the relation between two or more arguments.",
                     "Alice in Wonderland is a 2010 American live-action/animated dark fantasy adventure film",
                     "Ujjal Dev Dosanjh served as 33rd Premier of British Columbia from 2000 to 2001",
                     "Neuroplasticity is a continuous processing allowing short-term, medium-term, and long-term remodeling of the neuronosynaptic organization."]:
        test_cases.append({
            "class": tf.name(),
            "inputs": {"sentence": sentence}, "outputs": [{"sentence": o} for o in tf.generate(sentence)]}
        )
    json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
    print(json.dumps(json_file))
'''