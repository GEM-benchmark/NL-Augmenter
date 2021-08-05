import random

import spacy
from transformers import pipeline

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


class ContextualMeaningPerturbation(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en", "de"]
    heavy = True

    def __init__(
        self,
        seed=0,
        max_outputs=1,
        top_k=10,
        language="en",
        pos_to_change=["ADV", "ADJ", "VERB", "NOUN", "PROPN"],
        perturbation_rate=0.3,
        verbose=False,
    ):
        super().__init__(seed, max_outputs=max_outputs)
        self.verbose = verbose
        self.seed = seed
        if self.verbose:
            print("Starting to load the cross-lingual XLM-R (base) model.\n")
        self.unmasker = pipeline(
            "fill-mask", model="xlm-roberta-base", top_k=top_k
        )
        if self.verbose:
            print("Completed loading the cross-lingual XLM-R (base) model.\n")

        if self.verbose:
            print(
                "Starting to load Spacy model ("
                + language
                + ") for retrieving linguistic features.\n"
            )
        if language == "en":
            self.linguistic_pipeline = spacy.load("en_core_web_sm")
        elif language == "de":
            try:
                self.linguistic_pipeline = spacy.load("de_core_news_sm")
            except ImportError:
                print(
                    "To perturb German text, please download SpaCy's German pipeline de_core_news_sm, \
            for example by using the following command: python -m spacy download de_core_news_sm"
                )
        else:
            raise NotImplementedError(
                "As of now, only English and German are supported."
            )
        if self.verbose:
            print("Completed loading Spacy model.\n")

        self.pos_to_change = pos_to_change
        assert perturbation_rate <= 1 and perturbation_rate >= 0
        self.percentage = perturbation_rate  # How many of the elligable POS tags should be changed? Expects values between 0 and 1

    def get_linguistic_features(self, input: str):
        """
        Linguistic analysis of the input sentence.
        Returns a list of tokens, POS tags and lemmatised tokens.
        """
        tokens = []
        pos_tags = []
        lemmas = []
        sentence = self.linguistic_pipeline(input)
        for token in sentence:
            tokens.append(token.text)
            pos_tags.append(token.pos_)
            lemmas.append(token.lemma)
        return tokens, pos_tags, lemmas

    def count_eligible_tokens(self, pos_tags):
        """
        Returns the number of words that will be replaced.
        """
        pos_count = 0
        for pos in self.pos_to_change:
            pos_count += pos_tags.count(pos)
        return pos_count

    def get_perturbation_candidates(self, input: str):
        """
        Samples tokens that will be replaced.
        Generates and returns the top k contextual replacement candidates.
        """
        perturbation_dict = {}
        tokens, pos_tags, lemmas = self.get_linguistic_features(input)
        if self.count_eligible_tokens(pos_tags) == 0:
            print(
                "Warning: The sequence' ",
                input,
                " 'will remain unchanged as it didn't include the following POS tags:",
                self.pos_to_change,
            )
            num_word_swaps = 0
        else:
            num_word_swaps = max(
                1,
                round(self.percentage * self.count_eligible_tokens(pos_tags)),
            )
        if self.verbose:
            print(num_word_swaps, " tokens will be masked.\n")
        random.seed(self.seed)
        tokens_to_mask = random.sample(
            [
                token
                for i, token in enumerate(tokens)
                if pos_tags[i] in self.pos_to_change
            ],
            num_word_swaps,
        )
        for token in tokens_to_mask:
            masked_input = input.replace(token, "<mask>", 1)
            perturbation_dict[token] = self.unmasker(masked_input)

        return perturbation_dict

    def select_and_apply_perturbations(self, input: str):
        """
        Applies perturbations and returns the perturbed sentence
        By default, the best fitting candidate is used.
        If the top k candidate list includes a token with the same POS tag but different word family
        as the original token, it will be used instead of the default.
        """
        perturbation_dict = self.get_perturbation_candidates(input)
        tokens, pos_tags, lemmas = self.get_linguistic_features(input)

        replacement_dict = {}
        for original_token in perturbation_dict:
            replacement_dict[original_token] = perturbation_dict[
                original_token
            ][0]["token_str"]

            # Replace with the first best choice in case no better candidate is found
            for replacement_candidate in perturbation_dict[original_token]:
                p_tokens, p_pos_tags, p_lemmas = self.get_linguistic_features(
                    replacement_candidate["sequence"]
                )

                # The selected word should have the same POS tag but originate from a different word family
                if p_lemmas != lemmas and p_pos_tags == pos_tags:
                    replacement_dict[original_token] = replacement_candidate[
                        "token_str"
                    ]
                    break

        if self.verbose:
            print("The following words will be replaced:\n")
            for key in replacement_dict:
                print(key, "is replaced with", replacement_dict[key])

        perturbed_sentence = input
        for original_token in replacement_dict:
            perturbed_sentence = perturbed_sentence.replace(
                original_token, replacement_dict[original_token], 1
            )

        return perturbed_sentence

    def generate(self, sentence: str):
        perturbation = self.select_and_apply_perturbations(sentence)

        if self.verbose:
            print("Original:/t", sentence)
            print("Perturbation:/t", perturbation)
        return [perturbation]
