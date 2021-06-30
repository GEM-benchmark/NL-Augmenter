from typing import Tuple, List
import nltk
from pyinflect import getInflection
import spacy
import gender_guesser.detector as gender
from enum import Enum
import numpy as np


from interfaces.QuestionAnswerOperation import QuestionAnswerOperation
from tasks.TaskTypes import TaskType

"""
Base Class for implementing the different input transformations a generation should be robust against.
"""


class Pronouns:
    HE = 0
    SHE = 1
    IT = 2
    THEY = 3


class SuspectingParaphraser(QuestionAnswerOperation):
    tasks = [TaskType.QUESTION_ANSWERING, TaskType.QUESTION_GENERATION]

    languages = ["en"]

    def __init__(self, seed=0, max_output=1, pronoun_mod=0.9):
        super().__init__(seed)
        np.random.seed(seed)
        self.seed = seed
        self.max_output = max_output

        self.nlp = spacy.load("en_core_web_sm")
        self.gender_detector = gender.Detector()
        self.pronouns = ["he", "she", "it", "they"]
        self.static_pronouns = ["i", "you", *self.pronouns]

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

        verb_position = [i for i in range(len(doc)) if str(doc[i]) == token.head.text][
            0
        ]

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
        if modal == "did":
            demodded = first_verb._.inflect("VBD")
        else:
            demodded = modal + " " + str(first_verb)
        sentence = sentence.replace(str(first_verb), str(demodded)).replace("?", "")

        ending = self._resolve_ending(doc, modal)
        result = sentence + ending
        return result

    def _resolve_ending(self, doc, modal):
        try:
            subject = str([tok for tok in doc if (tok.dep_ == "nsubj")][0])
        except IndexError:
            print(doc)
            return ", right?"

        prob = np.ones(len(self.pronouns)) / len(self.pronouns)

        tagged = [(X.text, X.label_) for X in doc.ents]
        if subject.lower() in self.static_pronouns:
            pronoun = subject.lower()
            if pronoun == "i":
                pronoun = "I"
        else:
            if len(tagged) > 0 and tagged[0][1] != "PERSON":
                prob = [0] * len(self.pronouns)
                prob[Pronouns.IT] = 1
            else:
                noun_gender = self.gender_detector.get_gender(subject)

                if noun_gender in ["male", "mostly_male"]:
                    prob = [self._pronoun_alt] * len(self.pronouns)
                    prob[Pronouns.HE] = self.pronoun_mod

                elif noun_gender in ["female", "mostly_female"]:
                    prob = [self._pronoun_alt] * len(self.pronouns)
                    prob[Pronouns.SHE] = self.pronoun_mod

            pronoun = np.random.choice(self.pronouns, p=prob)
        if modal == "have" and (pronoun in ["he", "she", "it"]):
            modal = "has"

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
        if token.pos_ != "AUX":
            return False

        return True

    def generate(
        self, context: str, question: str, answers: [str]
    ) -> List[Tuple[str, str, List[str]]]:
        if not self._filter_phrase(question):
            return [(context, question, answers)]

        paraphrased = self._transform(question)
        print(paraphrased)
        return [(context, paraphrased, answers)]


if __name__ == "__main__":
    import json
    from TestRunner import convert_to_snake_case

    tf = SuspectingParaphraser()

    test_cases = []
    for i, sentence in enumerate(
        [
            "Did Sally finally return the french book to Chris?",
            "Did the American National Shipment company really break its own fleet?",
            "Couldn't she just leave?",
            "Shall you begone, lad?",
            "Has Buzz Aldrin, the first person who walked on the moon, brought back some aliens?",
        ]
    ):
        res = tf.generate("", sentence, [])
        test_cases.append(
            {
                "class": tf.name(),
                "inputs": {"context": "", "question": sentence, "answers": []},
                "outputs": [],
            }
        )

        for p_context, p_question, p_answers in res:
            test_cases[i]["outputs"].append(
                {"context": p_context, "question": p_question, "answers": p_answers}
            )

    json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
    print(json.dumps(json_file))
