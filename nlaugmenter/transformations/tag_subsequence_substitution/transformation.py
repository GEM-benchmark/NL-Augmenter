import collections
import itertools
import os
import pickle
import random
from typing import List, Tuple

from nlaugmenter.interfaces.TaggingOperation import TaggingOperation
from nlaugmenter.tasks.TaskTypes import TaskType
from nlaugmenter.transformations.tag_subsequence_substitution.data import (
    example_dataset,
)

"""
A subsequence substitution--based augmentation system for tagging.
Augmentation process:
1. Draw a subsequence A from the input (tokens, tags) tuple.
2. Draw a subsequence B within the whole dataset, with the same tag subsequence.
3. Substitute A with B in the input example.

Example:
Input:
    tokens: ['EU', 'rejects', 'German', 'call', 'to', 'boycott', 'British', 'lamb', '.']
    (POS) tags: ['NNP', 'VBZ', 'JJ', 'NN', 'TO', 'VB', 'JJ', 'NN', '.']
Drawn subsequence from input:
    tokens: ['British', 'lamb']
    (POS) tags: ['JJ', 'NN']
Reference (randomly drawn from datset w.r.t. subsequence tags):
    tokens: ['Germany', 'imported', '47,600', 'sheep', 'from', 'Britain', 'last', 'year', ',',
             'nearly', 'half', 'of', 'total', 'imports', '.']
    (POS) tags: ['NNP', 'VBD', 'CD', 'NN', 'IN', 'NNP', 'JJ', 'NN', ',', 'RB', 'NN', 'IN', 'JJ', 'NNS', '.']
Substitution content:
    tokens: ['last', 'year']
    (POS) tags: ['JJ', 'NN']
Output:
    tokens: ['EU', 'rejects', 'German', 'call', 'to', 'boycott', 'last', 'year', '.']
    (POS) tags: ['NNP', 'VBZ', 'JJ', 'NN', 'TO', 'VB', 'JJ', 'NN', '.']
"""


class TagSubsequenceSubstitution(TaggingOperation):
    tasks = [TaskType.TEXT_TAGGING]
    languages = "All"
    keywords = ["lexical", "rule-based", "possible-meaning-alteration"]

    def __init__(
        self,
        seed=0,
        max_outputs=1,
        base_dataset=example_dataset,
        min_n_gram=1,
        max_n_gram=4,
    ):
        super().__init__(seed, max_outputs=max_outputs)
        assert (
            base_dataset is not None
        ), "base_dataset should be a list of (tokens, tags) tuples"
        self.base_stats = self.extract_stats(
            base_dataset, min_n_gram, max_n_gram
        )
        self.max_n_gram = max_n_gram
        self.min_n_gram = min_n_gram

    @staticmethod
    def extract_stats(dataset, min_n_gram, max_n_gram, stats_path=None):
        """Extract statistics from dataset, or load stats if specified."""
        if stats_path and os.path.exists(stats_path):
            stats = pickle.load(open(stats_path, "rb"))
        else:
            stats = collections.defaultdict(collections.Counter)
            for sentence, tags in dataset:
                assert len(sentence) == len(tags)
                length = len(sentence)
                for ss_l in range(
                    min_n_gram, max_n_gram + 1
                ):  # subsequence_length
                    for i in range(length - ss_l):
                        subsequence_sentence = tuple(
                            sentence[slice(i, i + ss_l)]
                        )
                        subsequence_tags = tuple(tags[slice(i, i + ss_l)])
                        stats[subsequence_tags][subsequence_sentence] += 1
            if stats_path:
                pickle.dump(stats, open(stats_path, "wb"))
        return stats

    def generate(
        self, token_sequence: List[str], tag_sequence: List[str]
    ) -> List[Tuple[List[str], List[str]]]:
        """Generate a list of (sentence, tags) as output based on input."""
        random.seed(self.seed)
        token_seq = token_sequence.copy()
        length_token_seq = len(token_seq)
        perturbed_sentences = list()
        for _ in itertools.repeat(None, self.max_outputs):
            if length_token_seq < self.min_n_gram:
                continue
            subseq_length = random.randint(
                self.min_n_gram, min(length_token_seq, self.max_n_gram)
            )
            start_position = random.randint(
                0, length_token_seq - subseq_length
            )
            subsequence = tuple(
                tag_sequence[
                    slice(start_position, start_position + subseq_length)
                ]
            )
            substitution_content = list(
                random.sample(
                    [
                        val
                        for val, cnt in self.base_stats[subsequence].items()
                        for _ in range(cnt)
                    ],
                    1,
                )[0]
            )
            token_seq = (
                token_seq[:start_position]
                + substitution_content
                + token_seq[
                    slice(start_position + subseq_length, None)
                ]  # noqa: E203
            )
            perturbed_sentences.append((token_seq, tag_sequence))
            token_seq = token_sequence.copy()
        return perturbed_sentences


# Sample code to demonstrate usage. Can also assist in adding test cases.

"""
if __name__ == '__main__':
    import json
    from TestRunner import convert_to_snake_case
    tf = TagSubsequenceSubstitution(max_outputs=3)
    test_cases = []
    src = [
        ['EU', 'rejects', 'German', 'call', 'to', 'boycott', 'British', 'lamb', '.'],
        ['Peter', 'Blackburn'],
        ['BRUSSELS', '1996-08-22'],
        ['The', 'European', 'Commission', 'said', 'on', 'Thursday', 'it', 'disagreed', 'with', 'German',
         'advice', 'to', 'consumers', 'to', 'shun', 'British', 'lamb', 'until', 'scientists', 'determine',
         'whether', 'mad', 'cow', 'disease', 'can', 'be', 'transmitted', 'to', 'sheep', '.'],
        ['Germany', "'s", 'representative', 'to', 'the', 'European', 'Union', "'s", 'veterinary', 'committee',
         'Werner', 'Zwingmann', 'said', 'on', 'Wednesday', 'consumers', 'should', 'buy', 'sheepmeat', 'from',
         'countries', 'other', 'than', 'Britain', 'until', 'the', 'scientific', 'advice', 'was', 'clearer', '.']
    ]
    tgt = [
        ['NNP', 'VBZ', 'JJ', 'NN', 'TO', 'VB', 'JJ', 'NN', '.'],
        ['NNP', 'NNP'],
        ['NNP', 'CD'],
        ['DT', 'NNP', 'NNP', 'VBD', 'IN', 'NNP', 'PRP', 'VBD', 'IN', 'JJ', 'NN', 'TO', 'NNS', 'TO', 'VB', 'JJ',
         'NN', 'IN', 'NNS', 'VBP', 'IN', 'JJ', 'NN', 'NN', 'MD', 'VB', 'VBN', 'TO', 'NN', '.'],
        ['NNP', 'POS', 'NN', 'TO', 'DT', 'NNP', 'NNP', 'POS', 'JJ', 'NN', 'NNP', 'NNP', 'VBD', 'IN', 'NNP', 'NNS',
         'MD', 'VB', 'NN', 'IN', 'NNS', 'JJ', 'IN', 'NNP', 'IN', 'DT', 'JJ', 'NN', 'VBD', 'JJR', '.']
    ]

    for idx, (token_sequence, tag_sequence) in enumerate(zip(src, tgt)):
        sentences = tf.generate(token_sequence, tag_sequence)
        test_cases.append({
            'class': tf.name(),
            'inputs': {'token_sequence': ' '.join(token_sequence), 'tag_sequence': ' '.join(tag_sequence)},
            'outputs': []}
        )
        for token_seq, tag_seq in sentences:
            test_cases[idx]['outputs'].append(
                {'token_sequence': ' '.join(token_seq), 'tag_sequence': ' '.join(tag_seq)}
            )
    json_file = {'type': convert_to_snake_case(tf.name()), 'test_cases': test_cases}
    print(json.dumps(json_file, indent=2))
"""
