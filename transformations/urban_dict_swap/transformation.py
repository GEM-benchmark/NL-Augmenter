import random

import requests
import spacy
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from initialize import spacy_nlp
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


class UrbanThesaurusSwap(SentenceOperation):
    """
    Randomly swap nouns from the input text for related terms from the Urban Dictionary.

    Attributes
    ----------
    seed : int
        Seed to initialize random generation.
    prob : float
        Probability of transforming each noun.
    min_score: float
        Minimum relevancy score returned from API to consider as related term.
    max_outputs: int
        Maximum number of output sequences to return.

    Methods
    -------
    generate(sentence):
        Generates transformed output sequences for input sentence.
    """

    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["en"]
    keywords = ["lexical", "api-based", "unnaturally-written", "possible-meaning-alteration", "high-precision",
                "high-coverage", "figurative-language"]

    retry_strategy = Retry(
        total=3,
        status_forcelist=[429, 500, 502, 503, 504],
        method_whitelist=["HEAD", "GET", "OPTIONS"],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)

    def __init__(self, seed=0, prob=0.5, min_score=100.0, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)
        self.seed = seed
        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")
        self.prob = prob
        self.min_score = min_score
        self.max_outputs = max_outputs
        self.url = "https://urbanthesaurus.org/api/related?term="

    def filter(self, sentence: str) -> bool:
        pass

    def generate(self, sentence: str):
        """
        Return transformed input sequence.
        @param sentence: Original input sequence
        @return: List of transformed output sequences
        """
        perturbed_texts = self.__get_swap(text=sentence)
        return perturbed_texts

    def __get_swap(self, text: str):
        """
        Iterate through input sequence, obtain related terms for nouns from API
        @param text: Input sequence
        @return: List of transformed output sequences
        """
        random.seed(self.seed)
        results = []
        for _ in range(self.max_outputs):
            new_text = []
            for token in self.nlp(text):
                if token.pos_ == "NOUN" and random.random() < self.prob:
                    r = requests.get(self.url + token.text)
                    if r.status_code == 200:
                        doc = r.json()
                        new_items = []
                        for item in doc:
                            if isinstance(item, dict):
                                if "score" in item.keys():
                                    if float(item["score"]) > self.min_score:
                                        new_items.append(item)
                        if len(new_items) > 0:
                            new_text.append(random.choice(new_items)["word"])
                        else:
                            new_text.append(token.text)
                    else:
                        new_text.append(token.text)
                else:
                    new_text.append(token.text)
            results.append(" ".join(new_text))
        return results
