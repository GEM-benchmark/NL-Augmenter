import random
import string

from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

"""
Mixed Language Perturbation
This perturbation translates words in the text from English to other languages (e.g., German). It can be used to test the robustness of a model in a multilingual setting.
"""


def translate(model, tokenizer, text, src_lang, target_lang):
    tokenizer.src_lang = src_lang
    encoded = tokenizer(text, return_tensors="pt")
    generated_tokens = model.generate(
        **encoded, forced_bos_token_id=tokenizer.get_lang_id(target_lang)
    )
    res = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
    return res


def mixed_language(
    model, tokenizer, text, prob_mix=0.1, src_lang="en", trg_lang="fr", seed=0
):
    random.seed(seed)

    words = text.split()
    mixed_text = ""
    for word in words:
        if mixed_text != "":
            mixed_text += " "
        if random.random() < prob_mix:
            plain_word = word.translate(
                str.maketrans("", "", string.punctuation)
            ).strip()

            if plain_word == "":
                continue

            if not word[0].isupper():  # lower case
                mixed_text += translate(
                    model, tokenizer, plain_word, src_lang, trg_lang
                )[0].lower()
            else:
                mixed_text += translate(
                    model, tokenizer, plain_word, src_lang, trg_lang
                )[0]

            if word[-1] in string.punctuation:
                mixed_text += word[-1]
        else:
            mixed_text += word
    return mixed_text


class MixedLanguagePerturbation(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]
    tgt_languages = ["es", "de", "fr", "zh"]
    heavy = True

    def __init__(
        self, seed=0, prob_mix=0.3, src_lang="en", trg_lang="de", max_outputs=1
    ):
        super().__init__(seed, max_outputs=max_outputs)

        self.model = M2M100ForConditionalGeneration.from_pretrained(
            "facebook/m2m100_418M"
        )
        self.tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M")

        self.prob_mix = prob_mix
        self.src_lang = src_lang
        self.trg_lang = trg_lang

    def generate(self, sentence: str):
        pertubed = mixed_language(
            self.model,
            self.tokenizer,
            text=sentence,
            prob_mix=self.prob_mix,
            src_lang=self.src_lang,
            trg_lang=self.trg_lang,
            seed=self.seed,
        )
        return [pertubed]


"""
# Sample code to demonstrate usage. Can also assist in adding test cases.
if __name__ == '__main__':
    import json
    from TestRunner import convert_to_snake_case
    tf = MixedLanguagePerturbation()
    sentence = "Andrew finally returned the French book to Chris that I bought last week"
    test_cases = []
    for sentence in ["Andrew finally returned the Comic book to Chris that I bought last week",
                     "Chris borrowed the Comic book from Andrew last weekend",
                     "Turn off the light please",
                     "I love cat",
                     "Thomas loves to cook chicken every Monday"]:
        test_cases.append({
            "class": tf.name(),
            "inputs": {"sentence": sentence}, "outputs": [{"sentence": tf.generate(sentence)}]}
        )
    json_file = {"type": "mixed_language_perturbation", "test_cases": test_cases}
    # json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
    print(json.dumps(json_file))

    with open("task.json", "w") as out_file:
        json.dump(json_file, out_file, indent=2, ensure_ascii=True)
"""
