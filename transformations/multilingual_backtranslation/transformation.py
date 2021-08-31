from nltk import edit_distance
from transformers import MarianMTModel, MarianTokenizer

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
from transformations.multilingual_backtranslation.helpers.supported_languages import (
    SUPPORTED_LANGUAGES,
    check_support,
)

# This codebase is based on the previous backtranslation codebase.
# https://github.com/GEM-benchmark/NL-Augmenter/tree/main/transformations/back_translation


class MultilingualBacktranslation(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = SUPPORTED_LANGUAGES
    heavy = True

    """
        Multilingual backtranslation. Supports backtranslation for 232 language codes (201 unique languages) through MarianMT models.

        Args:
            src_lang_code: The ISO-code of the original language
            tgt_lang_code: The ISO-code of the intermediate language
            seed: The seed for the random generator
            max_outputs: The maximum number of outputs to return
            num_beams: The number of beams to use for beam search
            use_larger_model_if_available: If true, a larger, multilingual model is used if available. If false, the smaller model is used if available.
            verbose: If true, prints out the decoded outputs
    """

    def __init__(
        self,
        src_lang_code: str = "en",
        tgt_lang_code: str = "es",
        seed: int = 4,
        max_outputs: int = 1,
        num_beams: int = 4,
        use_larger_model_if_available: bool = True,
        verbose: bool = False,
        sort_by_edit_distance: bool = True,
    ):
        super().__init__(seed, max_outputs=max_outputs)
        self.sort_by_edit_distance = sort_by_edit_distance
        assert max_outputs <= num_beams, "max_outputs must be <= num_beams"

        (
            self.src,
            self.tgt,
            self.src_lang_code,
            self.tgt_lang_code,
        ) = check_support(
            src_lang_code, tgt_lang_code, use_larger_model_if_available
        )
        if verbose:
            print(
                f"Starting to load {src_lang_code} to {tgt_lang_code} Translation Model.\n"
            )
        src_model_name = (
            f"Helsinki-NLP/opus-mt-{self.src_lang_code}-{self.tgt_lang_code}"
        )
        tgt_model_name = (
            f"Helsinki-NLP/opus-mt-{self.tgt_lang_code}-{self.src_lang_code}"
        )
        self.tokenizer_src_tgt = MarianTokenizer.from_pretrained(
            src_model_name
        )
        self.model_src_tgt = MarianMTModel.from_pretrained(src_model_name)

        if self.verbose:
            print(
                f"Completed loading {self.src_lang_code} to {self.tgt_lang_code} Translation Model.\n"
            )
            print(
                f"Starting to load {self.tgt_lang_code} to {self.src_lang_code} Translation Model:"
            )
        # try:
        self.tokenizer_tgt_src = (
            MarianTokenizer.from_pretrained(tgt_model_name)
            if tgt_model_name != src_model_name
            else self.tokenizer_src_tgt
        )
        self.model_tgt_src = (
            MarianMTModel.from_pretrained(tgt_model_name)
            if tgt_model_name != src_model_name
            else self.model_src_tgt
        )
        self.num_beams = num_beams
        if self.verbose:
            print("Completed loading German to English Translation Model.\n")

    def back_translate(self, src_sentence: str):
        src_sentence = (
            self.tgt + src_sentence if self.tgt is not None else src_sentence
        )
        intermediate = self.src2tgt(src_sentence)
        intermediate = [
            self.src + x if self.src is not None else x for x in intermediate
        ]
        en_new = [
            self.tgt2src(intermediate[i]) for i in range(len(intermediate))
        ]
        return en_new

    def src2tgt(self, input):
        input_ids = self.tokenizer_src_tgt.encode(input, return_tensors="pt")
        outputs = self.model_src_tgt.generate(
            input_ids, num_return_sequences=3, num_beams=5
        )
        decoded = [
            self.tokenizer_src_tgt.decode(outputs[i], skip_special_tokens=True)
            for i in range(len(outputs))
        ]
        if self.verbose:
            print(decoded)  # Maschinelles Lernen ist großartig, oder?
        return decoded

    def tgt2src(self, input):
        input_ids = self.tokenizer_tgt_src.encode(input, return_tensors="pt")
        outputs = self.model_tgt_src.generate(
            input_ids,
            num_return_sequences=self.max_outputs,
            num_beams=self.num_beams,
        )
        predicted_outputs = []
        for output in outputs:
            decoded = self.tokenizer_tgt_src.decode(
                output, skip_special_tokens=True
            )
            # TODO: this should be able to return multiple sequences
            predicted_outputs.append(decoded)
        if self.verbose:
            print(predicted_outputs)  # Machine learning is great, isn't it?
        return predicted_outputs

    def generate(self, sentence: str):

        perturbs = self.back_translate(sentence)
        out = [x[0] for x in perturbs if x[0] != sentence]
        if self.sort_by_edit_distance:
            out = sorted(out, key=lambda x: edit_distance(x, sentence))
        return out[: self.max_outputs]


"""
# This code snippet can be uncommented to test the backtranslation function.
if __name__ == "__main__":
    backtranslator = MultilingualBacktranslation()
    # sentence = "Yo soy un estudiante y trabajo en la cafeteria al lado del mercado. "
    sentence = "Neuroplasticity is a continuous processing allowing short-term, medium-term, and long-term remodeling of the neuronosynaptic organization."
    out = backtranslator.generate(sentence)
    print(out)

"""
