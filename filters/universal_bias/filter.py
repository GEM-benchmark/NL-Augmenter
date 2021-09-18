from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
import re

class UniversalBiasFilter(SentenceOperation):
    tasks = [TaskType.TEXT_TO_TEXT_GENERATION]
    keywords = ["rule-based", "social-reasoning"]

    def __init__(self, minority=None, majority=None):
        super().__init__()
        self.minority = minority
        self.majority = majority

    @staticmethod
    def flag_sentences(sentences, minority, majority):
        """
        flag sentences as belonging to the minority, majority or neutral groups
        :param sentences: sentences array
        :param minority: array of keywords, describing potentially underrepresented population group
        :param majority: array of keywords, describing dominating group 
        :return: array of objects, each containing the analyzed sentence along with three flags
        """
        flagged_sentences = []

        # Check whether the sentences array is not empty, otherwise - inform the user
        assert len(sentences) > 0, "You must provide at least one sentence for the analysis. Check the content of your sentences array you pass to the filter() method."

        for sentence in sentences:
            
            # Initialize the variables
            minority_flag = False
            majority_flag = False
            union_flag = False
            neutral_flag = False
            intersection_minority = set()
            intersection_majority = set()

            # Clean the sentence content using regex
            sentence_cleaned = sentence.lower()
            sentence_cleaned = re.sub('^',' ', sentence_cleaned)
            sentence_cleaned = re.sub('$',' ', sentence_cleaned)

            # Take care of urls
            words = []
            for word in sentence_cleaned.split():
                i = word.find('http') 
                if i >= 0:
                    word = word[:i] + ' ' + '__url__'
                words.append(word.strip())
            sentence_cleaned = ' '.join(words)
            sentence_cleaned = re.sub(r'\[([^\]]*)\] \( *__url__ *\)', r'\1', sentence_cleaned)

            # Remove illegal chars and extra space
            sentence_cleaned = re.sub('__url__','URL', sentence_cleaned)
            sentence_cleaned = re.sub(r"[^A-Za-z0-9():,.!?\"\']", " ", sentence_cleaned)
            sentence_cleaned = re.sub('URL','__url__', sentence_cleaned)	
            sentence_cleaned = re.sub(r'^\s+', '', sentence_cleaned)
            sentence_cleaned = re.sub(r'\s+$', '', sentence_cleaned)
            sentence_cleaned = re.sub(r'\s+', ' ', sentence_cleaned)

            # Split the words in the sentence to find the intersection with the minority array of keywords
            intersection_minority = set(sentence_cleaned.split()).intersection(
                set(minority)
            )
            # Split the words in the sentence to find the intersection with the majority array of keywords
            intersection_majority = set(sentence_cleaned.split()).intersection(
                set(majority)
            )

            # If the intersection occured, the intersection_minority and intersection_majority will contain at least one common keyword
            # use this intersection information to get the value for the corresponding flags
            minority_flag = len(intersection_minority) > 0
            majority_flag = len(intersection_majority) > 0

            # In case the sentence contains the keywords from minority and majority groups, set a union_flag value
            union_flag = (
                len(intersection_minority) > 0 and len(intersection_majority) > 0
            )

            # If the sentence didn't contain the keywords neither from minority, nor from majority groups, set a neutral_flag value 
            neutral_flag = (
                len(intersection_minority) == 0 and len(intersection_majority) == 0
            )

            # Use the union_flag value to set the neutral_flag value, setting to False the minority and majority flags
            if union_flag is True:
                minority_flag = False
                majority_flag = False
                neutral_flag = True

            # Create the sentence object with the retrieved flag values
            sentence_object = {
                "sentence": sentence,
                "minority_flag": minority_flag,
                "majority_flag": majority_flag,
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
        :return: 3 integer values, representing minority, majority and neutral groups respectively
        """
        minority_count = len(
            [
                flag
                for flag in flagged_corpus
                if flag.get("minority_flag") is True
            ]
        )
        majority_count = len(
            [flag for flag in flagged_corpus if flag.get("majority_flag") is True]
        )
        neutral_count = len(
            [
                flag
                for flag in flagged_corpus
                if flag.get("neutral_flag") is True
            ]
        )

        return minority_count, majority_count, neutral_count

    @staticmethod
    def sort_groups(flagged_corpus):
        """
        sort the sentences in each of 3 groups
        :param flagged_corpus: array of flagged sentences
        :return: 3 arrays of strings, containing minority, majority and neutral groups respectively
        """
        minority_group = [
                flag.get("sentence")
                for flag in flagged_corpus
                if flag.get("minority_flag") is True
            ]
        majority_group = [
                flag.get("sentence")
                for flag in flagged_corpus
                if flag.get("majority_flag") is True
            ]
        neutral_group = [
                flag.get("sentence")
                for flag in flagged_corpus
                if flag.get("neutral_flag") is True
            ]
    
        return minority_group, majority_group, neutral_group


    def filter(self, sentences: []) -> bool:
        """
        filter the sentences to define whether the minority group is underepresented
        :param sentences: array of sentences
        :return: boolean, which is set to True if the the minority group is underepresented  
        """
        biased = False
        
        # Retrieve the flags for each of the sentences
        flagged_corpus = self.flag_sentences(sentences, self.minority, self.majority)

        # Use the retrieved flags to count the number of sentences in each group
        minority_count, majority_count, neutral_count = self.count_groups(
            flagged_corpus
        )

        minority_percentage = 100 * float(minority_count) / float(len(sentences))
        majority_percentage = 100 * float(majority_count) / float(len(sentences))


        # If the mumber of sentences in terms of percentage in the minority group
        # is lower than in the majority group, set bias to True
        # Note, that the neutral group is not taken into account in this calculation
        if minority_percentage < majority_percentage:
            biased = True
        else:
            biased = False

        return biased
