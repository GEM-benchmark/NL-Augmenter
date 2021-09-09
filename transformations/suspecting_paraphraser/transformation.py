from typing import List, Tuple

from gender_extractor import GenderExtractor
import nltk
import numpy as np

# Spacy needs this module, but it's used only implicitly
import pyinflect  # noqa: F401
import spacy

from initialize import spacy_nlp
from interfaces.QuestionAnswerOperation import QuestionAnswerOperation
from tasks.TaskTypes import TaskType

"""
Base Class for implementing the different input transformations a generation should be robust against.
"""


class SuspectingParaphraser(QuestionAnswerOperation):
    """ This paraphraser transforms a yes/no question into a tag one.
     
    Example: "Did the American National Shipment company really break its own fleet?" 
    -> "The American National Shipment company really broke its own fleet, didn't it?"
    """
    tasks = [TaskType.QUESTION_ANSWERING, TaskType.QUESTION_GENERATION]

    languages = ["en"]

    def __init__(self, seed=0, max_outputs=1, pronoun_mod=0.9):
        super().__init__(seed, max_outputs=max_outputs)
        np.random.seed(seed)
        nltk.download("punkt")

        self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")

        self.gender_detector = GenderExtractor()
        self.pronouns = ["he", "she", "it", "they"]
        self.static_pronouns = ["i", "we", "you", *self.pronouns]

        self._special_endings = {
            "may": "may {} not",
            "might": "might {} not",
            "shall": "shan't {}",
            "will": "won't {}",
        }

        self.pronoun_mod = pronoun_mod
        self._pronoun_alt = (1 - pronoun_mod) / (len(self.pronouns) - 1)

    def _transform(self, question):
        text = nltk.word_tokenize(question)
        doc = self.nlp(question)
        modal = str(doc[0]).lower()
        token = doc[0]

        verb_position = [
            i for i in range(len(doc)) if str(doc[i]) == token.head.text
        ][0]

        rest_of_sentence = [i for i in text[verb_position:]]

        if text[1].lower() == "n't":
            text = text[1:]
            doc = doc[1:]
            verb_position = verb_position - 1

        beginning = [text[1].capitalize()]
        beginning.extend(text[2:verb_position])
        sentence = nltk.tokenize.treebank.TreebankWordDetokenizer().detokenize(
            beginning + rest_of_sentence
        )

        first_verb = doc[verb_position]

        # If 'did' is our modal, the verb will be in a present tense
        # It means that we need to inflect it to the past one (VBD)
        # (Did John _drink_ my tea? -> John _drank_ my tea, didn't he?)
        # Otherwise, the verb is already in a good form and we can use
        # it directly
        if modal == "did":
            demodded = first_verb._.inflect("VBD")
        else:
            demodded = modal + " " + str(first_verb)
        sentence = sentence.replace(str(first_verb), str(demodded)).replace(
            "?", ""
        )

        ending = self._resolve_ending(doc, modal)
        result = sentence + ending
        return result

    def _resolve_ending(self, doc, modal):
        try:
            subject = str([tok for tok in doc if (tok.dep_ == "nsubj")][0])
        except IndexError:
            return ", right?"

        prob = {i: 1 / len(self.pronouns) for i in self.pronouns}

        tagged = [(X.text, X.label_) for X in doc.ents]
        if subject.lower() in self.static_pronouns:
            pronoun = subject.lower()
            if pronoun == "i":
                pronoun = "I"
        else:
            if len(tagged) > 0 and tagged[0][1] != "PERSON":
                prob = {i: 0 for i in self.pronouns}
                prob["it"] = 1
            else:
                noun_gender = self.gender_detector.extract_gender(subject)

                if noun_gender in ["male", "mostly_male"]:
                    prob = {i: self._pronoun_alt for i in self.pronouns}

                    prob["he"] = self.pronoun_mod

                elif noun_gender in ["female", "mostly_female"]:
                    prob = {i: self._pronoun_alt for i in self.pronouns}

                    prob["she"] = self.pronoun_mod

            pronoun = np.random.choice(self.pronouns, p=list(prob.values()))

        ending = ", "
        if modal in self._special_endings.keys():
            ending += self._special_endings[modal].format(pronoun)
        else:
            ending += f"{modal}n't {pronoun}"
        ending += "?"
        return ending

    def _filter_phrase(self, question):
        try:
            if question.strip()[-1] != "?":
                return False
        except IndexError:
            return False

        if " or " in question:
            return False

        doc = self.nlp(question)
        token = doc[0]
        print(token, token.pos_)
        if token.pos_ != "AUX":
            return False

        return True

    def generate(
        self, context: str, question: str, answers: [str]
    ) -> List[Tuple[str, str, List[str]]]:
        if not self._filter_phrase(question):
            return [(context, question, answers)]

        paraphrased = self._transform(question)
        return [(context, paraphrased, answers)]


# if __name__ == "__main__":
#     import json

#     from TestRunner import convert_to_snake_case

#     tf = SuspectingParaphraser()

#     test_cases = []
#     for i, sentence in enumerate(
#         [
#             "Did Sally finally return the french book to Chris?",
#             "Did the American National Shipment company really break its own fleet?",
#             "Couldn't she just leave?",
#             "Shall you begone, lad?",
#             "Has Buzz Aldrin, the first person who walked on the moon, brought back some aliens?",
#         ]
#     ):
#         res = tf.generate("", sentence, [])
#         test_cases.append(
#             {
#                 "class": tf.name(),
#                 "inputs": {"context": "", "question": sentence, "answers": []},
#                 "outputs": [],
#             }
#         )

#         for p_context, p_question, p_answers in res:
#             print(sentence)
#             print(p_question)
#             print()
#             test_cases[i]["outputs"].append(
#                 {
#                     "context": p_context,
#                     "question": p_question,
#                     "answers": p_answers,
#                 }
#             )

#     json_file = {
#         "type": convert_to_snake_case(tf.name()),
#         "test_cases": test_cases,
#     }
#     print(json.dumps(json_file))
