from collections import Counter

from nltk import ngrams
from transformers import BasicTokenizer

from interfaces.SentenceOperation import SentenceAndTargetOperation
from tasks.TaskTypes import TaskType


class OscillatoryHallucinationFilter(SentenceAndTargetOperation):

    """N-gram Count based Heuristic for Detecting Oscillatory Hallucinations
    Paper: https://arxiv.org/pdf/2104.06683.pdf
    The paper did not explicitly tokenize since IWSLT is available in tokenized form.
    Tokenization used here = Whitespace + Punctuation, as in multilingual BERT pre-tokenization.
    Finally, one more difference with the paper: Count Threshold is also set along with Difference Threshold.
    Thresholds are set to very high values to ensure very High Precision of the Filter, but this can be tweaked.
    """

    tasks = [TaskType.TEXT_TO_TEXT_GENERATION]
    keywords = ["generation", "translation", "language-agnostic"]
    heavy = True

    def __init__(
        self,
        ngram_size=2,
        count_threshold=10,
        difference_threshold=5,
        min_length_threshold=10,
    ):
        super().__init__()
        self.tokenizer = BasicTokenizer()
        self.ngram_size = ngram_size
        self.count_threshold = count_threshold
        self.difference_threshold = difference_threshold
        self.min_length_threshold = min_length_threshold

    def filter(self, source: str = None, output: str = None) -> bool:

        src = self.tokenizer.tokenize(source)
        tgt = self.tokenizer.tokenize(output)

        # Minimum Length Threshold is Not Really Required, Since Count Threshold will usually take care of it
        # But still useful in practice, in case count threshold is too low
        if len(tgt) < self.min_length_threshold:
            return False

        src_bigrams = ngrams(src, self.ngram_size)
        src_max_bigram_count = Counter(src_bigrams).most_common(1)[0][1]

        tgt_bigrams = ngrams(tgt, self.ngram_size)
        tgt_max_bigram_count = Counter(tgt_bigrams).most_common(1)[0][1]

        if (
            tgt_max_bigram_count >= self.count_threshold
            and (tgt_max_bigram_count - src_max_bigram_count)
            > self.difference_threshold
        ):
            return True

        return False
