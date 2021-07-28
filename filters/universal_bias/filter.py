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
        """
        flag sentences as belonging to the target, test or neutral groups
        :param sentences: sentences array
        :param target: array of keywords, describing potentially underrepresented population group
        :param test: array of keywords, describing dominating group 
        :return: array of objects, containing the analysed sentence along with three flags, one of which is set to True
        """
        flagged_sentences = []

        for sentence in sentences:
            
            # Initialize the variables
            target_flag = False
            test_flag = False
            union_flag = False
            neutral_flag = False

            intersection_target = set()
            intersection_test = set()

            # Lowercase and split the words in the sentence to find the intersection with the target array of keywords
            intersection_target = set(sentence.lower().split()).intersection(
                set(target)
            )
            # Lowercase and split the words in the sentence to find the intersection with the test array of keywords
            intersection_test = set(sentence.lower().split()).intersection(
                set(test)
            )

            # If the intersection occured, the intersection_target and intersection_test will contain at least one common keyword
            # use this intersection information to get the value for the corresponding flags
            target_flag = len(intersection_target) > 0
            test_flag = len(intersection_test) > 0

            # In case the sentence contains the keywords from target and test groups, set a union_flag value
            union_flag = (
                len(intersection_target) > 0 and len(intersection_test) > 0
            )

            # If the sentence didn't contain the keywords neither from target, nor from test groups, set a neutral_flag value 
            neutral_flag = (
                len(intersection_target) == 0 and len(intersection_test) == 0
            )

            # Use the union_flag value to set the neutral_flag value, setting to False the target and test flags
            if union_flag is True:
                target_flag = False
                test_flag = False
                neutral_flag = True

            # Create the sentence object with the retrieved flag values
            sentence_object = {
                "sentence": sentence,
                "target_flag": target_flag,
                "test_flag": test_flag,
                "neutral_flag": neutral_flag,
            }

            # Append the object to the array we return
            flagged_sentences.append(sentence_object)

        return flagged_sentences

    @staticmethod
    def count_groups(flagged_corpus):
        """
        count the number of sentences in each of groups
        :param flagged_corpus: array of flagged sentences
        :return: 3 integer values, representing target, test and neutral groups respectively
        """
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

    @staticmethod
    def sort_groups(flagged_corpus):
        """
        sort the sentences in each of 3 groups
        :param flagged_corpus: array of flagged sentences
        :return: 3 arrays of strings, containing target, test and neutral groups respectively
        """
        target_group = [
                flag.get("sentence")
                for flag in flagged_corpus
                if flag.get("target_flag") is True
            ]
        test_group = [
                flag.get("sentence")
                for flag in flagged_corpus
                if flag.get("test_flag") is True
            ]
        neutral_group = [
                flag.get("sentence")
                for flag in flagged_corpus
                if flag.get("neutral_flag") is True
            ]
    
        return target_group, test_group, neutral_group


    def filter(self, sentences: []) -> bool:
        """
        filter the sentences to define whether the target group is underepresented
        :param sentences: array of sentences
        :return: boolean, which is set to True if the the target group is underepresented  
        """
        biased = False
        # Retrieve the flags for each of the sentences
        flagged_corpus = self.flag_sentences(sentences, self.target, self.test)

        # Use the retrieved flags to count the number of sentences in each group
        target_count, test_count, neutral_count = self.count_groups(
            flagged_corpus
        )

        # If the mumber of sentences in the target group is lower than in the test group, set bias to True
        # Note, that the neutral group is not taken into account in this calculation
        if target_count < test_count:
            biased = True
        else:
            biased = False

        return biased