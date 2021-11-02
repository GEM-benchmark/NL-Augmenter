import re
import json
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


class GenderBiasFilter(SentenceOperation):
    tasks = [TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en", "fr", "pl", "ru"]
    keywords = ["rule-based", "social-reasoning"]

    def __init__(self, language, feminine_input=[], masculine_input=[]):
        """
        initialise the language and user defined arrays of keywords for feminine and masculine groups
        :param language: the string key representing the supported language
        :param feminine_input: array of keywords defined by the user and designating the female group
        :param masculine_input: array of keywords defined by the user and designating the male group
        """
        super().__init__()
        self.language = language
        self.feminine_input = feminine_input
        self.masculine_input = masculine_input

    @staticmethod
    def flag_sentences(
            sentences, language, feminine_input=[], masculine_input=[]
    ):
        """
        flag sentences as belonging to the feminine, masculine or neutral groups
        :param sentences: sentences array
        :param language: the string key representing the supported language
        :param feminine_input: array of keywords defined by the user and designating the female group
        :param masculine_input: array of keywords defined by the user and designating the male group
        :return: array of objects, each containing the analyzed sentence along with three flags
        """
        flagged_sentences = []

        # Read names
        f = open('filters/gender_bias/lexicals.json')
        data = json.load(f)

        # Define the words, that represent feminine and masculine groups in both languages
        if language == "en":

            feminine_titles = data["feminine_titles_en"]
            feminine_relation = data["feminine_relation_en"]
            feminine_relation_plural = data["feminine_relation_plural_en"]
            feminine_jobs = data["feminine_jobs_en"]
            feminine_jobs_plural = data["feminine_jobs_plural_en"]
            feminine_names = data['feminine_names_en']

            masculine_titles = data["masculine_titles_en"]
            masculine_relation = data["masculine_relation_en"]
            masculine_relation_plural = data["masculine_relation_plural_en"]
            masculine_jobs = data["masculine_jobs_en"]
            masculine_jobs_plural = data["masculine_jobs_plural_en"]
            masculine_names = data["masculine_names_en"]

            feminine = (
                    ["she", "her", "hers"]
                    + feminine_relation
                    + feminine_relation_plural
                    + feminine_titles
                    + feminine_jobs
                    + feminine_jobs_plural
                    + feminine_names
            )
            masculine = (
                    ["he", "him", "his"]
                    + masculine_relation
                    + masculine_relation_plural
                    + masculine_titles
                    + masculine_jobs
                    + masculine_jobs_plural
                    + masculine_names
            )

        elif language == "fr":

            feminine_titles = data["feminine_titles_fr"]
            feminine_relation = data["feminine_relation_fr"]
            feminine_relation_plural = data["feminine_relation_plural_fr"]
            feminine_jobs = data["feminine_jobs_fr"]
            feminine_jobs_plural = data["feminine_jobs_plural_fr"]
            feminine_names = data['feminine_names_fr']

            masculine_jobs = data["masculine_jobs_fr"]
            masculine_jobs_plural = data["masculine_jobs_plural_fr"]
            masculine_relation = data["masculine_relation_fr"]
            masculine_relation_plural = data["masculine_relation_plural_fr"]
            masculine_titles = data["masculine_titles_fr"]
            masculine_names = data['masculine_names_fr']

            feminine = (
                    ["elle", "sienne"]
                    + feminine_relation
                    + feminine_relation_plural
                    + feminine_titles
                    + feminine_jobs
                    + feminine_jobs_plural
                    + feminine_names
            )
            masculine = (
                    ["il", "sien"]
                    + masculine_relation
                    + masculine_relation_plural
                    + masculine_titles
                    + masculine_jobs
                    + masculine_jobs_plural
                    + masculine_names
            )

        elif language == "pl":

            feminine_titles = data["feminine_titles_pl"]
            feminine_relation = data["feminine_relation_pl"]
            feminine_relation_plural = data["feminine_relation_plural_pl"]
            feminine_jobs = data["feminine_jobs_pl"]
            feminine_jobs_plural = data["feminine_jobs_plural_pl"]
            feminine_names = data['feminine_names_pl']

            masculine_titles = data["masculine_titles_pl"]
            masculine_relation = data["masculine_relation_pl"]
            masculine_relation_plural = data["masculine_relation_plural_pl"]
            masculine_jobs = data["masculine_jobs_pl"]
            masculine_jobs_plural = data["masculine_jobs_plural_pl"]
            masculine_names = data['masculine_names_pl']

            feminine = (
                    ["ona", "jej"]
                    + feminine_relation
                    + feminine_relation_plural
                    + feminine_titles
                    + feminine_jobs
                    + feminine_jobs_plural
                    + feminine_names
            )
            masculine = (
                    ["on", "jego"]
                    + masculine_relation
                    + masculine_relation_plural
                    + masculine_titles
                    + masculine_jobs
                    + masculine_jobs_plural
                    + masculine_names
            )

        elif language == "ru":

            feminine_titles = data["feminine_titles_ru"]
            feminine_relation = data["feminine_relation_ru"]
            feminine_relation_plural = data["feminine_relation_plural_ru"]
            feminine_jobs = data["feminine_jobs_ru"]
            feminine_jobs_plural = data["feminine_jobs_plural_ru"]
            feminine_names = data['feminine_names_ru']

            masculine_titles = data["masculine_titles_ru"]
            masculine_relation = data["masculine_relation_ru"]
            masculine_relation_plural = data["masculine_relation_plural_ru"]
            masculine_jobs = data["masculine_jobs_ru"]
            masculine_jobs_plural = data["masculine_jobs_plural_ru"]
            masculine_names = data["masculine_names_ru"]

            feminine = (
                    ["она", "ее"]
                    + feminine_relation
                    + feminine_relation_plural
                    + feminine_titles
                    + feminine_jobs
                    + feminine_jobs_plural
                    + feminine_names
            )
            masculine = (
                    ["он", "его"]
                    + masculine_relation
                    + masculine_relation_plural
                    + masculine_titles
                    + masculine_jobs
                    + masculine_jobs_plural
                    + masculine_names
            )
        else:
            raise NameError(
                'The specified language is not supported or misformatted. Try "en", "fr", "pl" or "ru" as language arguments to the filter() method.'
            )

        # Close names file
        f.close()

        assert (
                len(sentences) > 0
        ), "You must provide at least one sentence for the analysis. Check the content of your sentences array you pass to the filter() method."

        for sentence in sentences:

            # Clean the sentence content using regex
            processed_sentence = sentence.lower()
            processed_sentence = re.sub("^", " ", processed_sentence)
            processed_sentence = re.sub("$", " ", processed_sentence)

            # Take care of urls
            words = []
            for word in processed_sentence.split():
                i = word.find("http")
                if i >= 0:
                    word = word[:i] + " " + "__url__"
                words.append(word.strip())
            processed_sentence = " ".join(words)
            processed_sentence = re.sub(r"\[([^\]]*)\] \( *__url__ *\)", r"\1", processed_sentence)

            # Remove illegal chars and extra space
            processed_sentence = re.sub("__url__", "URL", processed_sentence)
            processed_sentence = re.sub(r"[^A-Za-z0-9():,.!?\"\']", " ", processed_sentence)
            processed_sentence = re.sub("URL", "__url__", processed_sentence)
            processed_sentence = re.sub(r"^\s+", "", processed_sentence)
            processed_sentence = re.sub(r"\s+$", "", processed_sentence)
            processed_sentence = re.sub(r"\s+", " ", processed_sentence)

            # Make sure that user input has words in lower case form
            joint_feminine = feminine + feminine_input
            joint_feminine = [word.lower() for word in joint_feminine]
            joint_masculine = masculine + masculine_input
            joint_masculine = [word.lower() for word in joint_masculine]

            # Split the words in the processed_sentence to find the intersection with the feminine array of keywords
            intersection_feminine = set(processed_sentence.split()).intersection(
                set(joint_feminine)
            )

            # Split the words in the processed_sentence to find the intersection with the masculine array of keywords
            intersection_masculine = set(processed_sentence.split()).intersection(
                set(joint_masculine)
            )

            # If the intersection occured, the intersection_feminine and intersection_masculine variables will contain at least one common keyword
            # use this intersection information to get the value for the corresponding flags
            feminine_flag = len(intersection_feminine) > 0
            masculine_flag = len(intersection_masculine) > 0

            # In case the processed_sentence contains the keywords from feminine and masculine arrays, set a union_flag value
            union_flag = (
                    len(intersection_feminine) > 0
                    and len(intersection_masculine) > 0
            )

            # If the processed_sentence didn't contain the keywords neither from feminine, nor from masculine arrays, set a neutral_flag value
            neutral_flag = (
                    len(intersection_feminine) == 0
                    and len(intersection_masculine) == 0
            )

            # Use the union_flag value to set the neutral_flag value, setting to False the feminine and masculine flags
            if union_flag is True:
                feminine_flag = False
                masculine_flag = False
                neutral_flag = True

            # Create the sentence object with the retrieved flag values
            sentence_object = {
                "sentence": sentence,
                "feminine_flag": feminine_flag,
                "masculine_flag": masculine_flag,
                "neutral_flag": neutral_flag,
            }

            # Append the object to the array we return
            flagged_sentences.append(sentence_object)

        return flagged_sentences


    def count(self, group_flag, flagged_corpus):
        """
        generic method for counting the number of sentences
        :param group_flag: a string flag to be counted
        :return: integer value, representing the number of sentences with a particular flag
        """

        flags_count = len(
            [
                flag
                for flag in flagged_corpus
                if flag.get(group_flag) is True
            ]
        )
        return flags_count

    def get_group(self, group_flag, flagged_corpus):
        """
        generic method for counting the number of sentences
        :param group_flag: a string flag to extract corresponding sentences
        :return: array representing the sub group of sentences with a particular flag
        """

        group = [
            flag.get("sentence")
            for flag in flagged_corpus
            if flag.get(group_flag) is True
        ]
        return group

    def count_genders(self, flagged_corpus):
        """
        count the number of sentences in each of groups
        :param flagged_corpus: array of flagged sentences
        :return: 3 integer values, representing feminine, masculine and neutral groups respectively
        """
        feminine_count = self.count("feminine_flag", flagged_corpus)
        masculine_count = self.count("masculine_flag", flagged_corpus)
        neutral_count = self.count("neutral_flag", flagged_corpus)

        return feminine_count, masculine_count, neutral_count

    def sort_groups(self, flagged_corpus):
        """
        sort the sentences in each of 3 groups
        :param flagged_corpus: array of flagged sentences
        :return: 3 arrays of strings, containing feminine, masculine and neutral groups respectively
        """
        feminine_group = self.get_group("feminine_flag", flagged_corpus)
        masculine_group = self.get_group("masculine_flag", flagged_corpus)
        neutral_group = self.get_group("neutral_flag", flagged_corpus)

        return feminine_group, masculine_group, neutral_group

    def filter(self, sentences: []) -> bool:

        # Retrieve the flags for each of the sentences
        flagged_corpus = self.flag_sentences(
            sentences, self.language, self.feminine_input, self.masculine_input
        )

        # Use the retrieved flags to count the number of sentences in each group
        feminine_count, masculine_count, neutral_count = self.count_genders(
            flagged_corpus
        )

        feminine_percentage = 100 * float(feminine_count)/float(len(sentences))
        masculine_percentage = 100 * float(masculine_count)/float(len(sentences))

        # If the rounded percentage of sentences in the target group is lower than in the test group, set bias to True
        # Note, that the neutral group is not taken into account in this calculation
        if round(feminine_percentage) < round(masculine_percentage):
            biased = True
        else:
            biased = False

        return biased
