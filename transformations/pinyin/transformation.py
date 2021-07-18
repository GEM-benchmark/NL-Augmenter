import spacy
from g2pM import G2pM
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


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
            syllable = syllables[i].replace('u:', 'v')
            if i > 0 and len(word) and word[0] in VOWELS:
                pinyin += "'" + syllable
            else:
                pinyin += syllable
        return pinyin

    def generate(self, sentence: str):
        '''Convert sentence to space-separated pinyinized words.
        Ex.: "你会讲中文吗？" -> "ni hui jiang zhongwen ma ？"
        '''
        doc = self.nlp(sentence)
        tokens = [t.text_with_ws for t in doc]
        pinyin = ' '.join(self.word_to_pinyin(token) for token in tokens)
        return [pinyin]
