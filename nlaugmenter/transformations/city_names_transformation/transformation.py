import hashlib
import os
import random

import spacy

from nlaugmenter.common.initialize import spacy_nlp
from nlaugmenter.interfaces.SentenceOperation import SentenceOperation
from nlaugmenter.tasks.TaskTypes import TaskType


def hash(input: str):
    """
    Function to hash a sentence

    Parameters
    ----------
    input : str
        Input sentence to hash.

    Returns
    -------
    n : int
        Hashed value of the sentence.

    """
    t_value = input.encode("utf8")
    h = hashlib.sha256(t_value)
    n = int(h.hexdigest(), base=16)
    return n


"""
ChangeCityNames is a class that will take in a list of tokens from a SpaCy document object and will replace instances of popular cities with instances
of less populous cities to test the robustness of NER models.
"""


class ChangeCityNames:
    def __init__(self, data_path, language="en"):
        """
        Constructor for ChangeCityNames object.

        Parameters
        ----------
        data_path : str
            path to the .csv file with populous cities and sacrcely populous cities.
        language : str, optional
            language you are testing on. The default is "en".

        Returns
        -------
        None.

        """
        self.language = language
        if language == "en":
            f_pop = open(os.path.join(data_path, "Eng_Pop.txt"))
            f_scarce = open(os.path.join(data_path, "Eng_Scarce.txt"))
        else:
            f_pop = open(os.path.join(data_path, "Esp_Pop.txt"))
            f_scarce = open(os.path.join(data_path, "Esp_Scarce.txt"))
        self.populous_cities = f_pop.read().split("\n")
        self.scarce_cities = f_scarce.read().split("\n")

    def iob_ent_dict(self, doc):
        """
        Given a spaCy Doc object, this creates a list of dictionaries mapping each token to its text, IOB embedding, and entity

        Parameters
        ----------
        doc : SpaCy Doc
            SpaCy doc object outputted by spaCy model.

        Returns
        -------
        d : list<dict>
            List of dictionaries mapping each token in a Doc object to its text, IOB embedding, and entity.

        """
        d = []
        for i in doc:
            d.append({"Word": i.text, "IOB": i.ent_iob_, "Ent": i.ent_type_})
        return d

    def create_ents_dict(self, doc):
        """
        Given a SpaCy Doc object, this creates a list of dictionaries that maps a span of words to its entity

        Parameters
        ----------
        doc : SpaCy Doc
            SpaCy Doc object ouputted from spaCy model.

        Returns
        -------
        spans : list<dict>
            a list of dictionaries that maps a span of words to its entity.

        """
        spans = []
        ind = 0
        d = self.iob_ent_dict(doc)
        while ind < len(d):
            span = ""
            ent = ""
            if d[ind]["IOB"] == "O":
                span += d[ind]["Word"]
                ind += 1
            elif d[ind]["IOB"] == "B":
                ent = d[ind]["Ent"]
                span += d[ind]["Word"]
                ind += 1
                while ind < len(d) and d[ind]["IOB"] == "I":
                    span += " " + d[ind]["Word"]
                    ind += 1
            spans.append({"Word": span, "Entity": ent})
        return spans

    def transform(self, doc, seed=None):
        """
        Given a SpaCy doc object, this returns a sentence string that replaces populous cities with less populous/well-known cities

        Parameters
        ----------
        doc : SpaCy Doc
            SpaCy doc object that is ouputted from a SpaCy model given an input sentence.
        seed : int, optional
            seed value for random operations. The default is None.

        Returns
        -------
        new_sentence : str
            The transformed sentence.

        """
        if seed is not None:
            random.seed(seed)
        ents_dict = self.create_ents_dict(doc)
        sent_words = []
        for i in ents_dict:
            if i["Word"] in list(self.populous_cities) and (
                i["Entity"] == "GPE" or i["Entity"] == "LOC"
            ):
                sent_words.append("<CITY>")
            else:
                sent_words.append(i["Word"])
        new_sentence = " ".join(sent_words)
        while "<CITY>" in new_sentence:
            rand_city = self.scarce_cities[
                random.randint(0, len(self.scarce_cities))
            ]
            new_sentence = new_sentence.replace("<CITY>", rand_city, 1)
        return new_sentence


"""
CityNamesTransformation is a class that inherits from the SentenceOperation interface.
This class's main purpose is to take an input sentence that contains a populous city and replace the instance of that city with a new city that is
not as populous or well-known to test the robustness of NLP models.
"""


class CityNamesTransformation(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TAGGING]
    languages = ["en", "es"]
    heavy = True
    keywords = [
        "lexical",
        "model-based",
        "tokenizer-required",
        "highly-meaning-preserving",
        "high-precision",
        "low-coverage",
        "high-generations",
        "world-knowledge",
    ]

    def __init__(self, seed=0, max_outputs=1, lang="en", data_path=None):
        """
        Constructor of the CityNamesTransformation object in a given language

        Parameters
        ----------
        seed : int, optional
            seed value for random operations. The default is 0.
        max_outputs : 1, optional
            How many ouput sentences can be created by an operation. The default is 1.
        lang : str, optional
            What language you want to perform the operation on. The default is "en".
        data_path : str, optional
            data path of database of English and Spanish cities. The default is None.

        Returns
        -------
        None.

        """
        super().__init__(seed, max_outputs=max_outputs)
        self.model = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")
        if lang == "en":
            if data_path is None:
                self.transformer = ChangeCityNames(
                    os.path.dirname(os.path.abspath(__file__)), language="en"
                )
            else:
                self.transformer = ChangeCityNames(data_path, language="en")
        else:
            if data_path is None:
                self.transformer = ChangeCityNames(
                    os.path.dirname(os.path.abspath(__file__)), language="es"
                )
            else:
                self.transformer = ChangeCityNames(data_path, language="es")

    def generate(self, sentence: str):
        """
        Given an input sentence, creates a new transformed sentence. The input sentence should have at least one popular city, and the
        transformed sentence will replace these instances with less popular cities.

        Parameters
        ----------
        sentence : str
            Input sentence.

        Returns
        -------
        list
            Transformed sentence.

        """
        seed = self.seed + hash(sentence)
        doc = self.model(sentence)
        perturbed_text = self.transformer.transform(doc, seed=seed)
        return [perturbed_text]


"""
# Sample code to demonstrate usage. Can also assist in adding test cases.
# You don't need to keep this code in your transformation.
if __name__ == '__main__':
    import json
    from TestRunner import convert_to_snake_case

    tf = CityNamesTransformation(max_outputs=3)
    # sentence = "Andrew finally returned the French book to Chris that I bought last week"
    test_cases = []
    for sentence in ["Jarry returned to London and applied himself to drinking, writing, and the company of friends who appreciated his witty, sweet-tempered, and unpredictable conversation.",
                     "The team was established in Dallas in 1898 and was a charter member of the NFL in 1920.",
                     "The Falcons had their first Monday Night Football game in Los Angeles during the 1970 season.",
                     "In the event, Manchester was chosen instead of Miami, owing to political circumstances.",
                     "In 1841, Sax relocated permanently to Boston and began work on a new set of instruments which were exhibited there in 1844."]:
        # print(tf.generate(sentence))
        test_cases.append({
            "class": tf.name(),
            "inputs": {"sentence": sentence}, "outputs": [{"sentence": o} for o in tf.generate(sentence)]}
        )
    json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
    print(json.dumps(json_file))
"""
