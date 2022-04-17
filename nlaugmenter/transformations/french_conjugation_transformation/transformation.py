import re

import mlconjug
import nltk
import spacy
from spacy.language import Language
from spacy_lefff import LefffLemmatizer, POSTagger

from nlaugmenter.interfaces.SentenceOperation import SentenceOperation
from nlaugmenter.tasks.TaskTypes import TaskType

default_conjugator = mlconjug.Conjugator(language="fr")

nltk.download("wordnet")
nltk.download("punkt")

dicPronouns = {
    "j'": "1s",
    "J'": "1s",
    "je": "1s",
    "Je": "1s",
    "tu": "2s",
    "Tu": "2s",
    "il": "3s",
    "Il": "3s",
    "elle": "3s",
    "Elle": "3s",
    "on": "3s",
    "On": "3s",
    "'on": "3s",
    "nous": "1p",
    "Nous": "1p",
    "vous": "2p",
    "Vous": "2p",
    "ils": "3p",
    "Ils": "3p",
    "elles": "3p",
    "Elles": "3p",
}


# function to update value of a dictionary based on its key
def update_in_alist(alist, key, value):
    return [(k, v) if (k != key) else (key, value) for (k, v) in alist]


def update_in_alist_inplace(alist, key, value):
    alist[:] = update_in_alist(alist, key, value)


# function to change a dictionary key based on a given value
def update_in_alist_key(alist, key, value):
    return [(k, v) if (v != value) else (key, value) for (k, v) in alist]


def update_in_alist_inplace_key(alist, key, value):
    alist[:] = update_in_alist_key(alist, key, value)


# Sometimes, the conjugation of a verb will modify the first letter of the verb (ex : avec le verbe ALLER : je vais (présent) devient j'irais (futur)) we therefore need to change the pronoun "Je" to "J'"
def transform_pronoun_1s(sentence):
    # regex to find if "je" or "Je" is followed by a vowel
    regex_je = r"je (a|e|i|o|u|y|é|è|ê)|Je (a|e|i|o|u|y|é|è|ê)"
    reg = re.search(regex_je, sentence)

    if reg is None:
        pass
    else:
        sentence = sentence.replace("je ", "j'")
        sentence = sentence.replace("Je ", "J'")
    # regex to find if "J'"" or "j'" is folowed by a consonant
    regex_j = r"j'(z|r|t|p|q|s|d|f|g|h|j|k|l|m|w|x|c|v|b|n)|J'(z|r|t|p|q|s|d|f|g|h|j|k|l|m|w|x|c|v|b|n)"
    regj = re.search(regex_j, sentence)
    if regj is None:
        pass
    else:
        sentence = sentence.replace("j'", "je ")
        sentence = sentence.replace("J'", "Je ")
    return sentence


# sometimes, y is used to do a liason between the pronoun an a vowel, it must be deleted if next word starts by y or i
def y_exception(sentence):
    regex_y = r"j'y (i|y)|J'y (i|y|)"
    reg = re.search(regex_y, sentence)

    if reg is None:
        pass
    else:
        sentence = sentence.replace("j'y ", "j'")
        sentence = sentence.replace("J'y ", "J'")
    return sentence


# the negation is expressed with n' in font of a vowel and ne in front of a consonant
def n_exception(sentence):
    regex_n = r"n'(z|r|t|p|q|s|d|f|g|h|j|k|l|m|w|x|c|v|b|n)|N'(z|r|t|p|q|s|d|f|g|h|j|k|l|m|w|x|c|v|b|n)"
    reg = re.search(regex_n, sentence)
    if reg is None:
        pass
    else:
        sentence = sentence.replace("n'", "ne ")
        sentence = sentence.replace("N'", "Ne ")

    regex_ne = r"ne (a|e|i|o|u|y|é|è|ê)|Ne (a|e|i|o|u|y|é|è|ê)"
    reg = re.search(regex_ne, sentence)
    if reg is None:
        pass
    else:
        sentence = sentence.replace("ne ", "n'")
        sentence = sentence.replace("Ne ", "N'")
    return sentence


@Language.factory("french_lemmatizer")
def create_french_lemmatizer(nlp, name):
    return LefffLemmatizer()


@Language.factory("POSTagger")
def create_POSTagger(nlp, name):
    return POSTagger()


# for the library ML conjug, verbs must be in their infinitive form
def TurnToInfinitif(nlp, sentence):
    doc = nlp(sentence)
    verbs = [d.text for d in doc if d.pos_ == "VERB"]
    auxs = [d.text for d in doc if d.pos_ == "AUX"]
    auxs_lemma = [d.lemma_ for d in doc if d.pos_ == "AUX"]
    verbs_lemma = [d.lemma_ for d in doc if d.pos_ == "VERB"]

    listTuples = []

    for count, word in enumerate(doc):
        if word.lemma_ in verbs_lemma:
            listTuples.append((word.lemma_, "VERB"))
            if word.text == word.lemma_:
                update_in_alist_inplace(listTuples, word.lemma_, "INF")

        elif word.lemma_ in auxs_lemma:
            listTuples.append((word.lemma_, "AUX"))
            if doc[count - 1].text == "aller":
                update_in_alist_inplace(listTuples, "aller", "ALLER")
                for i in range(0, len(verbs)):
                    if verbs_lemma[i] == "aller":
                        update_in_alist_inplace_key(
                            listTuples, verbs[i], "ALLER"
                        )
        else:
            listTuples.append((word.text, "TEXT"))
        if word.lemma_ in verbs_lemma:
            if doc[count - 1].text in auxs:
                update_in_alist_inplace(
                    listTuples, doc[count - 1].lemma_, "AUX"
                )
                update_in_alist_inplace(listTuples, word.lemma_, "PP")
                update_in_alist_inplace_key(listTuples, word.text, "PP")
            elif doc[count - 1].text == "pas":
                if doc[count - 2].text in auxs:
                    update_in_alist_inplace(
                        listTuples, doc[count - 2].text, "AUX"
                    )
                    update_in_alist_inplace(listTuples, word.lemma_, "PP")
                    update_in_alist_inplace_key(listTuples, word.text, "PP")
    return listTuples


# function that conjugate verbs with mlconjug
def conjugate(nlp, sentence, pronoun, tense):
    infinitive = TurnToInfinitif(nlp, sentence)
    conjugatedSentence = []
    for tuple in infinitive:
        if tuple[1] == "VERB" or tuple[1] == "AUX":
            conjugatedSentence.append(
                default_conjugator.conjugate(tuple[0]).conjug_info[
                    "Indicatif"
                ][tense][pronoun]
            )
        else:
            conjugatedSentence.append(tuple[0])
    conjugatedSentence = transform_pronoun_1s(" ".join(conjugatedSentence))
    conjugatedSentence = conjugatedSentence.replace("' ", "'")
    conjugatedSentence = y_exception(conjugatedSentence)
    conjugatedSentence = n_exception(conjugatedSentence)
    return conjugatedSentence


# check if a word is in sentence
def contains_word(s, w):
    return f" {w} " in f" {s} "


# transform j' in je to avoid issues in the last function
def anomalous_1s_transform(sentence):
    regex_je = r"j'(a|e|i|o|u|y|é|è|ê)|J'(a|e|i|o|u|y|é|è|ê)"
    reg = re.search(regex_je, sentence)

    if reg is None:
        pass
    else:
        sentence = sentence.replace("j'", "je ")
        sentence = sentence.replace("J'", "Je ")
    return sentence


# transform "lorsqu'il" to "lorsqu' il" in order to detect the pronoun later on
def anomalous_indicators_transform(sentence):
    """on conjug_multiverbal_sentences, "lorsqu' " is trouble
    this is a way to fix it"""
    for word in sentence.split(" "):
        if word.startswith("lorsqu'"):
            sentence = sentence.replace(
                word, word.split("'")[0] + "' " + word.split("'")[1]
            )
    return sentence


# final function used to conjugate verbs
def french_conjugation_transformation(
    nlp, sentence, tense, dict_pronouns=dicPronouns
):
    """this function allows you to conjugate a multiverbal sentence where there are one or different
    pronouns. If the sentence is multiverbal, verbs are supposed to be conjugated on the same tense
    for exemple first person pronoun + verb(future) + ... + Third person pronoun + verb(future) + ...
    else concordance of the tenses might not be respected
    Pronouns MUST be specified as they are in the dicPronouns"""

    perturbed_texts = []

    sentence = anomalous_indicators_transform(sentence)

    regex_j = r"j'(a|e|i|o|u|y|é|è|ê)|J'(a|e|i|o|u|y|é|è|ê)"
    reg = re.search(regex_j, sentence)
    # if pronoun is "j'", it needs to be transformed as "je" for this process
    if reg is not None:
        sentence = anomalous_1s_transform(sentence)
    else:
        sentence = sentence

    pronouns_final_list = []
    pronouns = dict_pronouns.keys()
    list_pronouns = []

    for pronoun in pronouns:
        if contains_word(sentence, pronoun) is True:
            list_pronouns.append(pronoun)
    # if there is only one pronoun in the sentence (and therefore only one person for verbs transformation)
    if len(list_pronouns) == 1:
        for pronoun in list_pronouns:
            if pronoun in sentence:
                ispronoun = re.search(r"\b({})\b".format(pronoun), sentence)
                index_pronoun = ispronoun.start()
                pronouns_final_list.append(dict_pronouns[pronoun])
                conjugated = conjugate(
                    nlp, sentence, pronouns_final_list[0], tense
                )
                conjugated = conjugated.replace(".", "")
                final_sent = re.sub(" +", " ", conjugated)
                final_sent = final_sent.replace(" , ", ", ")
                final_sent = final_sent.replace("' ", "'")
                perturbed_texts.append(final_sent)
                return perturbed_texts
    elif len(list_pronouns) == 0:
        print(
            "No pronouns detected in this sentence, availables pronouns are in the dicPronouns"
        )
    else:
        index_pronouns = []
        for pronoun in list_pronouns:
            if pronoun in sentence:
                ispronoun = re.search(r"\b({})\b".format(pronoun), sentence)
                index_pronoun = ispronoun.start()
                index_pronouns.append(index_pronoun)
                pronouns_final_list.append(dict_pronouns[pronoun])
                # if sentence do not start by pronoun
                if index_pronouns[0] != 0:
                    indexBefore = index_pronouns[0] - 1
                    indexStart = index_pronouns[0]
                    sentence0 = sentence[0:indexBefore]
                    sentence1 = sentence[indexStart:]
                    ispronoun = re.search(
                        r"\b({})\b".format(pronoun), sentence1
                    )
                    idx_pronouns = ispronoun.start()
                    if idx_pronouns != 0:
                        indexBefore = idx_pronouns - 1

                        split_sentence = (
                            sentence1[:indexBefore]
                            + "."
                            + sentence1[indexBefore:]
                        )
                        splited_sentences = nltk.sent_tokenize(split_sentence)
                        sent_list = []
                        conjug_sent = []
                        for i in range(len(splited_sentences)):
                            sent_pron = [
                                splited_sentences[i],
                                pronouns_final_list[i],
                            ]
                            conjugated = conjugate(
                                nlp,
                                splited_sentences[i],
                                pronouns_final_list[i],
                                tense,
                            )
                            # delete the "." added in the split sentence process
                            conjugated = conjugated.replace(".", "")
                            conjug_sent.append(conjugated)
                            sent_list.append(sent_pron)
                        # join the conjugated sentences in a final one
                        final_sent = " ".join(conjug_sent)
                        final_sent = sentence0 + " " + final_sent
                        # delete the extra space
                        final_sent = re.sub(" +", " ", final_sent)
                        final_sent = final_sent.replace(" , ", ", ")
                        final_sent = final_sent.replace("' ", "'").replace(
                            " '", "'"
                        )
                        perturbed_texts.append(final_sent)
                        return perturbed_texts
                else:
                    indexBefore = index_pronoun - 1
                    if index_pronoun != 0:
                        split_sentence = (
                            sentence[:indexBefore]
                            + "."
                            + sentence[indexBefore:]
                        )
                        splited_sentences = nltk.sent_tokenize(split_sentence)
                        sent_list = []
                        conjug_sent = []

                        for i in range(len(splited_sentences)):
                            sent_pron = [
                                splited_sentences[i],
                                pronouns_final_list[i],
                            ]
                            conjugated = conjugate(
                                nlp,
                                splited_sentences[i],
                                pronouns_final_list[i],
                                tense,
                            )
                            # delete the "." added in the split sentence process
                            conjugated = conjugated.replace(".", "")
                            conjug_sent.append(conjugated)
                            sent_list.append(sent_pron)
                        # join the conjugated sentences in a final one
                        final_sent = " ".join(conjug_sent)
                        # delete the extra space
                        final_sent = re.sub(" +", " ", final_sent)
                        final_sent = final_sent.replace(" , ", ", ")
                        final_sent = final_sent.replace("' ", "'").replace(
                            " '", "'"
                        )

                        perturbed_texts.append(final_sent)
                        return perturbed_texts


class Conjugation_transformation(SentenceOperation):

    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
    ]
    languages = ["fr"]
    keyword = [
        "high-coverage",
        "highly-meaning-preserving",
        "lexical",
        "model-based",
    ]

    # The transormation tense is specified here
    def __init__(self, tense):
        super().__init__()
        assert tense in ["Futur", "Imparfait"]
        self.tense = tense

        self.nlp = spacy.load("fr_core_news_md")
        # definition of spacy pipeline

        self.nlp.add_pipe("POSTagger", name="pos")
        self.nlp.add_pipe("french_lemmatizer", name="lefff", after="pos")

    def generate(self, sentence: str):
        perturbed_texts = french_conjugation_transformation(
            self.nlp,
            sentence,
            self.tense,
        )
        return perturbed_texts
