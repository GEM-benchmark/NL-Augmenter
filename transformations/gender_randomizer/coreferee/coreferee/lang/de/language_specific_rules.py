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

from string import punctuation

from spacy.tokens import Token

from ...data_model import Mention
from ...rules import RulesAnalyzer


class LanguageSpecificRulesAnalyzer(RulesAnalyzer):

    random_word = "Freude"

    dependent_sibling_deps = "cj"

    conjunction_deps = ("app", "cd", "punct")

    adverbial_clause_deps = ("mo", "oc")

    or_lemmas = "oder"

    entity_noun_dictionary = {
        "PER": ["Person", "Mensch", "Mann", "Frau"],
        "LOC": ["Ort", "Platz", "Punkt", "Stelle", "Land", "Stadt"],
        "ORG": [
            "Firma",
            "Geschäft",
            "Gesellschaft",
            "Organisation",
            "Unternehmen",
        ],
    }

    quote_tuples = [
        ("'", "'"),
        ('"', '"'),
        ("„", "“"),
        ("‚", "‘"),
        ("«", "»"),
        ("‹", "›"),
    ]

    term_operator_pos = ("DET", "ADJ")

    clause_root_pos = ("VERB", "AUX")

    def get_dependent_siblings(self, token: Token) -> list:
        def add_siblings_recursively(
            recursed_token: Token, visited_set: set
        ) -> None:
            visited_set.add(recursed_token)
            siblings_set = set()
            if recursed_token.lemma_ in self.or_lemmas:
                token._.coref_chains.temp_has_or_coordination = True
            if recursed_token.dep_ in self.dependent_sibling_deps:
                siblings_set.add(recursed_token)
            for child in (
                child
                for child in recursed_token.children
                if child not in visited_set and
                # hyphenated siblings, e.g. 'Kindes- und Jugendzentrum'
                child.tag_ != "TRUNC"
                and (
                    child.dep_ in self.dependent_sibling_deps
                    or child.dep_ in self.conjunction_deps
                )
            ):
                child_siblings_set = add_siblings_recursively(
                    child, visited_set
                )
                siblings_set |= child_siblings_set
            return siblings_set

        if (
            token.dep_ not in self.conjunction_deps
            and token.dep_ not in self.dependent_sibling_deps
        ):
            siblings_set = add_siblings_recursively(token, set())
        else:
            siblings_set = set()
        return sorted(siblings_set)

    def is_independent_noun(self, token: Token) -> bool:
        if (
            not (
                token.pos_ in self.noun_pos
                or token.tag_ == "PIS"
                or (token.pos_ == "PRON" and token.tag_ == "NN")
            )
            or token.dep_ == "pnc"
            or token.text in punctuation
        ):
            return False
        return not self.is_token_in_one_of_phrases(
            token, self.blacklisted_phrases
        )

    def is_potential_anaphor(self, token: Token) -> bool:
        if not (
            (token.pos_ == "PRON" and token.tag_ in ("PPER", "PDS", "PRF"))
            or (token.pos_ == "DET" and token.tag_ == "PPOSAT")
            or (token.pos_ == "ADV" and token.tag_ == "PROAV")
        ):
            return False
        if self.has_morph(token, "Person", "1") or self.has_morph(
            token, "Person", "2"
        ):
            return False

        if (
            token.tag_ == "PPOSAT"
            and not token.text.lower().startswith("sein")
            and not token.text.lower().startswith("ihr")
        ):
            return False

        if token.tag_ == "PROAV":
            # 'damit' etc. in sentence-initial position refers to the preceding clause
            if (
                token.i
                == token.doc._.coref_chains.temp_sent_starts[
                    token._.coref_chains.temp_sent_index
                ]
            ):
                return False
            # 'sie machte es damit, dass ...'
            if (
                len(
                    [child for child in token.children if child.pos_ == "VERB"]
                )
                > 0
            ):
                return False
            if not token.lemma_.lower().startswith("da"):
                return False
            if token.lemma_.lower() in ("daher", "dahin"):
                return False

        # pleonastic 'es'
        if token.dep_ == "ep":
            return False

        # 'das'
        if token.text.lower() == "das":
            return False

        # avalent verbs
        if (
            token.dep_ != self.root_dep
            and token.head.pos_ in ("AUX", "VERB")
            and len(
                [
                    child
                    for child in token.head.subtree
                    if child.lemma_ in self.avalent_verbs
                ]
            )
            > 0
        ):
            return False
        return True

    def is_potential_anaphoric_pair(
        self, referred: Mention, referring: Token, directly: bool
    ) -> bool:
        def lemma_ends_with_word_in_list(token, word_list):
            lower_lemma = token.lemma_.lower()
            for word in word_list:
                if word.lower().endswith(lower_lemma):
                    return True
            return False

        def get_gender_number_info(token):
            masc = fem = neut = plur = False
            if token.tag_ != "PPOSAT":
                if self.has_morph(token, "Number", "Sing"):
                    if self.has_morph(token, "Gender", "Masc"):
                        masc = True
                    if self.has_morph(token, "Gender", "Fem"):
                        fem = True
                    if self.has_morph(token, "Gender", "Neut"):
                        neut = True
                        if lemma_ends_with_word_in_list(
                            token, self.neuter_person_words
                        ):
                            masc = True
                            fem = True
                        if lemma_ends_with_word_in_list(
                            token, self.neuter_male_words
                        ):
                            masc = True
                        if lemma_ends_with_word_in_list(
                            token, self.neuter_female_words
                        ):
                            fem = True
                        if (
                            not masc
                            and not fem
                            and (
                                token.lemma_.lower().endswith("chen")
                                or token.lemma_.lower().endswith("lein")
                                and len(token.lemma_) > 6
                            )
                        ):
                            masc = True
                            fem = True
                    if token.pos_ == "PROPN":
                        if token.lemma_ in self.male_names:
                            masc = True
                        if token.lemma_ in self.female_names:
                            fem = True
                        if (
                            token.lemma_ not in self.male_names
                            and token.lemma_ not in self.female_names
                        ):
                            masc = fem = neut = True
                if self.has_morph(token, "Number", "Plur"):
                    plur = True
            if token.pos_ == "PROPN" and not directly:
                # common noun and proper noun in same chain may have different genders
                masc = fem = neut = plur = True
            if self.is_potential_anaphor(token):
                if token.tag_ in ("PROAV", "PRF"):
                    masc = True
                    fem = True
                    neut = True
                    plur = True
                elif token.tag_ == "PPOSAT":
                    if token.text.lower().startswith("sein"):
                        masc = True
                        neut = True
                    elif token.text.lower().startswith("ihr"):
                        fem = True
                        plur = True
                else:
                    if (
                        self.has_morph(token, "Number", "Sing")
                        and self.has_morph(token, "Gender", "Masc")
                        and (
                            self.has_morph(token, "Case", "Dat")
                            or self.has_morph(token, "Case", "Gen")
                        )
                    ):
                        neut = True
                    elif (
                        self.has_morph(token, "Number", "Sing")
                        and self.has_morph(token, "Gender", "Fem")
                        and (
                            self.has_morph(token, "Case", "Acc")
                            or self.has_morph(token, "Case", "Gen")
                        )
                    ):
                        plur = True
            return masc, fem, neut, plur

        doc = referring.doc
        referred_root = doc[referred.root_index]

        (
            referring_masc,
            referring_fem,
            referring_neut,
            referring_plur,
        ) = get_gender_number_info(referring)

        # e.g. 'die Männer und die Frauen' ... 'sie': 'sie' cannot refer only to
        # 'die Männer' or 'die Frauen'
        if (
            len(referred.token_indexes) == 1
            and referring_plur
            and self.is_involved_in_non_or_conjunction(referred_root)
        ):
            return 0

        referred_masc = referred_fem = referred_neut = referred_plur = False

        if len(
            referred.token_indexes
        ) > 1 and self.is_involved_in_non_or_conjunction(referred_root):
            referred_plur = True
            if not referring_plur:
                return 0

        for working_token in (doc[index] for index in referred.token_indexes):
            (
                working_masc,
                working_fem,
                working_neut,
                working_plur,
            ) = get_gender_number_info(working_token)
            referred_masc = referred_masc or working_masc
            referred_fem = referred_fem or working_fem
            referred_neut = referred_neut or working_neut
            referred_plur = referred_plur or working_plur

        if (
            not (referred_masc and referring_masc)
            and not (referred_fem and referring_fem)
            and not (referred_neut and referring_neut)
            and not (referred_plur and referring_plur)
        ):
            return 0

        # 'damit' etc. does not refer to nouns over several sentences
        if referring.tag_ == "PROAV":

            # 'damit' etc. does not refer to nouns over several sentences
            if (
                referring._.coref_chains.temp_sent_index
                - referred_root._.coref_chains.temp_sent_index
                > 1
            ):
                return 0

            # 'damit' etc. cannot refer to people, places or organisations or to male or female
            # anaphors
            for working_token in (
                doc[index] for index in referred.token_indexes
            ):
                if (
                    working_token.lemma_ in self.male_names
                    or working_token.lemma_ in self.female_names
                    or working_token.ent_type_ in ("PER", "LOC", "ORG")
                ):
                    return 0
                if self.is_potential_anaphor(working_token) and (
                    referred_masc or referred_fem
                ):
                    return 0

            # 'damit' cannot refer forward to a noun
            if referring.i < referred.root_index:
                return 0

        if directly:
            if self.is_potential_reflexive_pair(referred, referring) != (
                self.is_reflexive_anaphor(referring) == 2
            ):
                return 0

            if referring.tag_ == "PPOSAT":
                # possessive pronouns cannot refer back to the head within a genitive phrase.
                # This functionality is under 'directly' to improve performance.
                working_token = referring
                while working_token.dep_ != self.root_dep:
                    if (
                        working_token.head.i in referred.token_indexes
                        and not working_token.dep_ in self.conjunction_deps
                    ):
                        return 0
                    if (
                        working_token.dep_ not in self.conjunction_deps
                        and working_token.dep_
                        not in self.dependent_sibling_deps
                        and working_token.dep_ != "ag"
                        and working_token.tag_ != "PPOSAT"
                    ):
                        break
                    working_token = working_token.head

        referring_governing_sibling = referring
        if referring._.coref_chains.temp_governing_sibling is not None:
            referring_governing_sibling = (
                referring._.coref_chains.temp_governing_sibling
            )
        if (
            referring_governing_sibling.dep_ == "sb"
            and referring_governing_sibling.head.lemma_
            in self.verbs_with_personal_subject
        ):
            for working_token in (
                doc[index] for index in referred.token_indexes
            ):
                if (
                    working_token.pos_ == self.propn_pos
                    or working_token.ent_type_ == "PER"
                ):
                    return 2
            return 1

        return 2

    def is_potentially_indefinite(self, token: Token) -> bool:

        for child in (
            child
            for child in token.children
            if child.pos_ in self.term_operator_pos
        ):
            for lemma_beginning in ("ein", "irgendein"):
                if child.lemma_.lower().startswith(lemma_beginning):
                    return True
        return False

    def is_potentially_definite(self, token: Token) -> bool:

        for child in (
            child
            for child in token.children
            if child.pos_ in self.term_operator_pos
        ):
            for lemma_beginning in ("der", "dies", "jen"):
                if child.lemma_.lower().startswith(lemma_beginning):
                    return True
        return False

    def is_reflexive_anaphor(self, token: Token) -> int:
        if token.tag_ == "PRF":
            return 2
        else:
            return 0

    @staticmethod
    def get_ancestor_spanning_any_preposition(token: Token) -> Token:
        if token.dep_ == "ROOT":
            return None
        head = token.head
        if head.pos_ == "ADP" and token.dep_ == "nk":
            if head.dep_ == "ROOT":
                return None
            head = head.head
        return head

    def is_potential_reflexive_pair(
        self, referred: Mention, referring: Token
    ) -> bool:

        if referring.pos_ != "PRON":
            return False

        referred_root = referring.doc[referred.root_index]

        if referred_root._.coref_chains.temp_governing_sibling is not None:
            referred_root = referred_root._.coref_chains.temp_governing_sibling

        if referring._.coref_chains.temp_governing_sibling is not None:
            referring = referring._.coref_chains.temp_governing_sibling

        if referred_root.dep_ == "sb":
            for referring_ancestor in referring.ancestors:
                # Loop up through the verb ancestors of the pronoun

                if referred_root in referring_ancestor.children:
                    return True

                # The ancestor has its own subject, so stop here
                if (
                    len(
                        [
                            t
                            for t in referring_ancestor.children
                            if t.dep_ == "sb" and t != referred_root
                        ]
                    )
                    > 0
                ):
                    return False
            return False

        referring_ancestor = self.get_ancestor_spanning_any_preposition(
            referring
        )
        referred_ancestor = self.get_ancestor_spanning_any_preposition(
            referred_root
        )
        return referring_ancestor is not None and (
            referring_ancestor == referred_ancestor
            or referring_ancestor.i in referred.token_indexes
        )
