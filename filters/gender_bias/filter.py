from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


class GenderBiasFilter(SentenceOperation):
    tasks = [TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]

    def __init__(self):
        super().__init__()

    @staticmethod
    def flag_sentences(sentences):
        flagged_sentences = []
        feminine = ["she", "her", "hers"]
        masculine = ["he", "him", "his"]
        for i, sentence in enumerate(sentences):
            feminine_flag = False
            masculin_flag = False
            union_flag = False
            neutral_flag = False
            intersection_feminine = set()
            intersection_masculine = set()
            intersection_feminine = set(sentence.lower().split()).intersection(
                set(feminine)
            )
            intersection_masculine = set(
                sentence.lower().split()
            ).intersection(set(masculine))
            feminine_flag = len(intersection_feminine) > 0
            masculin_flag = len(intersection_masculine) > 0
            union_flag = (
                len(intersection_feminine) > 0
                and len(intersection_masculine) > 0
            )
            neutral_flag = (
                len(intersection_feminine) == 0
                and len(intersection_masculine) == 0
            )
            if union_flag is True:
                feminine_flag = False
                masculin_flag = False
                neutral_flag = True
            sentence_object = {
                "sentence": sentence,
                "feminine_flag": feminine_flag,
                "masculin_flag": masculin_flag,
                "neutral_flag": neutral_flag,
            }
            flagged_sentences.append(sentence_object)
        return flagged_sentences

    @staticmethod
    def count_genders(flagged_corpus):
        feminine_count = len(
            [
                flag
                for flag in flagged_corpus
                if flag.get("feminine_flag") is True
            ]
        )
        masculine_count = len(
            [
                flag
                for flag in flagged_corpus
                if flag.get("masculin_flag") is True
            ]
        )
        neutral_count = len(
            [
                flag
                for flag in flagged_corpus
                if flag.get("neutral_flag") is True
            ]
        )
        return feminine_count, masculine_count, neutral_count

    def filter(self, sentences: []) -> bool:
        biased = False
        flagged_corpus = self.flag_sentences(sentences)
        feminine_count, masculine_count, neutral_count = self.count_genders(
            flagged_corpus
        )
        if feminine_count < masculine_count:
            biased = True
        else:
            biased = False
        return biased
