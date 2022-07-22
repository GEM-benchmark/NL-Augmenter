import itertools
from typing import List

import numpy as np
from transformers import FSMTForConditionalGeneration, FSMTTokenizer

from nlaugmenter.interfaces.TaggingOperation import TaggingOperation
from nlaugmenter.tasks.TaskTypes import TaskType


class BackTranslationNER(TaggingOperation):
    tasks = [TaskType.TEXT_TAGGING]
    heavy = True
    keywords = [
        "lexical",
        "model-based",
        "transformer-based",
        "possible-meaning-alteration",
        "high-generations",
        "world-knowledge",
    ]

    def __init__(self, segment_length=3, p=1.0, seed=0, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)
        np.random.seed(seed)
        self.segment_length = segment_length
        self.p = p
        self.max_outputs = max_outputs
        mname_en2de = "facebook/wmt19-en-de"
        mname_de2en = "facebook/wmt19-de-en"
        self.tokenizer_en2de = FSMTTokenizer.from_pretrained(mname_en2de)
        self.tokenizer_de2en = FSMTTokenizer.from_pretrained(mname_de2en)
        self.model_en2de = FSMTForConditionalGeneration.from_pretrained(
            mname_en2de
        )
        self.model_de2en = FSMTForConditionalGeneration.from_pretrained(
            mname_de2en
        )

    def generate(self, token_sequence: List[str], tag_sequence: List[str]):
        assert len(token_sequence) == len(
            tag_sequence
        ), f"token_sequence and tag_sequence should have same length! {len(token_sequence)}!={len(tag_sequence)}"
        augmentations = []
        segment_tokens, segment_tags = BackTranslationNER.create_segments(
            token_sequence, tag_sequence
        )
        for _ in range(self.max_outputs):
            tokens, tags = [], []
            for s_token, s_tag in zip(segment_tokens, segment_tags):
                translate_segment = np.random.binomial(1, p=self.p)
                if (
                    s_tag[0] != "O"
                    or len(s_token) < self.segment_length
                    or not translate_segment
                ):
                    tokens.extend(s_token)
                    tags.extend(s_tag)
                    continue
                segment_text = " ".join(s_token)
                segment_translation = self.translation_pipeline(segment_text)
                translated_tokens = segment_translation.split()
                translated_tags = ["O"] * len(translated_tokens)
                tokens.extend(translated_tokens)
                tags.extend(translated_tags)

            augmentations.append(([tokens, tags]))

        return augmentations

    def translation_pipeline(self, text):
        """
        Pass the text in source languages through the intermediate
        translations.
        :param text: the text to translate
        :return text_trans: backtranslated text
        """
        en2de_inputids = self.tokenizer_en2de.encode(text, return_tensors="pt")
        outputs_en2de = self.model_en2de.generate(en2de_inputids)
        text_trans = self.tokenizer_en2de.decode(
            outputs_en2de[0], skip_special_tokens=True
        )
        de2en_inputids = self.tokenizer_de2en.encode(
            text_trans, return_tensors="pt"
        )
        outputs_de2en = self.model_de2en.generate(de2en_inputids)
        text_trans = self.tokenizer_en2de.decode(
            outputs_de2en[0], skip_special_tokens=True
        )
        return text_trans

    @staticmethod
    def create_segments(tokens, tags):
        """
        A segment is defined as a consecutive sequence of same tag/label.
        """
        segment_tokens, segment_tags = [], []
        tags_idxs = [(i, t) for i, t in enumerate(tags)]
        groups = [
            list(g)
            for _, g in itertools.groupby(
                tags_idxs, lambda s: s[1].split("-")[-1]
            )
        ]
        for group in groups:
            idxs = [i[0] for i in group]
            segment_tokens.append([tokens[idx] for idx in idxs])
            segment_tags.append([tags[idx] for idx in idxs])

        return segment_tokens, segment_tags


"""
# Sample code to demonstrate usage.

if __name__ == "__main__":

    token_sequences = [
        ["Musk", "has", "been", "the", "subject", "of", "criticism", "due", "to", "unorthodox", "or", "unscientific", "stances", "and", "highly", "publicized", "controversies", "."],
        ["Shannon", "received", "his", "PhD", "from", "MIT", "in", "1940", "."]
    ]
    tag_sequences = [
        ["B-PER", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O"],
        ["B-PER", "O", "O", "O", "O", "B-ORG", "O", "O", "O"]
    ]

    tf = BackTranslationNER()
    augmentations = []
    for token_sequence, tag_sequence in zip(token_sequences, tag_sequences):
        augmentations.append(tf.generate(token_sequence, tag_sequence))
"""
