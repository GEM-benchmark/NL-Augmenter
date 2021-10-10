import requests

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


def britishize_americanize(string, final_dict):
    """
    Parameters:
        string(str): original string
        final_dict(dict): dictionary with all the different possible words in american and british english
    Returns:
        str: String after replacing the words
    """
    string = " ".join([final_dict.get(word, word) for word in string.split()])
    return string


class AmericanizeBritishizeEnglish(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION, TaskType.SENTIMENT_ANALYSIS,
             TaskType.QUESTION_ANSWERING, TaskType.QUESTION_GENERATION, TaskType.PARAPHRASE_DETECTION]
    languages = ["en"]
    keywords = ["lexical", "rule-based", "syntactic", "api-based", "external-knowledge-based",
                "highly-meaning-preserving", "high-precision", "low-coverage"]

    def __init__(self, n=1, seed=0, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)

        # Creating a custom vocab dictionary consisting of totally different words for same context
        difference_british_to_american = {
            "trousers": "pants",
            "flat": "apartment",
            "bonnet": "hood",
            "boot": "trunk",
            "lorry": "truck",
            "university": "college",
            "holiday": "vacation",
            "jumper": "sweater",
            "trainers": "sneakers",
            "postbox": "mailbox",
            "biscuit": "cookie",
            "chemist": "drugstore",
            "shop": "store",
            "football": "soccer",
            "autumn": "fall",
            "barrister": "attorney",
            "bill": "check",
            "caravan": "trailer",
            "cupboard": "closet",
            "diversion": "detour",
            "dustbin": "trash can",
            "jug": "pitcher",
            "lift": "elevator",
            "mad": "crazy",
            "maize": "corn",
            "maths": "math",
            "motorbike": "motorcycle",
            "motorway": "freeway",
            "nappy": "diaper",
            "pavement": "sidewalk",
            "post": "mail",
            "postman": "mailman",
            "pub": "bar",
            "rubber": "eraser",
            "solicitor": "attorney",
            "tax": "cab",
            "timetable": "schedule",
            "torch": "flashlight",
            "waistcoat": "vest",
            "windscreen": "windshield",
            "angry": "mad",
            "caretaker": "janitor",
            "cot": "crib",
            "curtains": "drapes",
            "engine": "motor",
            "garden": "yard",
            "handbag": "purse",
            "hoarding": "billboard",
            "ill": "sick",
            "interval": "intermission",
            "luggage": "baggage",
            "nowhere": "noplace",
            "optician": "optometrist",
            "queue": "line",
            "rubbish": "trash",
        }
        # Replacing the keys with values and vice versa for the custom vocab dictionary
        # And merging both of them
        vocab_diff = dict(
            (v, k) for k, v in difference_british_to_american.items()
        )
        vocab_diff.update(difference_british_to_american)

        """
         Gets the british to american english dictionary
         Gets the american to British english dictionary
         Merges both these dictionaries with the custom vocab dictionary.
        """
        try:
            url = "https://raw.githubusercontent.com/hyperreality/American-British-English-Translator/master/data/american_spellings.json"
            american_british_dict = requests.get(url).json()

            url = "https://raw.githubusercontent.com/hyperreality/American-British-English-Translator/master/data/british_spellings.json"
            british_american_dict = requests.get(url).json()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        self.final_dict = {**american_british_dict, **british_american_dict, **vocab_diff}

    def generate(self, sentence: str):
        translated = britishize_americanize(sentence,  self.final_dict)
        return ["".join(translated)]


# if __name__ == "__main__":
#     import json
#     from TestRunner import convert_to_snake_case
#
#     tf = AmericanizeBritishizeEnglish()
#     test_cases = []
#     input_sent = ["I love the pastel colours",
#                   "That shop is so unorganised",
#                   "Carry encyclopedia on vacation",
#                   "He was so ill that he had to be hospitalized"]
#
#     for i, sentence in enumerate(input_sent):
#         transformed_sentence = tf.generate(sentence)
#         test_cases.append(
#             {"class": tf.name(), "inputs": {"sentence": sentence}, "outputs": []}
#         )
#         for trans_sentence in transformed_sentence:
#             test_cases[i]["outputs"].append({"sentence": trans_sentence})
#     json_file = {
#         "type": convert_to_snake_case("add_hashtags"),
#         "test_cases": test_cases,
#     }
#     print(json.dumps(json_file))
