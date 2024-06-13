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

from spacy.tokens import Token

from ...data_model import Mention
from ...rules import RulesAnalyzer


class LanguageSpecificRulesAnalyzer(RulesAnalyzer):

    random_word = "treacle"

    or_lemmas = "or"

    entity_noun_dictionary = {
        "PERSON": ["person", "individual", "man", "woman"],
        "NORP": ["nation", "people", "ethnicity"],
        "FAC": ["building"],
        "ORG": ["company", "firm", "organisation"],
        "GPE": ["country", "state", "city", "town"],
        "LOC": ["place"],
        "LAW": ["law"],
        "LANGUAGE": ["language", "tongue"],
    }

    quote_tuples = [("'", "'"), ('"', '"'), ("“", "”"), ("‘", "’")]

    dependent_sibling_deps = "conj"

    conjunction_deps = ("appos", "cc", "punct")

    adverbial_clause_deps = ("advcl", "acl")

    term_operator_pos = "DET"

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
                if child not in visited_set
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
        if not (
            (
                token.pos_ in self.noun_pos
                and token.dep_ not in ("compound", "npadvmod")
            )
            or (token.tag_ == "CD" and token.dep_ != "nummod")
            or (token.tag_ == "DT" and token.dep_ != "det")
            or (token.pos_ == "PRON" and token.tag_ == "NN")
        ):
            return False
        return not self.is_token_in_one_of_phrases(
            token, self.blacklisted_phrases
        )

    def is_potential_anaphor(self, token: Token) -> bool:
        """Potentially externally referring tokens in English are third-person pronouns.
        Instances of 'it' have to be investigated further to find out if they are
        pleonastic."""
        # Is *token* a third-person pronoun?
        if token.tag_ not in ("PRP", "PRP$") or not self.has_morph(
            token, "Person", "3"
        ):
            return False
        if token.text.lower() != "it":
            return True

        # We have 'it' and have to find out if it is pleonastic...

        # Pleonastic it is out of the question in a conjunction environment
        if (
            len(token._.coref_chains.temp_dependent_siblings) > 0
            or token._.coref_chains.temp_governing_sibling is not None
        ):
            return True

        # e.g. '*It* is important that he has done it'
        for child in (
            child for child in token.children if child.dep_ == "amod"
        ):
            if (
                len(
                    [
                        grandchild
                        for grandchild in child.children
                        if grandchild.dep_ not in ("acomp", "xcomp")
                    ]
                )
                == 0
            ):
                return False

        # e.g. '*It* seems to be believed that he has done it'
        if (
            token.dep_ != "ROOT"
            and (
                token.head.lemma_ in ("be", "seem")
                or token.dep_ == "nsubjpass"
            )
            and len(
                [
                    child
                    for child in token.head.children
                    if child.dep_ in ("advcl", "ccomp", "xcomp")
                ]
            )
            > 0
        ):
            return False

        # e.g. 'This makes *it* unlikely that he has done it'
        if (
            token.dep_ != "ROOT"
            and token.i > 0
            and token.doc[token.i - 1].lemma_ == "make"
            and token.head.dep_ == "ccomp"
        ):
            return False

        # e.g. '*It* is in everyone's interest that attempting it should succeed'
        if token.dep_ in ("nsubj", "nsubjpass") and token.head.lemma_ == "be":
            for child in token.head.children:
                if (
                    len(
                        [
                            grandchild
                            for grandchild in child.children
                            if grandchild.dep_ == "relcl"
                        ]
                    )
                    > 0
                ):
                    return False

        # Avalent verbs, e.g. '*it* is snowing'
        if (
            token.dep_ != self.root_dep
            and token.head.pos_ == "VERB"
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

        doc = referring.doc
        referred_root = doc[referred.root_index]
        uncertain = False

        # e.g. 'the men and the women' ... 'they': 'they' cannot refer only to
        # 'the men' or 'the women'
        if (
            len(referred.token_indexes) == 1
            and self.has_morph(referring, "Number", "Plur")
            and self.is_involved_in_non_or_conjunction(referred_root)
        ):
            return 0

        # Two pronouns without coordination and differing number or gender
        if (
            len(referred.token_indexes) == 1
            and self.is_potential_anaphor(referred_root)
            and (
                referred_root.morph.get("Number")
                != referring.morph.get("Number")
                or referred_root.morph.get("Gender")
                != referring.morph.get("Gender")
            )
        ):
            return 0

        # Singular anaphor, plural referent
        if self.has_morph(referring, "Number", "Sing") and (
            len(referred.token_indexes) > 1
            or self.has_morph(referred_root, "Number", "Plur")
        ):
            return 0

        if not self.is_potential_anaphor(referred_root):
            # antecedent is a noun

            referred_lemma = referred_root.lemma_

            # 'they' referring to singular non-person noun
            if (
                self.has_morph(referring, "Number", "Plur")
                and len(referred.token_indexes) == 1
                and self.has_morph(referred_root, "Number", "Sing")
            ):
                if referred_lemma not in self.person_words:
                    if (
                        referred_root.tag_ != "NNP"
                        and referred_root.ent_type_ != "PERSON"
                    ):
                        return 0
                    else:
                        # named people who choose to refer to themselves with 'they'
                        uncertain = True
                if (
                    referred_lemma in self.exclusively_male_words
                    or referred_lemma in self.exclusively_female_words
                ):
                    uncertain = True

            # 'he' or 'she' referring to non-person, non-animal noun
            if (
                (
                    self.has_morph(referring, "Gender", "Masc")
                    or self.has_morph(referring, "Gender", "Fem")
                )
                and referred_lemma not in self.exclusively_person_words
                and referred_lemma not in self.animal_words
                and referred_lemma not in self.male_names
                and referred_lemma not in self.female_names
                and referred_root.ent_type_ != "PERSON"
            ):
                if (
                    referred_root.tag_ != "NNP"
                    and referred_lemma not in self.person_words
                ):
                    return 0
                else:
                    uncertain = True

            # 'it' referring to person noun or entity
            if self.has_morph(referring, "Gender", "Neut") and (
                referred_lemma in self.exclusively_person_words
                or referred_root.ent_type_ == "PERSON"
            ):
                return 0

            # 'it' referring to plural proper name
            if (
                self.has_morph(referring, "Gender", "Neut")
                and referred_root.tag_ == "NNPS"
            ):
                uncertain = True

            # 'he' referring to female noun
            if (
                self.has_morph(referring, "Gender", "Masc")
                and referred_lemma in self.exclusively_female_words
                and referred_lemma not in self.animal_words
            ):
                return 0

            # 'she' referring to male noun
            if (
                self.has_morph(referring, "Gender", "Fem")
                and referred_lemma in self.exclusively_male_words
                and referred_lemma not in self.animal_words
            ):
                return 0

            # 'it' referring to name
            if (
                self.has_morph(referring, "Gender", "Neut")
                and referred_root.tag_ == "NNP"
                and (
                    referred_lemma in self.male_names
                    or referred_lemma in self.female_names
                )
            ):
                return 0

            # 'he' referring to female name
            if (
                self.has_morph(referring, "Gender", "Masc")
                and referred_root.tag_ == "NNP"
                and self.has_list_member_in_propn_subtree(
                    doc[referred.root_index], self.exclusively_female_names
                )
            ):
                uncertain = True

            # 'she' referring to male name
            if (
                self.has_morph(referring, "Gender", "Fem")
                and referred_root.tag_ == "NNP"
                and self.has_list_member_in_propn_subtree(
                    doc[referred.root_index], self.exclusively_male_names
                )
            ):
                uncertain = True

        if directly:
            if (
                self.is_potential_reflexive_pair(referred, referring)
                and self.is_reflexive_anaphor(referring) == 0
            ):
                return 0

            if (
                not uncertain
                and not self.is_potential_reflexive_pair(referred, referring)
                and self.is_reflexive_anaphor(referring) == 1
            ):
                uncertain = True

        return 1 if uncertain else 2

    def is_potentially_indefinite(self, token: Token) -> bool:

        return (
            len(
                [
                    1
                    for child in token.children
                    if child.tag_ == "DT"
                    and child.dep_ == "det"
                    and child.lemma_ in ("a", "an", "some", "another")
                ]
            )
            > 0
        )

    def is_potentially_definite(self, token: Token) -> bool:

        return (
            len(
                [
                    1
                    for child in token.children
                    if child.tag_ == "DT"
                    and child.dep_ == "det"
                    and child.lemma_
                    in ("that", "the", "these", "this", "those")
                ]
            )
            > 0
        )

    def is_reflexive_anaphor(self, token: Token) -> int:
        if self.has_morph(token, "Reflex", "Yes"):
            return 1
        else:
            return 0

    @staticmethod
    def get_ancestor_spanning_any_preposition(token: Token) -> Token:
        if token.dep_ == "ROOT":
            return None
        head = token.head
        if token.dep_ == "pobj":
            if head.dep_ == "ROOT":
                return None
            head = head.head
        return head

    def is_potential_reflexive_pair(
        self, referred: Mention, referring: Token
    ) -> bool:

        if (
            referred.root_index > referring.i
        ):  # reflexives must follow their referents in English
            return False

        referred_root = referring.doc[referred.root_index]
        syntactic_subject_dep = ("nsubj", "nsubjpass")

        if referred_root._.coref_chains.temp_governing_sibling is not None:
            referred_root = referred_root._.coref_chains.temp_governing_sibling

        if referring._.coref_chains.temp_governing_sibling is not None:
            referring = referring._.coref_chains.temp_governing_sibling

        if referring.tag_ != "PRP":  # e.g. 'his' rather than 'him' 'himself'
            return False

        if referred_root.dep_ in syntactic_subject_dep:
            for referring_ancestor in referring.ancestors:
                # Loop up through the verb ancestors of the pronoun

                # Other dependencies imply clause types where reflexivity is no longer possible
                if referring_ancestor.pos_ in (
                    "VERB",
                    "AUX",
                ) and referring_ancestor.dep_ not in (
                    "ROOT",
                    "xcomp",
                    "pcomp",
                    "ccomp",
                    "conj",
                    "advcl",
                    "acl",
                ):
                    return False

                if referred_root in referring_ancestor.children:
                    return True

                # The ancestor has its own subject, so stop here
                if (
                    len(
                        [
                            t
                            for t in referring_ancestor.children
                            if t.dep_ in syntactic_subject_dep
                            and t != referred_root
                        ]
                    )
                    > 0
                ):
                    return False
            return False
        else:
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
