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

from collections import deque

from spacy.language import Language
from spacy.tokens import Doc, Token

from .data_model import Chain, FeatureTable, Mention
from .rules import RulesAnalyzerFactory
from .tendencies import TendenciesAnalyzer


class Annotator:

    RETRY_DEPTH = 5

    def __init__(
        self,
        nlp: Language,
        vectors_nlp: Language,
        feature_table: FeatureTable,
        keras_ensemble,
    ):
        self.keras_ensemble = keras_ensemble
        self.rules_analyzer = RulesAnalyzerFactory().get_rules_analyzer(nlp)
        self.tendencies_analyzer = TendenciesAnalyzer(
            self.rules_analyzer, vectors_nlp, feature_table
        )

    @staticmethod
    def record_mention(
        preceding_mention: Mention,
        token: Token,
        token_indexes_without_coordination_to_mention_sets: dict,
        token_indexes_with_coordination_to_mention_sets: dict,
    ) -> None:
        """*token_indexes_without_coordination_to_mention_sets* is the main means of
        generating and tracking chains.

        *token_indexes_with_coordination_to_mention_sets* tracks the ends of chains that
        end in a mention with coordination. It is necessary for the case where two anaphors
        both refer to a mention with coordination. It has to be kept separate from the main
        dictionary to cover the case where a mention with coordination itself contains an
        anaphor that belongs to a separate chain.
        """
        if len(preceding_mention.token_indexes) > 1:
            if (
                preceding_mention.root_index
                in token_indexes_with_coordination_to_mention_sets
            ):
                mention_set = token_indexes_with_coordination_to_mention_sets[
                    preceding_mention.root_index
                ]
            else:
                mention_set = {preceding_mention}
                for token_index in preceding_mention.token_indexes:
                    token_indexes_with_coordination_to_mention_sets[
                        token_index
                    ] = mention_set
        else:
            preceding_token = token.doc[preceding_mention.root_index]
            if (
                preceding_token.i
                in token_indexes_without_coordination_to_mention_sets
            ):
                mention_set = (
                    token_indexes_without_coordination_to_mention_sets[
                        preceding_token.i
                    ]
                )
            else:
                mention_set = {preceding_mention}
                token_indexes_without_coordination_to_mention_sets[
                    preceding_token.i
                ] = mention_set
        mention_set.add(Mention(token, False))
        if token.i in token_indexes_without_coordination_to_mention_sets:
            mention_set.update(
                token_indexes_without_coordination_to_mention_sets[token.i]
            )
            for mention in token_indexes_without_coordination_to_mention_sets[
                token.i
            ]:
                token_indexes_without_coordination_to_mention_sets[
                    mention.root_index
                ] = mention_set
        else:
            token_indexes_without_coordination_to_mention_sets[
                token.i
            ] = mention_set

    def get_compatibility(self, token: Token, mention_set: list) -> int:
        """Checks the compatibility of *token* with the possible chain represented by *mention_set*
        and expresses it with the semantics of *RuleAnalyzer.is_potential_anaphoric_pair()*.
        """

        result = 2
        mention_set_contains_referring_mention = False
        for mention in mention_set:
            if self.rules_analyzer.is_independent_noun(
                token.doc[mention.root_index]
            ):
                mention_set_contains_referring_mention = True
            working_result = self.rules_analyzer.is_potential_anaphoric_pair(
                mention, token, False
            )
            if working_result < result:
                result = working_result
            if result == 0:
                break
        if result == 2 and not mention_set_contains_referring_mention:
            result = 1
        return result

    def temp_annotate_any_coreferring_noun_link(
        self,
        token: Token,
        sentence_deque: deque,
        token_indexes_without_coordination_to_mention_sets: dict,
        token_indexes_with_coordination_to_mention_sets: dict,
    ) -> None:
        doc = token.doc
        if not token._.coref_chains.temp_potentially_referring:
            return
        for sent in sentence_deque:
            for preceding_token in (
                doc[index]
                for index in range(sent.end, sent.start - 1, -1)
                if index < token.i
            ):
                if (
                    preceding_token._.coref_chains.temp_potentially_referring
                    and self.rules_analyzer.is_potential_coreferring_noun_pair(
                        preceding_token, token
                    )
                ):
                    self.record_mention(
                        Mention(preceding_token, False),
                        token,
                        token_indexes_without_coordination_to_mention_sets,
                        token_indexes_with_coordination_to_mention_sets,
                    )
                    return
                if (
                    preceding_token.i
                    in token_indexes_without_coordination_to_mention_sets
                ):
                    # existing chain; *preceding_token* may be an anaphor linked to a noun
                    # that can form a noun pair with *token*
                    mention_set = (
                        token_indexes_without_coordination_to_mention_sets[
                            preceding_token.i
                        ]
                    )
                    for mention in (
                        mention
                        for mention in mention_set
                        if len(mention.token_indexes) == 1
                    ):
                        if self.rules_analyzer.is_potential_coreferring_noun_pair(
                            token.doc[mention.root_index], token
                        ):
                            self.record_mention(
                                Mention(preceding_token, False),
                                token,
                                token_indexes_without_coordination_to_mention_sets,
                                token_indexes_with_coordination_to_mention_sets,
                            )
                            return

    def temp_annotate_any_anaphoric_link(
        self,
        token: Token,
        token_indexes_without_coordination_to_mention_sets: dict,
        token_indexes_with_coordination_to_mention_sets: dict,
        permitted_start_index: int = 0,
    ) -> bool:
        """Returns *True* if an annotation occurred."""

        def check_mention_sets_for_reflexive_relationships(
            mention: Mention, index_to_mention_set_dict: dict
        ) -> bool:
            for token_index in mention.token_indexes:
                if token_index in index_to_mention_set_dict:
                    for working_mention in index_to_mention_set_dict[
                        token_index
                    ]:
                        if self.rules_analyzer.is_potential_reflexive_pair(
                            working_mention, token
                        ):
                            return True
            return False

        def intern_temp_annotate_any_anaphoric_link(
            allow_uncertainty: bool,
        ) -> bool:
            for index, potential_referred in enumerate(
                token._.coref_chains.temp_potential_referreds
            ):
                if index < permitted_start_index or index >= self.RETRY_DEPTH:
                    continue
                if len(potential_referred.token_indexes) == 1:
                    if (
                        potential_referred.root_index
                        in token_indexes_without_coordination_to_mention_sets
                    ):
                        mention_set = (
                            token_indexes_without_coordination_to_mention_sets[
                                potential_referred.root_index
                            ]
                        )
                        compatibility = self.get_compatibility(
                            token, mention_set
                        )
                        if compatibility == 0 or (
                            compatibility == 1 and not allow_uncertainty
                        ):
                            continue
                if self.rules_analyzer.is_reflexive_anaphor(token) == 0 and (
                    check_mention_sets_for_reflexive_relationships(
                        potential_referred,
                        token_indexes_without_coordination_to_mention_sets,
                    )
                    or check_mention_sets_for_reflexive_relationships(
                        potential_referred,
                        token_indexes_with_coordination_to_mention_sets,
                    )
                ):
                    continue
                self.record_mention(
                    potential_referred,
                    token,
                    token_indexes_without_coordination_to_mention_sets,
                    token_indexes_with_coordination_to_mention_sets,
                )
                return True
            return False

        if intern_temp_annotate_any_anaphoric_link(False):
            return True
        return intern_temp_annotate_any_anaphoric_link(True)

    def delete_from_collections_for_rewind(
        self,
        previous_token: Token,
        token: Token,
        token_indexes_without_coordination_to_mention_sets: dict,
        token_indexes_with_coordination_to_mention_sets: dict,
    ) -> None:
        def intern_delete_from_collections_for_rewind(
            dictionary: dict, working_token: Token
        ):
            if working_token.i in dictionary:
                mention_set = dictionary[working_token.i]
                working_mention = Mention(working_token, False)
                if working_mention in mention_set:
                    mention_set.remove(working_mention)
                del dictionary[working_token.i]
                if len(mention_set) == 1:
                    remaining_mention = list(mention_set)[0]
                    if remaining_mention.root_index in dictionary:
                        # is not the case where *remaining_mention* involves coordination
                        del dictionary[remaining_mention.root_index]

        doc = token.doc
        for working_token in doc[previous_token.i : token.i + 1]:
            intern_delete_from_collections_for_rewind(
                token_indexes_without_coordination_to_mention_sets,
                working_token,
            )
            intern_delete_from_collections_for_rewind(
                token_indexes_with_coordination_to_mention_sets, working_token
            )

    def attempt_rewind_with_previous_token_and_retry_index(
        self,
        retry_index: int,
        previous_token: Token,
        token: Token,
        sentence_deque: deque,
        token_indexes_without_coordination_to_mention_sets: list,
        token_indexes_with_coordination_to_mention_sets: list,
    ) -> bool:
        """Returns *True* if the rewind attempt succeeded."""
        doc = token.doc
        if self.temp_annotate_any_anaphoric_link(
            previous_token,
            token_indexes_without_coordination_to_mention_sets,
            token_indexes_with_coordination_to_mention_sets,
            retry_index,
        ):
            for working_token in doc[previous_token.i + 1 : token.i + 1]:
                self.temp_annotate_any_coreferring_noun_link(
                    working_token,
                    sentence_deque,
                    token_indexes_without_coordination_to_mention_sets,
                    token_indexes_with_coordination_to_mention_sets,
                )
                if hasattr(
                    working_token._.coref_chains, "temp_potential_referreds"
                ):
                    if not self.temp_annotate_any_anaphoric_link(
                        working_token,
                        token_indexes_without_coordination_to_mention_sets,
                        token_indexes_with_coordination_to_mention_sets,
                    ):
                        return False
            return True
        return False

    def attempt_retry(
        self,
        token: Token,
        coreferring_deque: deque,
        sentence_deque: deque,
        token_indexes_without_coordination_to_mention_sets: list,
        token_indexes_with_coordination_to_mention_sets: list,
    ):
        """Called when an anaphor could not be assigned to a chain; attempts alternative
        interpretations of the preceding anaphors to see whether any allow all anaphors to be
        assigned. Returns *True* if the rewind attempt succeeded."""
        previous_token = None
        for retry_index in range(
            1,
            min(
                self.RETRY_DEPTH,
                len(token._.coref_chains.temp_potential_referreds) + 1,
            ),
        ):
            # we only need start with *previous_token* because any different interpretations of
            # *token* have already been tried out unsuccessfully
            for previous_token in (
                t
                for t in coreferring_deque
                if token._.coref_chains.temp_sent_index
                - t._.coref_chains.temp_sent_index
                <= self.rules_analyzer.maximum_anaphora_sentence_referential_distance
            ):
                self.delete_from_collections_for_rewind(
                    previous_token,
                    token,
                    token_indexes_without_coordination_to_mention_sets,
                    token_indexes_with_coordination_to_mention_sets,
                )
                if self.attempt_rewind_with_previous_token_and_retry_index(
                    retry_index,
                    previous_token,
                    token,
                    sentence_deque,
                    token_indexes_without_coordination_to_mention_sets,
                    token_indexes_with_coordination_to_mention_sets,
                ):
                    return True
        if previous_token is not None:
            # All attempts have failed, so return to the original interpretation
            self.delete_from_collections_for_rewind(
                previous_token,
                token,
                token_indexes_without_coordination_to_mention_sets,
                token_indexes_with_coordination_to_mention_sets,
            )
            self.attempt_rewind_with_previous_token_and_retry_index(
                0,
                previous_token,
                token,
                sentence_deque,
                token_indexes_without_coordination_to_mention_sets,
                token_indexes_with_coordination_to_mention_sets,
            )
        return False

    def get_most_specific_mention(self, mention_set: set, doc: Doc):
        """Returns the most specific mention in the chain, where names > nouns > pronouns."""
        stored_mention = None
        for mention in mention_set:
            if len(mention.token_indexes) > 1:
                return mention
            if stored_mention is None:
                stored_mention = mention
                continue
            stored_mention_root_token = doc[stored_mention.root_index]
            this_mention_root_token = doc[mention.root_index]
            if self.rules_analyzer.is_independent_noun(
                this_mention_root_token
            ) and not self.rules_analyzer.is_independent_noun(
                stored_mention_root_token
            ):
                stored_mention = mention
            if (
                this_mention_root_token.pos_ in self.rules_analyzer.propn_pos
                and this_mention_root_token.ent_type_ != ""
                and (
                    stored_mention_root_token.pos_
                    not in self.rules_analyzer.propn_pos
                    or this_mention_root_token.ent_type_ == ""
                )
            ):
                stored_mention = mention
        return stored_mention

    def annotate(self, doc: Doc, used_in_training=False):
        if not used_in_training:
            self.rules_analyzer.initialize(doc)
        self.tendencies_analyzer.score(doc, self.keras_ensemble)
        token_indexes_without_coordination_to_mention_sets = {}
        token_indexes_with_coordination_to_mention_sets = {}
        sentence_deque = deque(
            maxlen=self.rules_analyzer.maximum_coreferring_nouns_sentence_referential_distance
            + 1
        )
        coreferring_deque = deque(maxlen=self.RETRY_DEPTH)
        for sent in doc.sents:
            sentence_deque.appendleft(sent)
            for token in sent:
                self.temp_annotate_any_coreferring_noun_link(
                    token,
                    sentence_deque,
                    token_indexes_without_coordination_to_mention_sets,
                    token_indexes_with_coordination_to_mention_sets,
                )
                if hasattr(token._.coref_chains, "temp_potential_referreds"):
                    if self.temp_annotate_any_anaphoric_link(
                        token,
                        token_indexes_without_coordination_to_mention_sets,
                        token_indexes_with_coordination_to_mention_sets,
                    ) or self.attempt_retry(
                        token,
                        coreferring_deque,
                        sentence_deque,
                        token_indexes_without_coordination_to_mention_sets,
                        token_indexes_with_coordination_to_mention_sets,
                    ):
                        coreferring_deque.appendleft(token)

        visited_token_indexes = set()
        chains = []
        for (
            token_index,
            mention_set,
        ) in token_indexes_without_coordination_to_mention_sets.items():
            if token_index in visited_token_indexes:
                continue
            mention_list = sorted(
                list(mention_set), key=lambda mention: mention.root_index
            )
            most_specific_mention = self.get_most_specific_mention(
                mention_list, doc
            )
            chain = Chain(
                mention_list, mention_list.index(most_specific_mention)
            )
            chains.append(chain)
            for mention in chain.mentions:
                if len(mention.token_indexes) == 1:
                    visited_token_indexes.add(mention.root_index)

        chains.sort(key=lambda chain: chain.mentions[0].root_index)

        for index, chain in enumerate(chains):
            chain.index = index
            for mention in chain.mentions:
                for token in (
                    doc[token_index] for token_index in mention.token_indexes
                ):
                    token._.coref_chains.chains.append(chain)

        doc._.coref_chains.chains = chains

        if not used_in_training:
            # get rid of the *temp_* properties on the various objects
            for temp_entry in [
                t for t in doc._.coref_chains.__dict__ if t.startswith("temp_")
            ][:]:
                doc._.coref_chains.__dict__.pop(temp_entry)
            for token in doc:
                for temp_entry in [
                    t
                    for t in token._.coref_chains.__dict__
                    if t.startswith("temp_")
                ][:]:
                    token._.coref_chains.__dict__.pop(temp_entry)
                    for chain in token._.coref_chains:
                        for mention in chain:
                            for inner_temp_entry in [
                                t
                                for t in mention.__dict__
                                if t.startswith("temp_")
                            ][:]:
                                mention.__dict__.pop(inner_temp_entry)

        return doc
