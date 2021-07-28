from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


class GenderBiasFilter(SentenceOperation):
    tasks = [TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en", "fr"]

    def __init__(self, language):
        super().__init__()
        self.language = language

    @staticmethod
    def flag_sentences(sentences, language):
        """
        flag sentences as belonging to the feminine, masculine or neutral groups
        :param sentences: sentences array
        :param language: the string key representing the supported langage
        :return: array of objects, each containing the analyzed sentence along with three flags
        """
        flagged_sentences = []
        
        # Define the words, that represent feminine and masculine groups in both languages
        if language == "en":
            feminine_relation = ["woman", "auntie", "niece", "girl", "daughter", "girlfriend", 
                                 "mistress", "sister", "bride", "wife", "mother", "mum", "mom", "mommy", 
                                 "grandmother", "granny"]
            feminine_relation_plural = ["women", "aunties", "nieces", "girls", "daughters", "girlfriends",
                                 "mistresses", "sisters", "brides", "wives", "mothers", "mums", "moms", "mommies", 
                                 "grandmothers", "grannies"]
            masculine_relation = ["man", "uncle", "nephew","boy", "boyfriend", "master", "brother",
                                  "groom", "bridegroom", "husband", "father", "dad", "daddy", "grandfather"]
            masculine_relation_plural = ["men", "uncles", "nephews", "boys", "boyfriends", "masters", "brothers",
                                  "grooms", "bridegrooms", "husbands", "fathers", "dads", "daddies", "grandfathers"]

            feminine_titles = ["mrs", "ms", "miss", "mademoiselle", "fräulein", "madam", "lady", "gentlewoman", 
                               "baronesse", "countess", "viscountess", "marquise", "duchess", "princess", "emperess", "queen", 
                               "dame", "primadonna", "diva", "goodwife", "guidwife"]
            masculine_titles = ["mr", "mister", "sir", "lord", "gentleman", 
                                "baron", "count", "viscount", "marquess", "duke", "prince", "emperor", "king", "goodman"]

            feminine = ["she", "her", "hers"] + feminine_relation + feminine_relation_plural + feminine_titles
            masculine = ["he", "him", "his"] + masculine_relation + masculine_relation_plural + masculine_titles

        elif language == "fr":
            feminine_relation = ["femme", "meuf", "nana", "tante", "fille", "fillette", "gamine", "gonzesse", 
                                 "amie", "pote", "compagne", "maîtresse", "amante", "soeur ", "épouse", "mariée", 
                                 "mère", "maman", "daronne", "nièce", "tante", "grand-mère", "mamie"]
            feminine_relation_plural = ["femmes", "meufs", "nanas", "tantes", "filles", "fillettes", "gamines", "gonzesses", 
                                 "amies", "potes", "compagnes", "maîtresses", "amantes", "soeurs", "épouses", "mariées", 
                                 "mères", "mamans", "daronnes", "nièces", "tantes", "grand-mères", "mamies"]
            masculine_relation = ["homme", "mec", "oncle", "neveu", "garçon", "fils", "gars", "gamin", 
                                  "ami", "pot", "maître", "frère", "amant", "époux", "mari", "marié" 
                                  "père", "papa", "daron", "grand-père", "papie"]
            masculine_relation_plural = ["hommes", "mecs", "oncles", "neveux", "garçons", "fils", "gars", "gamins", 
                                  "amis", "pots", "maîtres", "frères", "amants", "époux", "maris", "mariés" 
                                  "pères", "papas", "darons", "grand-pères", "papies"]
            feminine_titles = ["m", "mlle", "madame", "mademoiselle", "baronesse", "comtesse", "marquise", "duchesse", "princesse", "emperesse", "reine", "dame"]
            masculine_titles = ["mr", "monsieur", "monseigneur", "baron", "compte", "marquis", "duc", "prince", "dauphin" "empereur", "roi"]

            feminine = ["elle", "madame", "sienne"] + feminine_relation + feminine_relation_plural + feminine_titles
            masculine = ["il", "monsieur", "sien"] + masculine_relation + masculine_relation_plural + masculine_titles

        else:
            raise NameError('The specified language is not supported or misformatted. Try "en" or "fr" as language arguments to the filter() method.')

        assert len(sentences) > 0, "You must provide at least one sentence for the analysis. Check the content of your sentences array you pass to the filter() method."

        for sentence in sentences:

            # Initialize the variables
            feminine_flag = False
            masculin_flag = False
            union_flag = False
            neutral_flag = False
            intersection_feminine = set()
            intersection_masculine = set()

            # Lowercase and split the words in the sentence to find the intersection with the feminine array of keywords
            intersection_feminine = set(sentence.lower().split()).intersection(
                    set(feminine)
                )
            
            # Lowercase and split the words in the sentence to find the intersection with the masculine array of keywords
            intersection_masculine = set(sentence.lower().split()).intersection(
                    set(masculine))
           
            intersection_masculine = set(sentence.lower().split()).intersection(
                set(masculine))
            
            # If the intersection occured, the intersection_feminine and intersection_masculine variables will contain at least one common keyword
            # use this intersection information to get the value for the corresponding flags
            feminine_flag = len(intersection_feminine) > 0
            masculin_flag = len(intersection_masculine) > 0

            # In case the sentence contains the keywords from feminine and masculine arrays, set a union_flag value
            union_flag = (
                len(intersection_feminine) > 0
                and len(intersection_masculine) > 0
            )

            # If the sentence didn't contain the keywords neither from feminine, nor from masculine arrays, set a neutral_flag value
            neutral_flag = (
                len(intersection_feminine) == 0
                and len(intersection_masculine) == 0
            )

            # Use the union_flag value to set the neutral_flag value, setting to False the feminine and masculine flags
            if union_flag is True:
                feminine_flag = False
                masculin_flag = False
                neutral_flag = True

            # Create the sentence object with the retrieved flag values
            sentence_object = {
                "sentence": sentence,
                "feminine_flag": feminine_flag,
                "masculin_flag": masculin_flag,
                "neutral_flag": neutral_flag,
            }

            # Append the object to the array we return
            flagged_sentences.append(sentence_object)

        return flagged_sentences

    @staticmethod
    def count_genders(flagged_corpus):
        """
        count the number of sentences in each of groups
        :param flagged_corpus: array of flagged sentences
        :return: 3 integer values, representing feminine, masculine and neutral groups respectively
        """
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

    @staticmethod
    def sort_groups(flagged_corpus):
        """
        sort the sentences in each of 3 groups
        :param flagged_corpus: array of flagged sentences
        :return: 3 arrays of strings, containing feminine, masculine and neutral groups respectively
        """
        feminine_group = [
                flag.get("sentence")
                for flag in flagged_corpus
                if flag.get("feminine_flag") is True
            ]
        masculine_group = [
                flag.get("sentence")
                for flag in flagged_corpus
                if flag.get("masculine_flag") is True
            ]
        neutral_group = [
                flag.get("sentence")
                for flag in flagged_corpus
                if flag.get("neutral_flag") is True
            ]
    
        return feminine_group, masculine_group, neutral_group

    def filter(self, sentences: []) -> bool:
        biased = False

        # Retrieve the flags for each of the sentences
        flagged_corpus = self.flag_sentences(sentences, self.language)

        # Use the retrieved flags to count the number of sentences in each group
        feminine_count, masculine_count, neutral_count = self.count_genders(
            flagged_corpus
        )

        # If the mumber of sentences in the target group is lower than in the test group, set bias to True
        # Note, that the neutral group is not taken into account in this calculation
        if feminine_count < masculine_count:
            biased = True
        else:
            biased = False

        return biased