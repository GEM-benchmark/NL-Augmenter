from transformers import pipeline
import random
import spacy

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


class ContextualPerturbation(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en", "de"]

    def __init__(self, seed=0, max_outputs=1, top_k=10, language ="en", pos_to_change=['ADJ', 'VERB', 'NOUN', 'PROPN'],\
                 percentage=0.2, verbose=False):
        super().__init__(seed, max_outputs=max_outputs)
        self.verbose = verbose
        if self.verbose:
            print("Starting to load the cross-lingual XLM-R (base) model.\n")
        self.unmasker = pipeline('fill-mask', model='xlm-roberta-base', top_k=top_k)
        if self.verbose:
            print("Completed loading the cross-lingual XLM-R (base) model.\n")

        if self.verbose:
            print("Starting to load Spacy model ("+language+") for retrieving linguistic features.\n")
        if language == "en":
            self.linguistic_pipeline = spacy.load("en_core_web_sm")
        elif language == "de":
            self.linguistic_pipeline = spacy.load("en_core_web_sm")
        else:
            raise NotImplementedError("As of now, only English and German are supported.")
        if self.verbose:
            print("Completed loading Spacy model.\n")

        self.pos_to_change = pos_to_change
        assert percentage <=1 and percentage >= 0
        self.percentage = percentage #How many of the elligable POS tags should be changed? Expects values between 0 and 1

    def get_tokens_and_tags(self, input: str):
        tokens = []
        pos_tags = []
        dep_tags = []
        sentence = linguistic_pipeline(input)
        for token in sentence:
            tokens.append(token.text)
            pos_tags.append(token.pos_)
            dep_tags.append(token.dep_)
        return tokens, pos_tags, dep_tags # a list of POS tags as they appear in the input.

    def count_relevant_pos_tags(self, pos_tags):
        for pos in self.pos_to_change:
            pos_count += pos_tags.count(pos)
        return pos_count # Number of POS tags that are considered for perturbation.

    def get_perturbation_candidates(self, input: str):
        perturbation_dict = {}
        tokens, pos_tags, dep_tags = get_tokens_and_tags(input)
        mask_count = min(1, round(self.percentage*count_relevant_pos_tags(pos_tags)))
        if self.verbose:
            print(mask_count," tokens will be masked.\n")
        tokens_to_mask = random.sample([token for i, token in enumerate(tokens) if pos_tags[i] in self.pos_to_change], mask_count)
        for token in tokens_to_mask:
            masked_input = input.replace(token, "<mask>", 1)
            perturbation_dict[token] = self.unmasker(masked_input)

        return perturbation_dict

    def select_and_apply_perturbations(self, input: str):
        perturbation_dict = self.get_perturbation_candidates(input)
        #tokens, pos_tags, dep_tags = get_tokens_and_tags(input)

        replacement_dict = {}
        for original_token in perturbation_dict:
            for replacement_candidate in perturbation_dict[original_token]:
                if replacement_candidate['token_str'] != original_token:
                    replacements[original_token] = replacement_candidate['token_str']
                    break

        if self.verbose:
            print('The following words will be replaced:\n')
            for key in replacement_dict:
                print(key, "is replaced with", replacement_dict[key])

        perturbed_sentence = input
        for original_token in replacement_dict:
            perturbed_sentence = perturbed_sentence.replace(original_token, replacement_dict[original_token], 1)

        return perturbed_sentence

        #p_tokens, p_pos_tags, p_dep_tags = get_tokens_and_tags(perturbed_input)

        #if tokens == p_tokens and pos_tags == p_pos_tags:
        #    Success!
        #else: continue search and if end of cycle, print "not possible + the sentence"

    def generate(self, sentence: str):
        perturbations = self.select_and_apply_perturbations(sentence)
        return perturbations


if __name__ == '__main__':
    fuu = ContextualPerturbation(verbose=True)
    fuu.generate("This is a fun little test run.")