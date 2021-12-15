from typing import Callable, List, Tuple

import numpy as np
import spacy

from common.initialize import spacy_nlp
from interfaces.QuestionAnswerOperation import QuestionAnswerOperation
from tasks.TaskTypes import TaskType


class WordNoise(QuestionAnswerOperation):
    tasks = [TaskType.QUESTION_ANSWERING]
    languages = ["en"]

    CONCAT_POSITION_APPEND = "append"
    CONCAT_POSITION_PREPEND = "prepend"
    CONCAT_POSITION_ANY = "any"
    CONCAT_POSITION_BOTH = "both"

    def __init__(
        self,
        num_words: int = 10,
        concat_position: str = "prepend",
        remove_stop_words: bool = False,
        seed: int = 0,
        max_outputs: int = 1,
    ):
        super().__init__(seed, max_outputs=max_outputs)
        self.n = num_words
        self.concat_pos = concat_position
        self.concat_function = self.get_concat_function()
        self.spacy_model = (
            spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")
        )
        self.remove_stop_words = remove_stop_words
        self.seed = seed

    def get_concat_function(self) -> Callable:
        if self.concat_pos == WordNoise.CONCAT_POSITION_APPEND:
            return self.append_noise
        elif self.concat_pos == WordNoise.CONCAT_POSITION_PREPEND:
            return self.prepend_noise
        elif self.concat_pos == WordNoise.CONCAT_POSITION_ANY:
            return self.prepend_or_append_noise
        elif self.concat_pos == WordNoise.CONCAT_POSITION_BOTH:
            return self.prepend_and_append_noise
        else:
            raise ValueError(
                f"Expected `concat_position` to be one of {WordNoise.CONCAT_POSITION_APPEND}, {WordNoise.CONCAT_POSITION_PREPEND} or {WordNoise.CONCAT_POSITION_ANY}. Got {self.concat_pos}"
            )

    def generate_noise(self, noise_words: List[str]) -> str:
        np.random.seed(self.seed)
        sampled_words = np.random.choice(noise_words, self.n)
        noise = " ".join(sampled_words)
        return noise

    def prepend_noise(self, context: str, noise_words: List[str]) -> str:
        noise = self.generate_noise(noise_words)
        return noise + ". " + context

    def append_noise(self, context: str, noise_words: List[str]) -> str:
        noise = self.generate_noise(noise_words)
        return context + " " + noise + "."

    def prepend_or_append_noise(
        self, context: str, noise_words: List[str]
    ) -> str:
        if np.random.random() > 0.5:
            return self.prepend_noise(context, noise_words)
        else:
            return self.append_noise(context, noise_words)

    def prepend_and_append_noise(
        self, context: str, noise_words: List[str]
    ) -> str:
        noise_prepended_context = self.prepend_noise(context, noise_words)
        noise_appended_context = self.append_noise(
            noise_prepended_context, noise_words
        )
        return noise_appended_context

    def extract_words(self, text: str) -> List[str]:
        doc = self.spacy_model(text)
        # Remove punctuations
        tokens = [token for token in doc if not token.is_punct]
        # Remove stop words
        if self.remove_stop_words:
            tokens = [token for token in tokens if not token.is_stop]

        return [str(token) for token in tokens]

    def generate(
        self, context: str, question: str, answers: [str]
    ) -> List[Tuple[str, str, List[str]]]:
        np.random.seed(self.seed)
        context_words = self.extract_words(context)
        question_words = self.extract_words(question)
        noise_words = context_words + question_words

        new_context = self.concat_function(context, noise_words)

        return [(new_context, question, answers)]
