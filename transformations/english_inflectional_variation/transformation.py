import random, lemminflect
from typing import Dict, List, Optional, Tuple
from tokenizers.pre_tokenizers import BertPreTokenizer
from nltk.tag.mapping import map_tag
from nltk.tag.perceptron import PerceptronTagger
try:
    PerceptronTagger()
except LookupError:
    import nltk
    nltk.download('averaged_perceptron_tagger')

try:
    from nltk.data import find
    find('taggers/universal_tagset/en-ptb.map')
except LookupError:
    import nltk
    nltk.download('universal_tagset')

from interfaces.QuestionAnswerOperation import QuestionAnswerOperation
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType



class EnglishInflectionalVariation(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    heavy = True
    locales = ["en"]
    content_words = {'NOUN', 'VERB', 'ADJ'}
    def __init__(self, seed=0, max_outputs=1):
        super().__init__(seed=seed, max_outputs=max_outputs)
        self.tokenizer = BertPreTokenizer()
        self.tagger = PerceptronTagger()

    def generate(self, sentence: str) -> List[str]:
        '''
        `inflection_distribution` should have the following structure: { PTB tag: int, ... , PTB tag: int }
        '''
        tokenized = self.tokenizer.pre_tokenize_str(sentence)
        tokens = [t[0] for t in tokenized]

        pos_tagged = [(token, map_tag('en-ptb', 'universal', tag)) for (token, tag) in self.tagger.tag(tokens)]
        pos_tagged = [(tagged[0], '.') if '&' in tagged[0] else tagged for tagged in pos_tagged]

        random.seed(self.seed)
        perturbed_tokens = [self.randomly_inflect(tokens, pos_tagged, random.randint(0, i*1000)) for i in range(self.max_outputs)]
        perturbed_tokens = [[(t, tokenized[i][1]) for i, t in enumerate(sentence)] for sentence in perturbed_tokens]

        perturbed_sentences = [self.detokenize(sentence) for sentence in perturbed_tokens]

        #print(f"Perturbed Input from {self.name()} : {perturbed}")
        return perturbed_sentences

    def detokenize(self, tokens: List[Tuple[str, Tuple[int, int]]]) -> str:
        prev_end = 0
        new_tokens = []
        for token, positions in tokens:
            if prev_end != positions[0]:
                new_tokens.append(' ' + token)
            else:
                new_tokens.append(token)
            prev_end = positions[1]
        return ''.join(new_tokens)

    def randomly_inflect(self, tokens: List[str], pos_tagged: List[Tuple[str, str]], seed=0) -> List[str]:
        new_tokens = tokens.copy()
        for i, word in enumerate(tokens):
            lemmas = lemminflect.getAllLemmas(word)
            # Only operate on content words (nouns/verbs/adjectives)
            if lemmas and pos_tagged[i][1] in self.content_words and pos_tagged[i][1] in lemmas:
                lemma = lemmas[pos_tagged[i][1]][0]
                inflections = (i, [(tag, infl) 
                                for tag, tup in 
                                lemminflect.getAllInflections(lemma, upos=pos_tagged[i][1]).items() 
                                for infl in tup])
                if inflections[1]:
                    # Use inflection distribution for weighted random sampling if specified
                    # Otherwise unweighted
                    random.seed(seed+len(word))
                    inflection = random.choices(inflections[1])[0][1]
                    new_tokens[i] = inflection
        return new_tokens


class EnglishInflectionalVariationQAQuestionOnly(QuestionAnswerOperation):
    tasks = [TaskType.QUESTION_ANSWERING, TaskType.QUESTION_GENERATION]
    heavy = True
    locales = ["en"]
    def __init__(self, seed=0, max_outputs=1):
        super().__init__(seed=seed, max_outputs=max_outputs)
        self.question_perturber = EnglishInflectionalVariation(seed=seed, max_outputs=max_outputs)

    def generate(self, context: str, question: str, answers: List[str]):
        '''
        `inflection_distribution` should have the following structure: { PTB tag: int, ... , PTB tag: int }
        Can be used for generating training data since the span indices of answers/context are unchanged.
        '''
        perturbed_questions = self.question_perturber.generate(question)
        
        #print(f"Perturbed Input from {self.name()} : {perturbed_questions}")
        return [(context, pq, answers) for pq in perturbed_questions]
