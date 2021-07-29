import spacy

from initialize import spacy_nlp
from interfaces.SentenceOperation import SentenceOperation
from interfaces.SentencePairOperation import SentencePairOperation
from tasks.TaskTypes import TaskType

"""
Auxiliary Negation Removal.
    Remove auxiliary negations generating a sentence with oposite meaning.
"""


def auxiliary_negation_removal(sentence, nlp):

    # Tokenize Sentence
    doc = nlp(sentence)

    # Initialize Variables
    changed = False
    new_sentence = []
    supported_auxiliaries = [
        "am",
        "are",
        "can",
        "could",
        "had",
        "has",
        "have",
        "is",
        "may",
        "might",
        "must",
        "shall",
        "should",
        "was",
        "were",
        "will",
        "would",
    ]

    # Evaluate Tokens
    for token in doc:
        # Add Token to Output Sentence
        new_sentence.append(token)

        # Initialize Variables
        token_lowercased_lemma = token.lemma_.lower()

        # Process Negations
        if token_lowercased_lemma == "not" or token_lowercased_lemma == "n't":
            # Get not position
            not_index = token.i

            # Process Auxiliaries
            if not_index > 0:

                # Get Previous Token
                previous_index = not_index - 1
                previous_token = doc[previous_index]
                previous_surface = previous_token.text
                previous_lowercase_surface = previous_surface.lower()

                # Remove Negation
                if previous_lowercase_surface in supported_auxiliaries:
                    new_sentence = new_sentence[:-1]
                    changed = True

                elif previous_lowercase_surface in ["do"]:
                    new_sentence = new_sentence[:-2]
                    changed = True

                # Handle Spacing
                if (
                    token_lowercased_lemma == "n't"
                    and changed
                    and new_sentence
                ):
                    new_sentence[-1] = nlp(
                        new_sentence[-1].text + token.whitespace_
                    )[0]

    # Rebuild Sentence
    new_sentence = [t.text + t.whitespace_ for t in new_sentence]
    new_sentence = "".join(new_sentence)

    return (new_sentence, changed)


class SentenceAuxiliaryNegationRemoval(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]

    def __init__(self, seed=0, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)
        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")

    def generate(self, sentence: str):

        # Initialize Variables
        output_sentence = sentence

        # Process sentence
        new_sentence, changed = auxiliary_negation_removal(sentence, self.nlp)

        if changed:
            output_sentence = new_sentence

        return [output_sentence]


class PairAuxiliaryNegationRemoval(SentencePairOperation):
    tasks = [TaskType.PARAPHRASE_DETECTION]
    languages = ["en"]

    def __init__(self, seed=0, max_outputs=3, pos_label="1", neg_label="0"):
        super().__init__(seed, max_outputs=max_outputs)
        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")
        self.pos_label = pos_label
        self.neg_label = neg_label

    def generate(self, sentence1: str, sentence2: str, target: str):

        # Initialize Variables
        output_sentences = []
        changed_sentences = {}

        # Only process equivalent pairs
        if target == self.pos_label:

            for n, sentence in enumerate([sentence1, sentence2]):
                # Process sentence
                new_sentence, changed = auxiliary_negation_removal(
                    sentence, self.nlp
                )
                if changed:
                    changed_sentences[n] = new_sentence

        if 0 in changed_sentences.keys():
            output_sentences.append(
                (changed_sentences[0], sentence2, self.neg_label)
            )

        if 1 in changed_sentences.keys():
            output_sentences.append(
                (sentence1, changed_sentences[1], self.neg_label)
            )

        if 0 in changed_sentences.keys() and 1 in changed_sentences.keys():
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
    tf = SentenceAuxiliaryNegationRemoval()
    test_cases = []
    for sentence["Andrew has not returned the French book to the library.",
                 "Sentences with gapping, such as Paul likes coffee and Mary tea, do not have an overt predicate.",
                 "Alice in Wonderland isn't a 1997 American live-action/animated dark fantasy adventure film.",
                 "Ujjal Dev Dosanjh was not the 1st Premier of British Columbia from 1871 to 1872.",
                 "The fighters would not give up."]:
        test_cases.append({
            "class": tf.name(),
            "inputs": {"sentence": sentence},
            "outputs": [{"sentence": o[0]} for o in tf.generate(sentence)]}
        )
    json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
    print(json.dumps(json_file))
    tf = PairAuxiliaryNegationRemoval(max_outputs=3)
    test_cases = []
    for sentence1, sentence2, target in zip(["Andrew has not returned the French book to the library.",
                                     "Sentences with gapping, such as Paul likes coffee and Mary tea, do not have an overt predicate.",
                                     "Alice in Wonderland isn't a 1997 American live-action/animated dark fantasy adventure film.",
                                     "Ujjal Dev Dosanjh was not the 1st Premier of British Columbia from 1871 to 1872.",
                                     "The fighters would not give up."],
                                    ["He hasn't brought back the library's books.",
                                     "Gapping sentences, such as Paul likes coffee and Mary tea, lack an overt predicate.",
                                     "Alice in Wonderland is not an American animated, dark fantasy adventure film from 1997.",
                                     "U.D. Dosanjh wasn't the 1st Premier of British Columbia for a year from 1871.",
                                     "The warriors wouldn't leave the battlefield."],
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
