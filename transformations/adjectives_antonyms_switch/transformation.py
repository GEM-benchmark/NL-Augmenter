import spacy
from nltk import download
from nltk.corpus import wordnet
from nltk.data import find

from initialize import spacy_nlp
from interfaces.SentenceOperation import SentenceOperation
from interfaces.SentencePairOperation import SentencePairOperation
from tasks.TaskTypes import TaskType

"""
Adjectives Antonyms Switch.
    Change adjectives for their antonyms generating a sentence with oposite meaning.
"""


def adjectives_antonyms_switch(sentence, nlp):

    # Tokenize Sentence
    doc = nlp(sentence)

    # Initialize Variables
    changed = False
    new_sentence = []

    # Evaluate Tokens
    for token in doc:
        # Add Token to Output Sentence
        new_sentence.append(token)

        # Initialize Variables
        synsets = []
        antonyms = []

        # Get Synset
        if token.pos_ == "ADJ":
            synsets = wordnet.synsets(token.lemma_, "a")
            synsets = [s for s in synsets if ".a." in s.name()]

        # Get Antonyms
        if synsets:
            first_synset = synsets[0]
            lemmas = first_synset.lemmas()
            first_lemma = lemmas[0]
            antonyms = first_lemma.antonyms()

        # Get first Antonym
        if antonyms:
            antonyms.sort(key=lambda x: str(x).split(".")[2])
            first_antonym = antonyms[0].name() + token.whitespace_
            antonym_token = nlp(first_antonym)[0]
            new_sentence[-1] = antonym_token
            changed = True

    # Rebuild Sentence
    new_sentence = [t.text + t.whitespace_ for t in new_sentence]
    new_sentence = "".join(new_sentence)

    return (new_sentence, changed)


class SentenceAdjectivesAntonymsSwitch(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]
    keywords = ["lexical", "rule-based", "external-knowledge-based", "near-accurate", "natural-sounding", "natural-looking"]

    def __init__(self, seed=0, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)
        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")
        try:
            find("corpora/wordnet")
        except LookupError:
            download("wordnet")
            global wordnet
            from nltk.corpus import wordnet

    def generate(self, sentence: str):

        # Initialize Variables
        output_sentence = sentence

        new_sentence, changed = adjectives_antonyms_switch(sentence, self.nlp)

        if changed:
            output_sentence = new_sentence

        return [output_sentence]


class PairAdjectivesAntonymsSwitch(SentencePairOperation):
    tasks = [TaskType.PARAPHRASE_DETECTION]
    languages = ["en"]
    keywords = ["lexical", "rule-based", "external-knowledge-based", "near-accurate", "natural-sounding", "natural-looking"]

    def __init__(self, seed=0, max_outputs=3, pos_label="1", neg_label="0"):
        super().__init__(seed, max_outputs=max_outputs)
        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")
        try:
            find("corpora/wordnet")
        except LookupError:
            download("wordnet")
            global wordnet
            from nltk.corpus import wordnet
        self.pos_label = pos_label
        self.neg_label = neg_label

    def generate(self, sentence1: str, sentence2: str, target: str):

        # Initialize Variables
        output_sentences = []
        changed_sentences = {}

        # Only process equivalent pairs
        if target == self.pos_label:

            for n, sentence in enumerate([sentence1, sentence2]):
                new_sentence, changed = adjectives_antonyms_switch(
                    sentence, self.nlp
                )
                if changed:
                    changed_sentences[n] = new_sentence

        if 0 in changed_sentences.keys() and changed_sentences[0] != sentence2:
            output_sentences.append(
                (changed_sentences[0], sentence2, self.neg_label)
            )

        if 1 in changed_sentences.keys() and sentence1 != changed_sentences[1]:
            output_sentences.append(
                (sentence1, changed_sentences[1], self.neg_label)
            )

        if (
            0 in changed_sentences.keys()
            and 1 in changed_sentences.keys()
            and changed_sentences[0] != changed_sentences[1]
        ):
            output_sentences.append(
                (changed_sentences[0], changed_sentences[1], self.pos_label)
            )

        if not output_sentences:
            output_sentences = [(sentence1, sentence2, target)]

        return output_sentences


"""
# Sample code to demonstrate usage. Can also assist in adding test cases.
# You don't need to keep this code in your transformation.
if __name__ == '__main__':
    import json
    from TestRunner import convert_to_snake_case
    tf = SentenceAdjectivesAntonymsSwitch()
    test_cases = []
    for sentence in ["Anthony was a very tall boy.",
                     "Amanda's mother was very beautiful.",
                     "After the war he had become a rich man.",
                     "Creating that sort of machinery required a very talented engineer.",
                     "It was very foolish to start working right away."]:
        test_cases.append({
            "class": tf.name(),
            "inputs": {"sentence": sentence},
            "outputs": [{"sentence": o[0]} for o in tf.generate(sentence)]}
        )
    json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
    print(json.dumps(json_file))
    tf = PairAdjectivesAntonymsSwitch(max_outputs=3)
    test_cases = []
    for sentence1, sentence2, target in zip([ "Anthony was a very tall boy.",
                                     "Amanda's mother was very beautiful.",
                                     "After the war he had become a rich man.",
                                     "Creating that sort of machinery required a very talented engineer.",
                                     "It was very foolish to start working right away."],
                                    ["He was a very big guy.",
                                     "Her mother was a good looking woman.",
                                     "Thomas became very rich once the war was over.",
                                     "You had to be very skillfull to make such a machine.",
                                     "To sit there doing nothing was very stupid."],
                                     ["1",
                                      "1",
                                      "1",
                                      "1",
                                      "1"
                                     ]
                                    ):
        test_cases.append({
            "class": tf.name(),
            "inputs": {"sentence1": sentence1, "sentence2": sentence2, "target": target},
            "outputs": [{"sentence1": o[0], "sentence2": o[1], "target": o[2]} for o in tf.generate(sentence1, sentence2, target)]}
        )
    json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
    print(json.dumps(json_file))
"""
