import random
import numpy as np
import torch
from random import sample
from transformers import FSMTForConditionalGeneration, FSMTTokenizer

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

from transformations.diverse_paraphrase.submod.submodopt import SubmodularOpt
from transformations.diverse_paraphrase.submod.submodular_funcs import trigger_dips


class DiverseParaphrase(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]
    heavy = True

    def __init__(self, augmenter="dips", num_outputs=4):
        super().__init__()

        seed = 42
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        torch.use_deterministic_algorithms(True)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)

        assert augmenter in ["dips", "random", "diverse_beam", "beam"]
        if self.verbose:
            choices = ["dips", "random", "diverse_beam", "beam"]
            print(
                "The base paraphraser being used is Backtranslation - Generating {} candidates based on {}\n".format(
                    num_outputs, augmenter
                )
            )
            print("Primary options for augmenter : {}. \n".format(str(choices)))
            print(
                "Default: augmenter='dips', num_outputs=4. Change using DiverseParaphrase(augmenter=<option>, num_outputs=<num_outputs>)\n"
            )
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

        if self.verbose:
            print("Completed loading German to English Translation Model.\n")

        self.augmenter = augmenter
        if self.augmenter == "dips":
            if self.verbose:
                print("Loading word2vec gensim model. Please wait...")
            trigger_dips()
            if self.verbose:
                print("Completed loading word2vec gensim model.\n")
        self.num_outputs = num_outputs

    def en2de(self, input):
        input_ids = self.tokenizer_en_de.encode(input, return_tensors="pt")
        outputs = self.model_en_de.generate(input_ids)
        decoded = self.tokenizer_en_de.decode(outputs[0], skip_special_tokens=True)
        if self.verbose:
            print(decoded)
        return decoded

    def generate_diverse(self, en: str):
        try:
            de = self.en2de(en)
            if self.augmenter == "diverse_beam":
                en_new = self.generate_diverse_beam(de)
            else:
                en_new = self.select_candidates(de, en)
        except Exception:
            if self.verbose:
                print("Returning Default due to Run Time Exception")
            en_new = [en for _ in range(self.num_outputs)]
        return en_new

    def select_candidates(self, input: str, sentence: str):
        input_ids = self.tokenizer_de_en.encode(input, return_tensors="pt")
        outputs = self.model_de_en.generate(
            input_ids,
            num_return_sequences=self.num_outputs * 5,
            num_beams=self.num_outputs * 5,
        )

        predicted_outputs = []
        decoded = [
            self.tokenizer_de_en.decode(output, skip_special_tokens=True)
            for output in outputs
        ]
        if self.augmenter == "dips":
            try:
                subopt = SubmodularOpt(decoded, sentence)
                subopt.initialize_function(0.4, a1=0.5, a2=0.5, b1=1.0, b2=1.0)
                predicted_outputs = list(subopt.maximize_func(self.num_outputs))
            except Exception as e:
                if self.verbose:
                    print("Error in SubmodularOpt: {}".format(e))
                predicted_outputs = decoded[: self.num_outputs]
        elif self.augmenter == "random":
            predicted_outputs = sample(decoded, self.num_outputs)
        else:  # Fallback to top n points in beam search
            predicted_outputs = decoded[: self.num_outputs]

        if self.verbose:
            print(predicted_outputs)

        return predicted_outputs

    def generate_diverse_beam(self, sentence: str):
        input_ids = self.tokenizer_de_en.encode(sentence, return_tensors="pt")

        try:
            outputs = self.model_de_en.generate(
                input_ids,
                num_return_sequences=self.num_outputs,
                num_beam_groups=2,
                num_beams=self.num_outputs,
            )
        except:
            outputs = self.model_de_en.generate(
                input_ids,
                num_return_sequences=self.num_outputs,
                num_beam_groups=1,
                num_beams=self.num_outputs,
            )

        predicted_outputs = [
            self.tokenizer_de_en.decode(output, skip_special_tokens=True)
            for output in outputs
        ]

        if self.verbose:
            print(predicted_outputs)

        return predicted_outputs

    def generate(self, sentence: str):
        candidates = self.generate_diverse(sentence)
        return candidates
