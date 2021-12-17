import random
from typing import Optional

from aaransia import get_alphabets, transliterate

from nlaugmenter.interfaces.SentenceOperation import SentenceOperation
from nlaugmenter.tasks.TaskTypes import TaskType


class MixTransliteration(SentenceOperation):
    """
    This transformation transforms native scripts in any of the following languages to it's transliterated form in english
    1. Afrikaans	    2. Algerian	        3. Arabic
    4. Azerbaijani	    5. Bosnian	        6. Catalan
    7. Corsican	        8. Czech	        9. Welsh
    10. Danish	        11. German	        12. Greek
    13. English	        14. Esperanto       15. Spanish
    16. Estonian	    17. Basque	        18. Persian
    19. Finnish	        20. French	        21. Frisian
    22. Irish	        23. Gaelic	        24. Galician
    25. Hausa	        26. Croatian	    27. Creole
    28. Hungarian	    29. Hawaiian	    30. Indonesian
    31. Igbo	        32. Icelandic	    33. Italian
    34. Kinyarwanda	    35. Kurdish	        36. Latin
    37. Libyan	        38. Lithuanian	    39. Luxembourgish
    40. Latvian	        41. Moroccan	    42. Malagasy
    43. Maori	        44. Malay	        45. Maltese
    46. Dutch	        47. Norwegian	    48. Polish
    49. Portuguese	    50. Romanian	    51. Samoan
    52. Shona	        53. Slovak	        54. Slovenian
    55. Somali	        56. Albanian	    57. Sesotho
    58. Sundanese	    59. Swedish	        60. Swahili
    61. Filipino	    62. Tunisian	    63. Turkish
    64. Turkmen	        65. Urdu	        66. Uzbek
    67. Vietnamese	    68. Xhosa	        69. Yoruba
    70. Zulu

    args:
        source_lang (str):  source language in input text
        target_lang (str, default = "en"): target language in transformed text
        seed (int, default = 42): seed for reproducibility
    """

    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    LANG_MAPPING = get_alphabets()

    def __init__(
        self,
        source_lang: str,
        target_lang: Optional[str] = "en",
        seed: Optional[int] = 42,
    ):
        super().__init__()
        random.seed(seed)
        assert source_lang in self.LANG_MAPPING.keys(), NotImplementedError(
            f"Incorrect source language, choose one of {list(self.LANG_MAPPING.keys())}"
        )
        assert target_lang in self.LANG_MAPPING.keys(), NotImplementedError(
            f"Incorrect target language, choose one of {list(self.LANG_MAPPING.keys())}"
        )
        print(
            f"Transformation initialized from {self.LANG_MAPPING[source_lang]} to {self.LANG_MAPPING[target_lang]}"
        )
        self.source_lang = source_lang
        self.target_lang = target_lang

    @staticmethod
    def get_languages(self):
        return self.LANG_MAPPING

    def generate(self, sentence: str, prob_mix: int = 1):
        temp_text = transliterate(
            sentence,
            source=self.source_lang,
            target=self.target_lang,
            universal=True,
        )
        temp_tokens = temp_text.split(" ")
        input_tokens = sentence.split(" ")
        output_tokens = []
        mixed = False  # if foreign script exists, ensure at least one is transliterated
        for i in range(len(temp_tokens)):
            if temp_tokens[i] != input_tokens[i] and (
                random.random() < prob_mix or mixed is False
            ):
                output_tokens.append(temp_tokens[i])
                mixed = True
            else:
                output_tokens.append(input_tokens[i])
        output = " ".join(output_tokens)
        return [output]
