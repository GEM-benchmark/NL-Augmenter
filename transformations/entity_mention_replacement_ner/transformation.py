from typing import List

import numpy as np

from interfaces.TaggingOperation import TaggingOperation
from tasks.TaskTypes import TaskType


class EntityMentionReplacementNER(TaggingOperation):
    tasks = [TaskType.TEXT_TAGGING]

    def __init__(
        self, token_sequences, tag_sequences, p=0.7, seed=0, max_outputs=1
    ):
        super().__init__(seed, max_outputs=max_outputs)
        self.entity_mentions_by_type = (
            EntityMentionReplacementNER.extract_entity_mentions_by_type(
                token_sequences, tag_sequences
            )
        )
        self.max_outputs = max_outputs
        self.p = p

    def generate(self, token_sequence: List[str], tag_sequence: List[str]):
        assert len(token_sequence) == len(
            tag_sequence
        ), f"token_sequence and tag_sequence should have same length! {len(token_sequence)}!={len(tag_sequence)}"
        augmentations = []
        entities = EntityMentionReplacementNER.extract_entities(
            token_sequence, tag_sequence
        )
        if len(entities) == 0:
            augmentations.append(([token_sequence, tag_sequence]))
        else:
            for _ in range(self.max_outputs):
                augmented_entities = []
                for entity in entities:
                    assert (
                        entity["type"] in self.entity_mentions_by_type
                    ), f"invalid entity type {entity['type']} in tag_sequence"
                    if EntityMentionReplacementNER.flip_coin(self.p):
                        aug_entity = {
                            "text": np.random.choice(
                                self.entity_mentions_by_type[entity["type"]]
                            ),
                            "start": entity["start"],
                            "end": entity["end"],
                            "type": entity["type"],
                        }
                        augmented_entities.append(aug_entity)

                tokens, tags = [], []
                ptr = 0
                for aug_entity in augmented_entities:
                    (
                        ent_tokens,
                        ent_tags,
                    ) = EntityMentionReplacementNER.format_entity(
                        aug_entity["text"], aug_entity["type"]
                    )
                    if ptr < aug_entity["start"]:
                        tokens += [
                            token_sequence[t]
                            for t in range(ptr, aug_entity["start"])
                        ]
                        tags += [
                            tag_sequence[t]
                            for t in range(ptr, aug_entity["start"])
                        ]
                    tokens += ent_tokens
                    tags += ent_tags
                    ptr = aug_entity["end"]
                if ptr != len(token_sequence):
                    tokens += token_sequence[ptr:]
                    tags += tag_sequence[ptr:]

                augmentations.append(([tokens, tags]))

        return augmentations

    @staticmethod
    def format_entity(entity_text, entity_type):
        """
        Format the entity type tags in the correct BIO format.
        """
        entity_tokens = entity_text.split()
        entity_tags = [f"I-{entity_type}"] * len(entity_tokens)
        entity_tags[0] = f"B-{entity_type}"

        return entity_tokens, entity_tags

    @staticmethod
    def flip_coin(p):
        """
        Perform a binomial experiment.
        """
        return np.random.binomial(1, p=p)

    @staticmethod
    def extract_entity_mentions_by_type(token_sequences, tag_sequences):
        """
        Extract entity mentions categorized by entity type from a list of token_sequences and tags tag_sequences.
        """
        entity_mention_by_type = {}
        for sent_tokens, sent_tags in zip(token_sequences, tag_sequences):
            sent_entities = EntityMentionReplacementNER.extract_entities(
                sent_tokens, sent_tags
            )
            for entity in sent_entities:
                if entity["type"] not in entity_mention_by_type:
                    entity_mention_by_type[entity["type"]] = set()
                entity_mention_by_type[entity["type"]].add(entity["text"])
        for entity_type in entity_mention_by_type:
            entity_mention_by_type[entity_type] = list(
                entity_mention_by_type[entity_type]
            )
        return entity_mention_by_type

    @staticmethod
    def extract_entities(tokens, tags):
        """
        Extract entities from a list of tokens and tags sequence.
        """
        entities = []
        last_tag = "O"
        phrase_tokens = []
        start_idx, end_idx = -1, -1
        for idx in range(len(tokens)):
            token, tag = tokens[idx], tags[idx]
            start_chunk, end_chunk = False, False
            appended = False
            end_token = idx == len(tags) - 1
            if (last_tag == "O" and tag.startswith("B")) or (
                last_tag == "O" and tag.startswith("I")
            ):
                start_chunk = True
                end_chunk = False
                start_idx = idx
            if (last_tag.startswith("B") and tag == "O") or (
                last_tag.startswith("I") and tag == "O"
            ):
                start_chunk = False
                end_chunk = True
                end_idx = idx
            if (
                (last_tag.startswith("B") and tag.startswith("I"))
                or (last_tag.startswith("I") and tag.startswith("I"))
                or (last_tag == "O" and tag == "O")
            ):
                start_chunk = False
                end_chunk = False
            if (last_tag.startswith("I") and tag.startswith("B")) or (
                last_tag.startswith("B") and tag.startswith("B")
            ):
                start_chunk = True
                end_chunk = True
                end_idx = idx

            if start_chunk and end_chunk:
                phrase_str = " ".join(phrase_tokens)
                entity = {
                    "text": phrase_str,
                    "type": last_tag.split("-")[-1],
                    "start": start_idx,
                    "end": end_idx,
                }
                entities.append(entity)
                phrase_tokens = []
                start_chunk = False
                end_chunk = False
                start_idx = idx

            if start_chunk:
                phrase_tokens.append(token)
                start_chunk = False
                appended = True

            if end_token and tag != "O":
                if not appended:
                    phrase_tokens.append(token)
                    appended = True
                if not end_chunk:
                    last_tag = tag
                    end_chunk = True
                    end_idx = idx

            if end_chunk:
                phrase_str = " ".join(phrase_tokens)
                entity = {
                    "text": phrase_str,
                    "type": last_tag.split("-")[-1],
                    "start": start_idx,
                    "end": end_idx,
                }
                entities.append(entity)
                phrase_tokens = []
                end_chunk = False

            # middle of the entity mention
            if last_tag != "O" and tag != "O":
                if not appended:
                    phrase_tokens.append(token)
            last_tag = tag

        return entities


"""
# Sample code to demonstrate usage.

if __name__ == "__main__":

    token_sequences = [
        [
            "Judea",
            "Pearl",
            "was",
            "born",
            "in",
            "Tel",
            "Aviv",
            ",",
            "in",
            "1936",
            "to",
            "Polish",
            "Jewish",
            "immigrant",
            "parents",
            ".",
        ],
        ["Berlin", "is", "nine", "times", "bigger", "than", "Paris", "."],
        [
            "Vladimir",
            "Vladimirovich",
            "Putin",
            "was",
            "born",
            "in",
            "Leningrad",
            ".",
        ],
        [
            "Michael",
            "Irwin",
            "Jordan",
            "is",
            "an",
            "American",
            "scientist",
            ",",
            "professor",
            "at",
            "the",
            "University",
            "of",
            "California",
            ",",
            "Berkeley",
            ".",
        ],
        [
            "Bayerische",
            "Motoren",
            "Werke",
            "AG",
            ",",
            "commonly",
            "referred",
            "to",
            "as",
            "BMW",
            "is",
            "headquartered",
            "in",
            "Munich",
            ".",
        ],
        [
            "Boeing",
            "was",
            "founded",
            "by",
            "William",
            "Boeing",
            "in",
            "Seattle",
            ",",
            "Washington",
            ",",
            "on",
            "July",
            "15",
            ",",
            "1916",
            ".",
        ],
        [
            "SpaceX",
            "was",
            "founded",
            "in",
            "2002",
            "by",
            "Elon",
            "Musk",
            "with",
            "the",
            "goal",
            "of",
            "reducing",
            "space",
            "transportation",
            "costs",
            ".",
        ],
    ]
    tag_sequences = [
        [
            "B-PER",
            "I-PER",
            "O",
            "O",
            "O",
            "B-LOC",
            "I-LOC",
            "O",
            "O",
            "O",
            "O",
            "O",
            "O",
            "O",
            "O",
            "O",
        ],
        ["B-LOC", "O", "O", "O", "O", "O", "B-LOC", "O"],
        ["B-PER", "I-PER", "I-PER", "O", "O", "O", "B-LOC", "O"],
        [
            "B-PER",
            "I-PER",
            "I-PER",
            "O",
            "O",
            "O",
            "O",
            "O",
            "O",
            "O",
            "O",
            "B-ORG",
            "I-ORG",
            "I-ORG",
            "O",
            "B-LOC",
            "O",
        ],
        [
            "B-ORG",
            "I-ORG",
            "I-ORG",
            "I-ORG",
            "O",
            "O",
            "O",
            "O",
            "O",
            "B-ORG",
            "O",
            "O",
            "O",
            "B-LOC",
            "O",
        ],
        [
            "B-ORG",
            "O",
            "O",
            "O",
            "B-PER",
            "I-PER",
            "O",
            "B-LOC",
            "O",
            "B-LOC",
            "O",
            "O",
            "O",
            "O",
            "O",
            "O",
            "O",
        ],
        [
            "B-ORG",
            "O",
            "O",
            "O",
            "O",
            "O",
            "B-PER",
            "I-PER",
            "O",
            "O",
            "O",
            "O",
            "O",
            "O",
            "O",
            "O",
            "O",
        ],
    ]

    tf = EntityMentionReplacementNER(token_sequences, tag_sequences, p=1.0)
    augmentations = []
    for token_sequence, tag_sequence in zip(token_sequences, tag_sequences):
        augmentations.append(tf.generate(token_sequence, tag_sequence))
"""
