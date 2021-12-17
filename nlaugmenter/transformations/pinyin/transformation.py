import re

import spacy
from g2pM import G2pM

from nlaugmenter.interfaces.SentenceOperation import SentenceOperation
from nlaugmenter.tasks.TaskTypes import TaskType

VOWELS = set("aeiou")
CHINESE_CHAR = re.compile("[\u4e00-\u9fff]+")
CHINESE_PUNC = re.compile("[\u3000-\u303f]+")


class PinyinTranscription(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
    ]
    languages = ["zh"]
    heavy = True

    def __init__(self, seed=0, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)
        self.nlp = spacy.load("zh_core_web_sm")
        self.g2pm = G2pM()

    def word_to_pinyin(self, word: str, with_tones: bool) -> str:
        """Ex.: "你好" -> "nihao"

        `word` should be only in Chinese characters
        """
        if not re.match(CHINESE_CHAR, word):
            raise ValueError(
                "`word` should be comprised exclusively of "
                "Chinese characters"
            )
        syllables = self.g2pm(word, tone=with_tones)
        pinyin = ""
        for i in range(len(syllables)):
            syllable = syllables[i].replace("u:", "v")
            # TODO: Check that this is correct in all cases
            if i > 0 and len(word) and word[0] in VOWELS:
                pinyin += "'" + syllable
            else:
                pinyin += syllable
        return pinyin

    def generate(self, sentence: str, with_tones: bool = False):
        """Convert sentence to space-separated pinyinized words.
        Ex.: "你会讲中文吗？" -> "ni hui jiang zhongwen ma ？"
        """
        doc = self.nlp(sentence)

        tokens = []
        for token in doc:
            if CHINESE_CHAR.match(token.text):
                tokens.append(self.word_to_pinyin(token.text, with_tones))
            else:
                tokens.append(token.text)
        pinyin = " ".join(tokens)
        return [pinyin]
