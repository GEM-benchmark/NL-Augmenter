from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
from initialize import spacy_nlp
import spacy


class DiscriminationFilter(SentenceOperation):
    tasks = [TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en", "fr"]

    def __init__(self, language, minority_group, majority_group, minority_factor, majority_factor):
        super().__init__()
        self.language = language
        self.minority_group = minority_group
        self.majority_group = majority_group
        self.minority_factor = minority_factor
        self.majority_factor = majority_factor

    @staticmethod
    def flag_sentences(sentences, minority_group, majority_group):
        """
        flag sentences as belonging to the minority_group, majority_group or neutral groups
        :param sentences: sentences array
        :param minority_group: array of keywords, describing potentially underrepresented population group
        :param majority_group: array of keywords, describing dominating group 
        :return: array of objects, each containing the analyzed sentence along with three flags
        """
        flagged_sentences = []

        # Check whether the array are not empty, otherwise - inform the user
        assert len(sentences) > 0, "You must provide at least one sentence for the analysis. Check the content of your sentences array you pass to the filter() method."
        assert len(minority_group) > 0, "You must provide at least one keyword in the minority group array."
        assert len(majority_group) > 0, "You must provide at least one keyword in the majority group array."

        for sentence in sentences:
            
            # Initialize the variables
            minority_group_flag = False
            majority_group_flag = False
            union_flag = False
            neutral_flag = False

            intersection_minority_group = set()
            intersection_majority_group = set()

            # Lowercase and split the words in the sentence to find the intersection with the minority_group array of keywords
            intersection_minority_group = set(sentence.lower().split()).intersection(
                set(minority_group)
            )
            # Lowercase and split the words in the sentence to find the intersection with the majority_group array of keywords
            intersection_majority_group = set(sentence.lower().split()).intersection(
                set(majority_group)
            )

            # If the intersection occured, the intersection_minority_group and intersection_majority_group will contain at least one common keyword
            # use this intersection information to get the value for the corresponding flags
            minority_group_flag = len(intersection_minority_group) > 0
            majority_group_flag = len(intersection_majority_group) > 0

            # In case the sentence contains the keywords from minority_group and majority_group groups, set a union_flag value
            union_flag = (
                len(intersection_minority_group) > 0 and len(intersection_majority_group) > 0
            )

            # If the sentence didn't contain the keywords neither from minority_group, nor from majority_group groups, set a neutral_flag value 
            neutral_flag = (
                len(intersection_minority_group) == 0 and len(intersection_majority_group) == 0
            )

            # Create the sentence object with the retrieved flag values
            sentence_object = {
                "sentence": sentence,
                "minority_group_flag": minority_group_flag,
                "majority_group_flag": majority_group_flag,
                "union_flag": union_flag,
                "neutral_flag": neutral_flag
            }

            # Append the object to the array we return
            flagged_sentences.append(sentence_object)

        return flagged_sentences

    @staticmethod
    def count_groups(flagged_corpus):
        """
        count the number of sentences in each of groups
        :param flagged_corpus: array of flagged sentences
        :return: 3 integer values, representing minority_group, majority_group and neutral groups respectively
        """
        minority_group_count = len(
            [
                flag
                for flag in flagged_corpus
                if flag.get("minority_group_flag") is True
            ]
        )
        majority_group_count = len(
            [
                flag 
                for flag in flagged_corpus 
                if flag.get("majority_group_flag") is True
             ]
        )
        union_count = len(
            [
                flag
                for flag in flagged_corpus
                if flag.get("union_flag") is True
            ]
        )
        neutral_count = len(
            [
                flag
                for flag in flagged_corpus
                if flag.get("neutral_flag") is True
            ]
        )

        return minority_group_count, majority_group_count, union_count, neutral_count

    @staticmethod
    def find_intersection(language, minority_group, majority_group, minority_factor, majority_factor):
        """
        find intersection between minority group and two factors, then do the same for the majority group
        :param minority_group: array of keywords, describing minority group
        :param majority_group: array of keywords, describing majority group
        :param minority_factor: array of keywords, describing minority factor
        :param majority_factor: array of keywords, describing majority factor 
        :return: array of objects, each containing the analyzed sentence along with two flags
        """
        # Load the appropriate langauge model from spacy
        if language == "en":
            nlp = spacy.load("en_core_web_sm")
        elif language == "fr":
            nlp = spacy.load("fr_core_news_sm")
        else:
            raise NameError('The specified language is not supported or misformatted. Try "en" or "fr" as language arguments to the filter() method.')

        flagged_sentences = []

        # Iterate through minority group and find intersections for both factors       
        for sentence in minority_group:
            sentence_lemmatized = []
            minority_factor_intersection = False

            sentence = nlp(sentence.lower())
            for token in sentence:
                if token.lemma_ != "." and token.lemma_ != "," and token.lemma_ != "?" and token.lemma_ != "!":
                    sentence_lemmatized.append(token.lemma_)
          
            intersection_minority_factor = set(sentence_lemmatized).intersection(
                set(minority_factor)
            )           
            intersection_majority_factor = set(sentence_lemmatized).intersection(
                set(majority_factor)
            )
            
            # If the sentence from the minority group has the intersection with the minority factor - the flag is set to True
            # Otherwise, if the minority group sentence has the intersection in the majority factor, or both factors are present - the flag stays set to False
            if intersection_minority_factor > intersection_majority_factor:
                minority_factor_intersection = True

            # Create the sentence object with the retrieved flag values
            sentence_object = {
                "sentence": sentence,
                "minority_group": True,
                "minority_factor_intersection": minority_factor_intersection
            }

            # Append the object to the array we return
            flagged_sentences.append(sentence_object)

        # Iterate through the majority group and find te intersections for both factors
        for sentence in majority_group:
            sentence_lemmatized = []
            minority_factor_intersection = False

            sentence = nlp(sentence.lower())
            for token in sentence:
                if token.lemma_ != "." and token.lemma_ != "," and token.lemma_ != "?" and token.lemma_ != "!":
                    sentence_lemmatized.append(token.lemma_)

            minority_factor_intersection = False
            intersection_minority_factor = set(sentence_lemmatized).intersection(
                set(minority_factor)
            )         
            intersection_majority_factor = set(sentence).intersection(
                set(majority_factor)
            )
            
            # If the sentence from the majority group has the intersection with the minority factor - the flag is set to True
            # Otherwise, if the majority group sentence has the intersection in the majority factor, or both factors are present - the flag stays set to False
            if intersection_minority_factor > intersection_majority_factor:
                minority_factor_intersection = True

            # Create the sentence object with the retrieved flag values
            sentence_object = {
                "sentence": sentence,
                "majority_group": True,
                "minority_factor_intersection": minority_factor_intersection
            }

            # Append the object to the array we return
            flagged_sentences.append(sentence_object)
  
        return flagged_sentences

    @staticmethod
    def count_intersections(flagged_corpus):
        """
        count the number of sentences in each of groups
        :param flagged_corpus: array of flagged sentences with the information about minority factor intersections
        :return: 2 integer values, representing the number of minority factor intersection in each of the groups
        """
        minority_group_intersection_count = len(
            [
                flag
                for flag in flagged_corpus
                if flag.get("minority_group") is True and flag.get("minority_factor_intersection") is True
            ]
        )       
        majority_group_intersection_count = len(
            [
                flag 
                for flag in flagged_corpus 
                if flag.get("majority_group") is True and flag.get("minority_factor_intersection") is True
             ]
        )

        return minority_group_intersection_count, majority_group_intersection_count

    @staticmethod
    def sort_groups(flagged_corpus):
        """
        sort the sentences in each of 3 groups
        :param flagged_corpus: array of flagged sentences
        :return: 3 arrays of strings, containing minority_group, majority_group and neutral groups respectively
        """
        minority_group = [
                flag.get("sentence")
                for flag in flagged_corpus
                if flag.get("minority_group_flag") is True
            ]
        majority_group = [
                flag.get("sentence")
                for flag in flagged_corpus
                if flag.get("majority_group_flag") is True
            ]
        union_group = [
                flag.get("sentence")
                for flag in flagged_corpus
                if flag.get("union_flag") is True
            ]
        neutral_group = [
                flag.get("sentence")
                for flag in flagged_corpus
                if flag.get("neutral_flag") is True
            ]
    
        return minority_group, majority_group, union_group, neutral_group


    def filter(self, sentences: []) -> bool:
        """
        filter the sentences to define whether the minority_group group is underepresented
        :param sentences: array of sentences
        :return: boolean, which is set to True if the the minority_group group is underepresented  
        """
        discrimination = False
        
        # Retrieve the flags for each of the sentences
        flagged_corpus = self.flag_sentences(sentences, self.minority_group, self.majority_group)

        # Use the flagged objects to get the groups
        minority_group, majority_group, union_group, neutral_group = self.sort_groups(flagged_corpus)

        # Retrive the flags of intersection for the miority and majority groups
        doubble_flagged_corpus = self.find_intersection(self.language, minority_group, majority_group, self.minority_factor, self.majority_factor)

        # Count the number of intersections with the minority and majority factors
        minority_group_intersection_count, majority_group_intersection_count = self.count_intersections(doubble_flagged_corpus)
		
		minority_group_intersection_percentage = 100 * float(minority_group_intersection_count)/float(len(sentences))
        majority_group_intersection_percentage = 100 * float(majority_group_intersection_count)/float(len(sentences))

        # If the number of intersections with the minority factors preveils for the minority group, indicate potential discrimination  
        if minority_group_intersection_percentage > majority_group_intersection_percentage:
            discrimination = True
        else:
            discrimination = False       

        return discrimination