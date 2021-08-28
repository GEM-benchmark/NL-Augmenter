# Copyright 2021 msg systems ag

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
from spacy.language import Language
from spacy.tokens import Doc, Token

from .data_model import FeatureTable, Mention
from .rules import RulesAnalyzer

ENSEMBLE_SIZE = 5


class TendenciesAnalyzer:
    def __init__(
        self,
        rules_analyzer: RulesAnalyzer,
        vectors_nlp: Language,
        feature_table: FeatureTable,
    ):
        self.rules_analyzer = rules_analyzer
        self.vectors_nlp = vectors_nlp
        if self.vectors_nlp.vocab[rules_analyzer.random_word].has_vector:
            self.vector_length = len(
                self.vectors_nlp.vocab[rules_analyzer.random_word].vector
            )
        else:
            self.vector_length = len(
                vectors_nlp(rules_analyzer.random_word)[0].vector
            )
        assert self.vector_length > 0
        self.feature_table = feature_table

    def get_feature_map(self, token_or_mention, doc: Doc) -> list:
        """Returns a binary list representing the features from *self.feature_table* that
        the token or any of the tokens within the mention has. The list is also
        added as *token._.coref_chains.temp_feature_map* or *mention.temp_feature_map*.
        """

        def convert_to_oneshot(reference_list, actual_list):
            """
            Returns a list of the same length as 'reference_list' where positions corresponding to
            entries in 'reference_list' that are also contained within 'actual_list' have the
            value '1' and other positions have the value '0'.
            """
            return [
                1 if reference in actual_list else 0
                for reference in reference_list
            ]

        def get_oneshot_for_token_and_siblings(prop, func):
            """Executes a logical AND between the values for the respective siblings."""
            oneshot = convert_to_oneshot(prop, func(token))
            for sibling in siblings:
                sibling_oneshot = convert_to_oneshot(prop, func(sibling))
                oneshot = [
                    1 if (entry == 1 or sibling_oneshot[index] == 1) else 0
                    for (index, entry) in enumerate(oneshot)
                ]
            return oneshot

        siblings = []
        if isinstance(token_or_mention, Token):
            if hasattr(token_or_mention._.coref_chains, "temp_feature_map"):
                return token_or_mention._.coref_chains.temp_feature_map
            token = token_or_mention
        else:
            if hasattr(token_or_mention, "temp_feature_map"):
                return token_or_mention.temp_feature_map
            token = doc[token_or_mention.root_index]
            if len(token_or_mention.token_indexes) > 1:
                siblings = [doc[i] for i in token_or_mention.token_indexes[1:]]

        feature_map = convert_to_oneshot(self.feature_table.tags, [token.tag_])

        feature_map.extend(
            get_oneshot_for_token_and_siblings(
                self.feature_table.morphs, lambda token: token.morph
            )
        )

        feature_map.extend(
            convert_to_oneshot(self.feature_table.ent_types, [token.ent_type_])
        )

        feature_map.extend(
            get_oneshot_for_token_and_siblings(
                self.feature_table.lefthand_deps_to_children,
                lambda token: [
                    child.dep_ for child in token.children if child.i < token.i
                ],
            )
        )

        feature_map.extend(
            get_oneshot_for_token_and_siblings(
                self.feature_table.righthand_deps_to_children,
                lambda token: [
                    child.dep_ for child in token.children if child.i > token.i
                ],
            )
        )

        if (
            token.dep_ != self.rules_analyzer.root_dep
            and token.i < token.head.i
        ):
            feature_map.extend(
                convert_to_oneshot(
                    self.feature_table.lefthand_deps_to_parents, [token.dep_]
                )
            )
        else:
            feature_map.extend(
                convert_to_oneshot(
                    self.feature_table.lefthand_deps_to_parents, []
                )
            )

        if (
            token.dep_ != self.rules_analyzer.root_dep
            and token.i > token.head.i
        ):
            feature_map.extend(
                convert_to_oneshot(
                    self.feature_table.righthand_deps_to_parents, [token.dep_]
                )
            )
        else:
            feature_map.extend(
                convert_to_oneshot(
                    self.feature_table.righthand_deps_to_parents, []
                )
            )

        if token.dep_ != self.rules_analyzer.root_dep:
            feature_map.extend(
                convert_to_oneshot(
                    self.feature_table.parent_tags, [token.head.tag_]
                )
            )
        else:
            feature_map.extend(
                convert_to_oneshot(self.feature_table.parent_tags, [])
            )

        if token.dep_ != self.rules_analyzer.root_dep:
            feature_map.extend(
                convert_to_oneshot(
                    self.feature_table.parent_morphs, token.head.morph
                )
            )
        else:
            feature_map.extend(
                convert_to_oneshot(self.feature_table.parent_morphs, [])
            )

        if token.dep_ != self.rules_analyzer.root_dep:
            feature_map.extend(
                convert_to_oneshot(
                    self.feature_table.parent_lefthand_deps_to_children,
                    [
                        child.dep_
                        for child in token.head.children
                        if child.i < token.head.i
                    ],
                )
            )
        else:
            feature_map.extend(
                convert_to_oneshot(
                    self.feature_table.parent_lefthand_deps_to_children, []
                )
            )

        if token.dep_ != self.rules_analyzer.root_dep:
            feature_map.extend(
                convert_to_oneshot(
                    self.feature_table.parent_righthand_deps_to_children,
                    [
                        child.dep_
                        for child in token.head.children
                        if child.i > token.head.i
                    ],
                )
            )
        else:
            feature_map.extend(
                convert_to_oneshot(
                    self.feature_table.parent_righthand_deps_to_children, []
                )
            )

        if isinstance(token_or_mention, Token):
            token_or_mention._.coref_chains.temp_feature_map = feature_map
        else:
            token_or_mention.temp_feature_map = feature_map
        return feature_map

    def get_position_map(self, token_or_mention, doc: Doc) -> list:
        """Returns a list of numbers representing the position, depth, etc. of the token or mention
        within its sentence. The list is also added as *token._.coref_chains.temp_position_map*
        or *mention.temp_position_map*.
        """

        if isinstance(token_or_mention, Token):
            if hasattr(token_or_mention._.coref_chains, "temp_position_map"):
                return token_or_mention._.coref_chains.temp_position_map
            token = token_or_mention
        else:
            if hasattr(token_or_mention, "temp_position_map"):
                return token_or_mention.temp_position_map
            token = doc[token_or_mention.root_index]

        # This token is the nth word within its sentence
        position_map = [
            token.i
            - token.doc._.coref_chains.temp_sent_starts[
                token._.coref_chains.temp_sent_index
            ]
        ]

        # This token is at depth n from the root
        position_map.append(len(list(token.ancestors)))

        # This token is n verbs from the root
        position_map.append(
            len(
                [
                    ancestor
                    for ancestor in token.ancestors
                    if ancestor.pos_ in self.rules_analyzer.verb_pos
                ]
            )
        )

        # This token is the nth token at its depth within its sentence
        position_map.append(
            len(
                [
                    1
                    for token_in_sentence in token.sent
                    if token_in_sentence.i < token.i
                    and len(list(token_in_sentence.ancestors))
                    == len(list(token.ancestors))
                ]
            )
        )

        # This token is the nth child of its parents
        if token.dep_ != self.rules_analyzer.root_dep:
            position_map.append(
                sorted([child.i for child in token.head.children]).index(
                    token.i
                )
            )
        else:
            position_map.append(-1)

        # Number of dependent siblings, or -1 if the method was passed a mention that is within
        # a coordination phrase but only covers one token within that phrase
        if token._.coref_chains.temp_governing_sibling is not None or (
            len(token._.coref_chains.temp_dependent_siblings) > 0
            and not (
                isinstance(token_or_mention, Mention)
                and len(token_or_mention.token_indexes) > 1
            )
        ):
            position_map.append(-1)
        else:
            position_map.append(
                len(token._.coref_chains.temp_dependent_siblings)
            )

        position_map.append(
            1 if token._.coref_chains.temp_governing_sibling is not None else 0
        )

        if isinstance(token_or_mention, Token):
            token_or_mention._.coref_chains.temp_position_map = position_map
        else:
            token_or_mention.temp_position_map = position_map
        return position_map

    def get_compatibility_map(
        self, referred: Mention, referring: Token
    ) -> list:
        """Returns a list of numbers representing the interaction between *referred* and
        *referring*. It will already have been established that coreference between the two is
        possible; the compatibility map assists the neural network in ascertaining how likely
        it is. The list is also added as *referred.temp_compatibility_map*.
        """
        doc = referring.doc
        referred_root = doc[referred.root_index]

        if hasattr(referred, "temp_compatibility_map"):
            return referred.temp_compatibility_map

        # Referential distance in words (may be negative in the case of cataphora)
        compatibility_map = [referring.i - referred_root.i]

        # Referential distance in sentences
        compatibility_map.append(
            referring._.coref_chains.temp_sent_index
            - referred_root._.coref_chains.temp_sent_index
        )

        # Whether the referred mention, its lefthand sibling or its head is among the ancestors
        # of the referring element
        compatibility_map.append(
            1
            if referred_root in referring.ancestors
            or (
                referred_root.dep_ != self.rules_analyzer.root_dep
                and referred_root.head in referring.ancestors
            )
            or referred_root._.coref_chains.temp_governing_sibling is not None
            and (
                referred_root._.coref_chains.temp_governing_sibling
                in referring.ancestors
                or (
                    referred_root._.coref_chains.temp_governing_sibling.dep_
                    != self.rules_analyzer.root_dep
                    and referred_root._.coref_chains.temp_governing_sibling.head
                    in referring.ancestors
                )
            )
            else 0
        )

        # The cosine similarity of the two objects' heads' vectors
        if (
            referred_root.dep_ != self.rules_analyzer.root_dep
            and referring.dep_ != self.rules_analyzer.root_dep
        ):
            referred_head_lexeme = self.vectors_nlp.vocab[
                referred_root.head.lemma_
            ]
            referring_head_lexeme = self.vectors_nlp.vocab[
                referring.head.lemma_
            ]
            if (
                referred_head_lexeme.has_vector
                and referring_head_lexeme.has_vector
            ):
                compatibility_map.append(
                    referred_head_lexeme.similarity(referring_head_lexeme)
                )
            elif (
                referred_root.has_vector and referring.has_vector
            ):  # _sm models
                compatibility_map.append(referred_root.similarity(referring))
            else:
                compatibility_map.append(-1)
        else:
            compatibility_map.append(-1)

        # The number of common true values in the feature maps of *referred.root* and *referring*.
        referred_feature_map = self.get_feature_map(referred, referring.doc)
        referring_feature_map = self.get_feature_map(
            Mention(referring, False), referring.doc
        )
        compatibility_map.append(
            [
                1 if (entry == 1 and referring_feature_map[index] == 1) else 0
                for (index, entry) in enumerate(referred_feature_map)
            ].count(1)
        )

        referred.temp_compatibility_map = compatibility_map
        return compatibility_map

    def get_vectors(self, token_or_mention, doc: Doc) -> list:
        """Returns vector representations for *token_or_mention* and its head. If there is no head,
        a zero vector is returned in place of the head vector. The vector representations are
        added as a tuple as *token._.coref_chains.temp_vectors* or *mention.temp_vectors*
        """
        if isinstance(token_or_mention, Token):
            if hasattr(token_or_mention._.coref_chains, "temp_vectors"):
                return token_or_mention._.coref_chains.temp_vectors
            tokens = [token_or_mention]
        else:
            if hasattr(token_or_mention, "temp_vectors"):
                return token_or_mention.temp_vectors
            tokens = [doc[i] for i in token_or_mention.token_indexes]
        if self.vectors_nlp.vocab[tokens[0].lemma_].has_vector:
            # The mean of the siblings seems likely to be more representative than the whole span
            this_object_vector = np.mean(
                np.array(
                    [self.vectors_nlp.vocab[t.lemma_].vector for t in tokens]
                ),
                axis=0,
            )
        else:
            this_object_vector = np.mean(
                np.array([t.vector for t in tokens]), axis=0
            )
        if len(this_object_vector) == 0:
            this_object_vector = np.zeros(self.vector_length)

        if tokens[0].dep_ != self.rules_analyzer.root_dep:
            head = tokens[0].head
            if self.vectors_nlp.vocab[head.lemma_].has_vector:
                head_vector = self.vectors_nlp.vocab[head.lemma_].vector
            else:
                head_vector = head.vector
            if len(head_vector) == 0:
                head_vector = np.zeros(self.vector_length)
        else:
            head_vector = np.zeros(self.vector_length)

        if isinstance(token_or_mention, Token):
            token_or_mention._.coref_chains.temp_vectors = (
                this_object_vector,
                head_vector,
            )
        else:
            token_or_mention.temp_vectors = (this_object_vector, head_vector)

        return this_object_vector, head_vector

    def prepare_keras_data(self, docs: list, *, return_outputs: bool = False):
        """Generates from a list of documents the inputs for a Keras model, a boolean value
        specfying whether scoring is necessary, and - when training only - the outputs
        for a Keras model.
        """
        referred_vector_inputs = []
        referred_head_vector_inputs = []
        referred_feature_map_inputs = []
        referred_position_map_inputs = []
        referring_vector_inputs = []
        referring_head_vector_inputs = []
        referring_feature_map_inputs = []
        referring_position_map_inputs = []
        compatibility_map_inputs = []
        if return_outputs:
            outputs = []

        keras_inputs = {}
        keras_outputs = {}

        # if there are no competing interpretations of anaphors in the document, there is nothing
        # to score
        scoring_necessary = False

        for doc in docs:
            for referring in (
                t
                for t in doc
                if hasattr(t._.coref_chains, "temp_potential_referreds")
            ):
                (
                    referring_vector_input,
                    referring_head_vector_input,
                ) = self.get_vectors(referring, doc)
                referring_feature_map_input = self.get_feature_map(
                    referring, doc
                )
                referring_position_map_input = self.get_position_map(
                    referring, doc
                )

                for index, potential_referred in enumerate(
                    p
                    for p in referring._.coref_chains.temp_potential_referreds
                    if not hasattr(p, "spanned_in_training")
                ):
                    # spanned in training - X->Y and Y->Z; we do want to present X->Z
                    # as neither correct nor incorrect and so remove it from the
                    # training data
                    if index > 0:
                        scoring_necessary = True
                    (
                        referred_vector_input,
                        referred_head_vector_input,
                    ) = self.get_vectors(potential_referred, doc)
                    referred_feature_map_input = self.get_feature_map(
                        potential_referred, doc
                    )
                    referred_position_map_input = self.get_position_map(
                        potential_referred, doc
                    )
                    compatibility_map_input = self.get_compatibility_map(
                        potential_referred, referring
                    )
                    referred_vector_inputs.append(referred_vector_input)
                    referred_head_vector_inputs.append(
                        referred_head_vector_input
                    )
                    referred_feature_map_inputs.append(
                        referred_feature_map_input
                    )
                    referred_position_map_inputs.append(
                        referred_position_map_input
                    )
                    referring_vector_inputs.append(referring_vector_input)
                    referring_head_vector_inputs.append(
                        referring_head_vector_input
                    )
                    referring_feature_map_inputs.append(
                        referring_feature_map_input
                    )
                    referring_position_map_inputs.append(
                        referring_position_map_input
                    )
                    compatibility_map_inputs.append(compatibility_map_input)
                    if return_outputs:
                        outputs.append(
                            [
                                1
                                if hasattr(
                                    potential_referred, "true_in_training"
                                )
                                else 0
                            ]
                        )

        np_referred_vector_inputs = np.array(referred_vector_inputs)
        np_referred_head_vector_inputs = np.array(referred_head_vector_inputs)
        np_referred_feature_map_inputs = np.array(referred_feature_map_inputs)
        np_referred_position_map_inputs = np.array(
            referred_position_map_inputs
        )
        np_referring_vector_inputs = np.array(referring_vector_inputs)
        np_referring_head_vector_inputs = np.array(
            referring_head_vector_inputs
        )
        np_referring_feature_map_inputs = np.array(
            referring_feature_map_inputs
        )
        np_referring_position_map_inputs = np.array(
            referring_position_map_inputs
        )
        np_compatibility_map_inputs = np.array(compatibility_map_inputs)

        for index in range(ENSEMBLE_SIZE):
            keras_inputs[
                "_".join(("referred_vector_input", str(index)))
            ] = np_referred_vector_inputs
            keras_inputs[
                "_".join(("referred_head_vector_input", str(index)))
            ] = np_referred_head_vector_inputs
            keras_inputs[
                "_".join(("referred_feature_map_input", str(index)))
            ] = np_referred_feature_map_inputs
            keras_inputs[
                "_".join(("referred_position_map_input", str(index)))
            ] = np_referred_position_map_inputs
            keras_inputs[
                "_".join(("referring_vector_input", str(index)))
            ] = np_referring_vector_inputs
            keras_inputs[
                "_".join(("referring_head_vector_input", str(index)))
            ] = np_referring_head_vector_inputs
            keras_inputs[
                "_".join(("referring_feature_map_input", str(index)))
            ] = np_referring_feature_map_inputs
            keras_inputs[
                "_".join(("referring_position_map_input", str(index)))
            ] = np_referring_position_map_inputs
            keras_inputs[
                "_".join(("compatibility_map_input", str(index)))
            ] = np_compatibility_map_inputs

        if return_outputs:
            np_outputs = np.array(outputs)
            for index in range(ENSEMBLE_SIZE):
                keras_outputs["_".join(("output", str(index)))] = np_outputs

        if return_outputs:
            return keras_inputs, scoring_necessary, keras_outputs
        return keras_inputs, scoring_necessary

    def score(self, doc: Doc, keras_ensemble) -> None:
        """Scores all possible anaphoric pairs in *doc*. The scores are never referenced
        outside this method because the possible pairs on each anaphor are sorted within
        this method with the more likely interpretations at the front of the list.
        """
        keras_inputs, scoring_necessary = self.prepare_keras_data([doc])
        if scoring_necessary:
            scores = np.mean(keras_ensemble.predict(keras_inputs), axis=0)
            score_iterator = iter(scores)
            for referring in (
                t
                for t in doc
                if hasattr(t._.coref_chains, "temp_potential_referreds")
            ):
                for potential_referred in (
                    p
                    for p in referring._.coref_chains.temp_potential_referreds
                ):
                    potential_referred.temp_score = next(score_iterator)[0]
            is_last = False
            try:
                next(score_iterator)
            except StopIteration:
                is_last = True
            assert (
                is_last
            ), "Mismatch between potential referreds and Keras output."
            for referring in (
                t
                for t in doc
                if hasattr(t._.coref_chains, "temp_potential_referreds")
            ):
                referring._.coref_chains.temp_potential_referreds.sort(
                    key=lambda potential_referred: (
                        potential_referred.temp_is_uncertain,
                        0 - potential_referred.temp_score,
                    )
                )
