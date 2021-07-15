import spacy
from g2pM import G2pM
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


"""
Base Class for implementing the different input transformations a generation should be robust against.
"""


VOWELS = set('aeiou')


class PinyinTranscription(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["zh"]

    def __init__(self, seed=0, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)
        self.nlp = spacy.load('zh_core_web_sm')
        self.g2pm = G2pM()

    def word_to_pinyin(self, word: str) -> str:
        '''Ex.: "你好" -> "nihao"
        '''
        syllables = self.g2pm(word, tone=False)
        pinyin = ''
        for i in range(len(syllables)):
            # TODO: Check that this is correct in all cases
            if i > 0 and len(word) and word[0] in VOWELS:
                pinyin += "'" + syllables[i]
            else:
                pinyin += syllables[i]
        return pinyin

    def generate(self, sentence: str):
        doc = self.nlp(sentence)
        tokens = [t.text_with_ws for t in doc]
        pinyin = ' '.join(self.word_to_pinyin(token) for token in tokens)
        return [pinyin]


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
