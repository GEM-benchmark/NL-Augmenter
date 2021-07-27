from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


class UniversalBiasFilter(SentenceOperation):
    tasks = [TaskType.TEXT_TO_TEXT_GENERATION]

    def __init__(self, target=None, test=None):
        super().__init__()
        self.target = target
        self.test = test

    @staticmethod
    def flag_sentences(sentences, target, test):
        flagged_sentences = []

        for i, sentence in enumerate(sentences):
            target_flag = False
            test_flag = False
            union_flag = False
            neutral_flag = False

            intersection_target = set()
            intersection_test = set()
            intersection_target = set(sentence.lower().split()).intersection(
                set(target)
            )
            intersection_test = set(sentence.lower().split()).intersection(
                set(test)
            )

            target_flag = len(intersection_target) > 0
            test_flag = len(intersection_test) > 0
            union_flag = (
                len(intersection_target) > 0 and len(intersection_test) > 0
            )
            neutral_flag = (
                len(intersection_target) == 0 and len(intersection_test) == 0
            )

            if union_flag is True:
                target_flag = False
                test_flag = False
                neutral_flag = True

            sentence_object = {
                "sentence": sentence,
                "target_flag": target_flag,
                "test_flag": test_flag,
                "neutral_flag": neutral_flag,
            }

            flagged_sentences.append(sentence_object)

        return flagged_sentences

    @staticmethod
    def count_groups(flagged_corpus):
        target_count = len(
            [
                flag
                for flag in flagged_corpus
                if flag.get("target_flag") is True
            ]
        )
        test_count = len(
            [flag for flag in flagged_corpus if flag.get("test_flag") is True]
        )
        neutral_count = len(
            [
                flag
                for flag in flagged_corpus
                if flag.get("neutral_flag") is True
            ]
        )

        return target_count, test_count, neutral_count

    def filter(self, sentences: []) -> bool:
        biased = False
        flagged_corpus = self.flag_sentences(sentences, self.target, self.test)
        target_count, test_count, neutral_count = self.count_groups(
            flagged_corpus
        )

        if target_count < test_count:
            biased = True
        else:
            biased = False

        return biased