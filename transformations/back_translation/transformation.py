from transformers import FSMTForConditionalGeneration, FSMTTokenizer

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


class BackTranslation(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]
    heavy = True

    def __init__(self, max_output=1, num_beams=2):
        super().__init__()
        if self.verbose:
            print("Starting to load English to German Translation Model.\n")
        name_en_de = "facebook/wmt19-en-de"
        self.tokenizer_en_de = FSMTTokenizer.from_pretrained(name_en_de)
        self.model_en_de = FSMTForConditionalGeneration.from_pretrained(name_en_de)
        if self.verbose:
            print("Completed loading English to German Translation Model.\n")
            print("Starting to load German to English Translation Model:")
        name_de_en = "facebook/wmt19-de-en"
        self.tokenizer_de_en = FSMTTokenizer.from_pretrained(name_de_en)
        self.model_de_en = FSMTForConditionalGeneration.from_pretrained(name_de_en)
        self.max_output = max_output
        self.num_beams = num_beams
        if self.verbose:
            print("Completed loading German to English Translation Model.\n")

    def back_translate(self, en: str):
        try:
            de = self.en2de(en)
            en_new = self.de2en(de)
        except Exception:
            print("Returning Default due to Run Time Exception")
            en_new = en
        return en_new

    def en2de(self, input):
        input_ids = self.tokenizer_en_de.encode(input, return_tensors="pt")
        outputs = self.model_en_de.generate(input_ids)
        decoded = self.tokenizer_en_de.decode(outputs[0], skip_special_tokens=True)
        if self.verbose:
            print(decoded)  # Maschinelles Lernen ist großartig, oder?
        return decoded

    def de2en(self, input):
        input_ids = self.tokenizer_de_en.encode(input, return_tensors="pt")
        outputs = self.model_de_en.generate(
            input_ids, num_return_sequences=self.max_output, num_beams=self.num_beams
        )
        predicted_outputs = []
        for output in outputs:
            decoded = self.tokenizer_de_en.decode(output, skip_special_tokens=True)
            predicted_outputs.append(decoded) #TODO: this should be able to return multiple sequences
        if self.verbose:
            print(predicted_outputs)  # Machine learning is great, isn't it?
        return predicted_outputs

    def generate(self, sentence: str):
        perturbeds = self.back_translate(sentence)
        return perturbeds
