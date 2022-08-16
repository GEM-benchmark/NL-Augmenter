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

import keras
from keras import layers
from spacy.language import Language

from ..data_model import FeatureTable, Mention
from ..rules import RulesAnalyzerFactory


class ModelGenerator:
    def __init__(self, model_label: str, nlp: Language, vectors_nlp: Language):
        self.nlp = nlp
        self.model_label = model_label
        self.rules_analyzer = RulesAnalyzerFactory().get_rules_analyzer(nlp)
        self.vectors_nlp = vectors_nlp

    def generate_feature_table(self, docs: list) -> FeatureTable:

        tags = set()
        morphs = set()
        ent_types = set()
        lefthand_deps_to_children = set()
        righthand_deps_to_children = set()
        lefthand_deps_to_parents = set()
        righthand_deps_to_parents = set()
        parent_tags = set()
        parent_morphs = set()
        parent_lefthand_deps_to_children = set()
        parent_righthand_deps_to_children = set()

        for doc in docs:
            for token in (
                token
                for token in doc
                if self.rules_analyzer.is_independent_noun(token)
                or self.rules_analyzer.is_potential_anaphor(token)
            ):
                tags.add(token.tag_)
                morphs.update(token.morph)
                ent_types.add(token.ent_type_)
                lefthand_deps_to_children.update(
                    (
                        child.dep_
                        for child in token.children
                        if child.i < token.i
                    )
                )
                righthand_deps_to_children.update(
                    (
                        child.dep_
                        for child in token.children
                        if child.i > token.i
                    )
                )
                if token.dep_ != self.rules_analyzer.root_dep:
                    if token.i < token.head.i:
                        lefthand_deps_to_parents.add(token.dep_)
                    else:
                        righthand_deps_to_parents.add(token.dep_)
                    parent_tags.add(token.head.tag_)
                    parent_morphs.update(token.head.morph)
                    parent_lefthand_deps_to_children.update(
                        (
                            child.dep_
                            for child in token.head.children
                            if child.i < token.head.i
                        )
                    )
                    parent_righthand_deps_to_children.update(
                        (
                            child.dep_
                            for child in token.head.children
                            if child.i > token.head.i
                        )
                    )

        return FeatureTable(
            tags=sorted(list(tags)),
            morphs=sorted(list(morphs)),
            ent_types=sorted(list(ent_types)),
            lefthand_deps_to_children=sorted(list(lefthand_deps_to_children)),
            righthand_deps_to_children=sorted(
                list(righthand_deps_to_children)
            ),
            lefthand_deps_to_parents=sorted(list(lefthand_deps_to_parents)),
            righthand_deps_to_parents=sorted(list(righthand_deps_to_parents)),
            parent_tags=sorted(list(parent_tags)),
            parent_morphs=sorted(list(parent_morphs)),
            parent_lefthand_deps_to_children=sorted(
                list(parent_lefthand_deps_to_children)
            ),
            parent_righthand_deps_to_children=sorted(
                list(parent_righthand_deps_to_children)
            ),
        )

    def generate_keras_model(
        self, docs: list, tendencies_analyzer, ensemble_size: int
    ):
        def create_vector_squeezer(name, ensemble_index):
            """Generates part of the network that accepts a full-width vector and squeezes
            it down to 3 neurons to feed into the rest of the network. This is intended
            to force the network to learn succinct, relevant information about the vectors
            and also to reduce the overall importance of the vectors compared to the other
            map inputs during training.
            """
            input_layer = keras.Input(
                shape=(vector_width,),
                name="_".join((name, "vector_input", str(ensemble_index))),
            )
            layer = layers.Dense(
                24,
                activation="relu",
                name="_".join((name, "vector_hidden_0_", str(ensemble_index))),
            )(input_layer)
            output_layer = layers.Dense(
                3,
                activation="relu",
                name="_".join((name, "vector_output", str(ensemble_index))),
            )(layer)
            return input_layer, output_layer

        # Look for a helpful document in the training corpus that has a token near the beginning
        # with a vector (should normally be the case for the majority of tokens in the majority
        # of documents)
        helpful_docs = [doc for doc in docs if len(doc) > 10]
        if len(helpful_docs) == 0:
            raise RuntimeError("No usable docs in training corpus.")
        vector_width = -1
        for token in helpful_docs[0][0:10]:
            if self.vectors_nlp.vocab[token.lemma_].has_vector:
                vector_width = len(self.vectors_nlp.vocab[token.lemma_].vector)
                break
        if vector_width == -1:  # _sm models
            for token in helpful_docs[0][0:10]:
                if token.has_vector:
                    vector_width = len(token.vector)
                    break
        if vector_width == -1:
            raise RuntimeError("Unable to determine vector width.")

        feature_map = tendencies_analyzer.get_feature_map(
            helpful_docs[0][0], helpful_docs[0]
        )

        feature_map_width = len(feature_map)
        position_map_width = len(
            tendencies_analyzer.get_position_map(
                helpful_docs[0][0], helpful_docs[0]
            )
        )
        compatibility_map_width = len(
            tendencies_analyzer.get_compatibility_map(
                Mention(helpful_docs[0][0], False), helpful_docs[0][1]
            )
        )
        overall_input_width = (
            (2 * feature_map_width)
            + (2 * position_map_width)
            + compatibility_map_width
            + 12
        )  # each vector is squeezed to 3 neurons

        keras_inputs = []
        keras_outputs = []
        for ensemble_index in range(ensemble_size):
            (
                referred_vector_input,
                referred_vector_output,
            ) = create_vector_squeezer("referred", ensemble_index)
            keras_inputs.append(referred_vector_input)
            (
                referred_head_vector_input,
                referred_head_vector_output,
            ) = create_vector_squeezer("referred_head", ensemble_index)
            keras_inputs.append(referred_head_vector_input)
            referred_feature_map_input = keras.Input(
                shape=(feature_map_width,),
                name="_".join(
                    ("referred_feature_map_input", str(ensemble_index))
                ),
            )
            keras_inputs.append(referred_feature_map_input)
            referred_position_map_input = keras.Input(
                shape=(position_map_width,),
                name="_".join(
                    ("referred_position_map_input", str(ensemble_index))
                ),
            )
            keras_inputs.append(referred_position_map_input)
            (
                referring_vector_input,
                referring_vector_output,
            ) = create_vector_squeezer("referring", ensemble_index)
            keras_inputs.append(referring_vector_input)
            (
                referring_head_vector_input,
                referring_head_vector_output,
            ) = create_vector_squeezer("referring_head", ensemble_index)
            keras_inputs.append(referring_head_vector_input)
            referring_feature_map_input = keras.Input(
                shape=(feature_map_width,),
                name="_".join(
                    ("referring_feature_map_input", str(ensemble_index))
                ),
            )
            keras_inputs.append(referring_feature_map_input)
            referring_position_map_input = keras.Input(
                shape=(position_map_width,),
                name="_".join(
                    ("referring_position_map_input", str(ensemble_index))
                ),
            )
            keras_inputs.append(referring_position_map_input)
            compatibility_map_input = keras.Input(
                shape=(compatibility_map_width,),
                name="_".join(
                    ("compatibility_map_input", str(ensemble_index))
                ),
            )
            keras_inputs.append(compatibility_map_input)
            layer = layers.Concatenate(
                axis=1, name="_".join(("combined_input", str(ensemble_index)))
            )(
                [
                    referred_vector_output,
                    referred_head_vector_output,
                    referred_feature_map_input,
                    referred_position_map_input,
                    referring_vector_output,
                    referring_head_vector_output,
                    referring_feature_map_input,
                    referring_position_map_input,
                    compatibility_map_input,
                ]
            )
            layer = layers.Dense(
                overall_input_width,
                activation="relu",
                name="_".join(("combined_hidden_0", str(ensemble_index))),
            )(layer)
            layer = layers.Dense(
                20,
                activation="relu",
                name="_".join(("combined_hidden_1", str(ensemble_index))),
            )(layer)
            output = layers.Dense(
                1,
                activation="sigmoid",
                name="_".join(("output", str(ensemble_index))),
            )(layer)
            keras_outputs.append(output)
        keras_model = keras.Model(
            inputs=keras_inputs,
            outputs=keras_outputs,
            name="_".join(("model", self.model_label)),
        )
        keras_model.compile(
            loss="binary_crossentropy",
            optimizer="adam",
            metrics=["binary_accuracy"],
        )
        return keras_model

    def train_keras_model(self, docs: list, tendencies_analyzer, keras_model):

        # First we go through the document marking any potential referreds that are in the
        # same chain but not next to one another; these are then excluded from training
        # (neither True nor False)
        for doc in docs:
            for token in (
                t
                for t in doc
                if hasattr(t._.coref_chains, "temp_potential_referreds")
            ):
                for index, referred in enumerate(
                    r
                    for r in token._.coref_chains.temp_potential_referreds
                    if hasattr(r, "true_in_training")
                ):
                    while True:
                        working_referring = doc[referred.root_index]
                        if not hasattr(
                            working_referring._.coref_chains,
                            "temp_potential_referreds",
                        ):
                            break
                        for index, working_referred in enumerate(
                            r
                            for r in working_referring._.coref_chains.temp_potential_referreds
                            if hasattr(r, "true_in_training")
                        ):
                            assert index == 0  # should only be one
                            for index, spanning_referred in enumerate(
                                r
                                for r in token._.coref_chains.temp_potential_referreds
                                if r == working_referred
                            ):
                                assert index == 0  # should only be one
                                spanning_referred.spanned_in_training = True
                            referred = working_referred
                            break
                        else:
                            break
        (
            keras_inputs,
            _,
            keras_outputs,
        ) = tendencies_analyzer.prepare_keras_data(docs, return_outputs=True)
        return keras_model.fit(
            x=keras_inputs,
            y=keras_outputs,
            epochs=self.rules_analyzer.training_epochs,
        )
