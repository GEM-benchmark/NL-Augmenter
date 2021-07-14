from typing import Tuple, List, Callable
from interfaces.QuestionAnswerOperation import QuestionAnswerOperation
from tasks.TaskTypes import TaskType
import spacy
from random import Random


class WordNoise(QuestionAnswerOperation):
    tasks = [TaskType.QUESTION_ANSWERING]
    languages = ["en"]

    CONCAT_POSITION_APPEND = 'append'
    CONCAT_POSITION_PREPEND = 'prepend'
    CONCAT_POSITION_ANY = 'any'

    def __init__(self, num_words: int, concat_position: str, remove_stop_words: bool = False, seed:int = 0, max_outputs: int =1):
        super().__init__(seed, max_outputs=max_outputs)
        self.n = num_words
        self.concat_pos = concat_position
        self.concat_function = self.get_concat_function()
        self.spacy_model = spacy.load('en_core_web_sm')
        self.remove_stop_words = remove_stop_words
        self.random = Random(seed)

    def get_concat_function(self) -> Callable:
        if self.concat_pos == WordNoise.CONCAT_POSITION_APPEND:
            return WordNoise.append_noise
        elif self.concat_pos == WordNoise.CONCAT_POSITION_PREPEND:
            return WordNoise.prepend_noise
        elif self.concat_pos == WordNoise.CONCAT_POSITION_ANY:
            return self.prepend_or_append_noise
        else:
            raise ValueError(f'Expected `concat_position` to be one of {WordNoise.CONCAT_POSITION_APPEND}, {WordNoise.CONCAT_POSITION_PREPEND} or {WordNoise.CONCAT_POSITION_ANY}. Got {self.concat_pos}')

    @staticmethod
    def prepend_noise(context: str, noise: str) -> str:
        return noise + '. ' + context

    @staticmethod
    def append_noise(context: str, noise: str) -> str:
        return context + ' ' + noise + '.'

    def prepend_or_append_noise(self, context: str, noise: str) -> str:
        if self.random.random() > 0.5:
            return WordNoise.prepend_noise(context, noise)
        else:
            return WordNoise.append_noise(context, noise)

    def extract_words(self, text: str) -> List[str]:
        doc = self.spacy_model(text)
        # Remove punctuations
        tokens = [token for token in doc if not token.is_punct]
        # Remove stop words
        if self.remove_stop_words:
            tokens = [token for token in tokens if not token.is_stop]

        return [str(token) for token in tokens]

    def generate(self, context: str, question: str, answers: [str]) -> List[Tuple[str, str, List[str]]]:
        context_words = self.extract_words(context)
        question_words = self.extract_words(question)
        noise_words = self.random.choices(context_words + question_words, k=self.n)
        noise = ' '.join(noise_words)

        context = self.concat_function(context, noise)

        return [(context, question, answers)]

