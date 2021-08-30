import spacy

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

"""
Base Class for implementing the different input transformations a generation should be robust against.
"""
"""
Yoda Speak implementation borrowed from here: https://github.com/yevbar/Yoda-Script, with minor mofifications to fix
deprecation and to change some stylistic features
"""

punctuation = [",", ".", ";", "?", "!"]
nlp = spacy.load("en_core_web_sm")
comma = nlp(" , ")[1]


def sentify(text):
    output = []
    doc = nlp(text)
    for sent in doc.sents:
        sentence = []
        for clause in clausify(sent):
            sentence.append(yodafy(clause))
        output.append(sentence)
    return output


def clausify(sent):
    output = []
    cur = []
    for token in sent:
        if token.dep_ == "cc" or (
            token.dep_ == "punct" and token.text in punctuation
        ):
            output.append(cur)
            output.append([token])
            cur = []
        else:
            cur.append(token)
    if cur != []:
        output.append(cur)
    return output


def yodafy(clause):
    new_array = []
    state = False
    for token in clause:
        if state:
            new_array.append(token)
        if not state and (token.dep_ == "ROOT" or token.dep_ == "aux"):
            state = True
    if len(new_array) > 0 and new_array[len(new_array) - 1].dep_ != "punct":
        new_array.append(comma)
    for token in clause:
        new_array.append(token)
        if token.dep_ == "ROOT" or token.dep_ == "aux":
            break
    return new_array


def yoda(s):
    string = []
    yodafied = sentify(s)
    for sentence in yodafied:
        sent = ""
        for clause in sentence:
            for token in clause:
                if token.dep_ in ["NNP", "NNPS"] or token.text == "I":
                    sent += token.text + " "
                elif sent == "":
                    if token.dep_ == "neg":
                        sent += "Not" + " "
                    else:
                        sent += token.text[0].upper() + token.text[1:] + " "
                elif token.dep_ == "punct":
                    sent = sent[: len(sent) - 1] + token.text + " "
                else:
                    if token.pos_ == "PROPN":
                        sent += token.text + " "
                    else:
                        sent += token.text.lower() + " "
        string.append(sent + " ")
    return "".join(string).rstrip(" ")


class YodaPerturbation(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["en"]

    def __init__(self, seed=0, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)

    def generate(self, sentence: str):
        perturbed_texts = yoda(sentence)
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
    print(json.dumps(json_file, indent=2))
"""
