import itertools
import random
import spacy
import os


from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
from initialize import spacy_nlp

"""
Base Class for implementing the different input transformations a generation should be robust against.
"""


def slangifyPoS(
    token, modified_toks, Dictionary, PoS, probReplace, isCap, ReplPot, ReplMade
):  # performs transformation similar to all three PoS

    # Check if word is in the corresponding dictionary
    if token.lemma_ in Dictionary[0]:
        ReplPot += 1  # increment potential replacements

        repDecision = (
            random.uniform(0, 1) <= probReplace
        )  # Randomly decide whether to replace or not

        if repDecision:  # if replacement is made
            ReplMade += 1

            # Choose a new word for replacement
            # ind=Slang_Adverbs[0].index(token.lemma_)
            indAllPosRepl = [
                i for i, x in enumerate(Dictionary[0]) if x == token.lemma_
            ]  # all possible replacements
            indChosenRepl = random.randint(
                0, len(indAllPosRepl) - 1
            )  # choose one of the replacements
            indChosenRepl = indAllPosRepl[indChosenRepl]  # index of that replacement

            if PoS == "Noun":  # Treat plular case for nouns
                # Take plural or singular form. Note only for nouns
                if token.tag_ == "NN" or token.tag_ == "NNP":
                    temp = Dictionary[1][
                        indChosenRepl
                    ]  # pick the word chosen for replcacement
                else:
                    temp = Dictionary[2][
                        indChosenRepl
                    ]  # pick the word chosen for replcacement
            else:
                temp = Dictionary[1][
                    indChosenRepl
                ]  # pick the word chosen for replcacement

            if isCap:  # Make the fist letter capital if necessary
                temp = temp[0].upper() + temp[1:]

            modified_toks.append(temp + token.whitespace_)

        else:  # if no replacement is made
            modified_toks.append(token.text + token.whitespace_)

    else:  # if not in the dictionary
        modified_toks.append(token.text + token.whitespace_)


def slangify(
    self,
    text,
    probReplaceNoun=0.5,
    probReplaceAdjective=0.5,
    probReplaceAdverb=0.5,
    seed=0,
    max_outputs=1,
):
    random.seed(seed)

    nlp = self.nlp  # get an instance of the tokenizer
    perturbed_texts = []  # output for all perturbed texts

    # Load dictionaries
    Slang_Nouns = self.Slang_Nouns
    Slang_Nouns = list(map(list, zip(*Slang_Nouns)))
    Slang_Adverbs = self.Slang_Adverbs
    Slang_Adverbs = list(map(list, zip(*Slang_Adverbs)))
    Slang_Adjectives = self.Slang_Adjectives
    Slang_Adjectives = list(map(list, zip(*Slang_Adjectives)))

    # Tags for nouns
    noun_tag = ["NN", "NNS", "NNPS", "NNP"]

    # Tokenize text
    doc = nlp(text)

    for _ in itertools.repeat(None, max_outputs):

        ReplPot = 0  # counts potential replcacements, which could have been made if the probability of replacement would be set to one for all PoS
        ReplMade = 0  # counts actual replcacements

        modified_toks = []  # modified tokens
        for token in doc:
            isCap = token.text[
                0
            ].isupper()  # check if token begins with the capital letter

            # Nouns
            if token.tag_ in noun_tag:
                slangifyPoS(
                    token,
                    modified_toks,
                    Slang_Nouns,
                    "Noun",
                    probReplaceNoun,
                    isCap,
                    ReplPot,
                    ReplMade,
                )

            # Adverbs
            elif token.tag_ == "RB":
                slangifyPoS(
                    token,
                    modified_toks,
                    Slang_Adverbs,
                    "Adverb",
                    probReplaceAdverb,
                    isCap,
                    ReplPot,
                    ReplMade,
                )

            # Adjectives
            elif token.tag_ == "JJ":
                slangifyPoS(
                    token,
                    modified_toks,
                    Slang_Adjectives,
                    "Adjective",
                    probReplaceAdjective,
                    isCap,
                    ReplPot,
                    ReplMade,
                )

            else:  # if there is no part of speech which might be replaced then just keep the original one
                modified_toks.append(token.text + token.whitespace_)

        modified_toks = "".join(modified_toks)  # Reconstruct the transformed text

        perturbed_texts.append(modified_toks)

    return perturbed_texts


class Slangificator(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["en"]
    keywords = [
        "lexical",
        "rule-based",
        "external-knowledge-based",
        "tokenizer-required",
        "possible-meaning-alteration",
    ]

    def __init__(self, seed=0, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)

        pathDic = os.path.dirname(os.path.abspath(__file__))

        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")  # get an instance of the tokenizer

        # Load dictionaries
        self.Slang_Nouns = [
            line.strip("\n\r").split(",")
            for line in open(os.path.join(pathDic, "Slang_Nouns.txt"), "r")
        ]
        self.Slang_Adverbs = [
            line.strip("\n\r").split(",")
            for line in open(os.path.join(pathDic, "Slang_Adverbs.txt"), "r")
        ]
        self.Slang_Adjectives = [
            line.strip("\n\r").split(",")
            for line in open(os.path.join(pathDic, "Slang_Adjectives.txt"), "r")
        ]

    def generate(self, sentence: str):

        perturbed_texts = slangify(
            self,
            text=sentence,
            probReplaceNoun=1.0,
            probReplaceAdjective=1.0,
            probReplaceAdverb=1.0,
            seed=self.seed,
            max_outputs=self.max_outputs,
        )
        return perturbed_texts


"""
# Sample code to demonstrate usage. Can also assist in adding test cases.
# You don't need to keep this code in your transformation.
if __name__ == '__main__':
    import json
    from TestRunner import convert_to_snake_case

    tf = ButterFingersPerturbation(max_outputs=3)
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
"""
