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

    random_word = "szczęście"

    or_lemmas = ("albo", "lub")

    dependent_sibling_deps = "conj"

    conjunction_deps = ("cc", "punct")

    adverbial_clause_deps = ("ccomp", "dep", "advcl", "cop")

    entity_noun_dictionary = {
        "persName": ["człowiek", "osoba", "mężczyzna", "kobieta"],
        "placeName": ["miejsce", "miasto", "państwo", "kraj"],
        "orgName": [
            "firma",
            "przedsiębiorstwo",
            "organizacja",
            "zespół",
            "przedsięwzięcie",
        ],
    }

    quote_tuples = [
        ("'", "'"),
        ('"', '"'),
        ("„", "“"),
        ("‚", "‘"),
        ("«", "»"),
        ("»", "«"),
    ]

    term_operator_pos = ("DET", "ADP")

    clause_root_pos = ("VERB", "AUX", "ADJ")

    @staticmethod
    def is_reflexive_possessive_pronoun(token: Token) -> bool:
        return (
            token.pos_ == "DET"
            and token.tag_ == "ADJ"
            and token.lemma_[:4] in ("swój", "swoj", "swoi")
        )

    def get_dependent_siblings(self, token: Token) -> list:

        # As well as the standard conjunction found in other languages we also capture
        # comitative phrases where coordination is expressed using the pronoun 'z' and
        # a noun in the instrumental case.
        def add_siblings_recursively(
            recursed_token: Token, visited_set: set
        ) -> None:
            visited_set.add(recursed_token)
            siblings_set = set()
            if recursed_token.lemma_ in self.or_lemmas:
                token._.coref_chains.temp_has_or_coordination = True
            if (
                token != recursed_token
                and token.pos_ in ("VERB", "AUX")
                and self.is_potential_anaphor(token)
                and recursed_token.pos_ in ("VERB", "AUX")
                and self.is_potential_anaphor(recursed_token)
            ):
                # we treat two verb anaphors as having or coordination because two
                # singular anaphors do not give rise to a plural phrase
                token._.coref_chains.temp_has_or_coordination = True
            if (
                recursed_token.dep_ in self.dependent_sibling_deps
                or self.has_morph(recursed_token, "Case", "Ins")
            ) and recursed_token != token:
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
            for child in (
                child
                for child in recursed_token.children
                if recursed_token.pos_ in self.noun_pos
                and child.pos_ in self.noun_pos
                and self.has_morph(child, "Case", "Ins")
                and len(
                    [
                        1
                        for c in child.children
                        if c.dep_ == "case" and c.lemma_ == "z"
                    ]
                )
                > 0
                and child not in visited_set
            ):
                child_siblings_set = add_siblings_recursively(
                    child, visited_set
                )
                siblings_set |= child_siblings_set
            for child in (
                child
                for child in recursed_token.children
                if recursed_token.pos_ in ("VERB", "AUX")
                and self.is_potential_anaphor(recursed_token)
                and child.pos_ in self.noun_pos
                and self.has_morph(child, "Case", "Ins")
                and len(
                    [
                        1
                        for c in child.children
                        if c.dep_ == "case"
                        and c.lemma_ == "z"
                        and c.i - 1 == recursed_token.i
                    ]
                )
                > 0
                and child not in visited_set
            ):
                child_siblings_set = add_siblings_recursively(
                    child, visited_set
                )
                siblings_set |= child_siblings_set
            if recursed_token.dep_ != self.root_dep:
                # the 'z' sibling and this word are contiguous children of the same parent
                for child in (
                    child
                    for child in recursed_token.head.children
                    if recursed_token.pos_ in self.noun_pos
                    and child.pos_ in self.noun_pos
                    and self.has_morph(child, "Case", "Ins")
                    and len(
                        [
                            1
                            for c in child.children
                            if c.dep_ == "case"
                            and c.lemma_ == "z"
                            and c.i - 1 == recursed_token.i
                        ]
                    )
                    > 0
                    and child not in visited_set
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
        if not token.pos_ in self.noun_pos or token.text in punctuation:
            return False
        return not self.is_token_in_one_of_phrases(
            token, self.blacklisted_phrases
        )

    def is_potential_anaphor(self, token: Token) -> bool:
        # third-person pronoun
        if token.tag_ in ("PPRON3", "SIEBIE"):
            return True

        # reflexive third-person possessive pronoun
        if self.is_reflexive_possessive_pronoun(token):
            return True

        # finite verb without subject (zero anaphora)
        if (
            token.pos_ in ("VERB", "AUX")
            and token.tag_ in ("FIN", "PRAET", "BEDZIE")
            and len(
                [
                    child
                    for child in token.children
                    if child.dep_.startswith("nsubj")
                ]
            )
            == 0
            and not self.has_morph(token, "Person", "1")
            and not self.has_morph(token, "Person", "2")
        ):

            if (
                token._.coref_chains.temp_governing_sibling is not None
                and len(
                    [
                        child
                        for child in token._.coref_chains.temp_governing_sibling.children
                        if child.dep_.startswith("nsubj")
                    ]
                )
                > 0
            ):
                return False

            if (
                token.pos_ == "AUX"
                and token.dep_ != self.root_dep
                and len(
                    [
                        child
                        for child in token.head.children
                        if child.dep_.startswith("nsubj")
                    ]
                )
                > 0
            ):
                return False

            # exclude structures like 'okazało się, że ...'
            return not (
                len(
                    [
                        child
                        for child in token.children
                        if child.dep_ == "expl:pv"
                    ]
                )
                > 0
                and len(
                    [
                        child
                        for child in token.children
                        if child.dep_ == "ccomp"
                    ]
                )
                > 0
                and not self.has_morph(token, "Gender", "Masc")
                and not self.has_morph(token, "Gender", "Fem")
            )
        return False

    def is_potential_anaphoric_pair(
        self, referred: Mention, referring: Token, directly: bool
    ) -> bool:

        # masc:     'rodzaj męski'
        # fem:      'rodzaj żeński'
        # neut:     'rodzaj nijaki'
        # nonvirile:'rodzaj niemęskoosobowy'
        # virile:   'rodzaj męskoosobowy'

        def get_gender_number_info(token):
            masc = fem = neut = nonvirile = virile = False
            if self.has_morph(token, "Number", "Sing"):
                if self.has_morph(token, "Gender", "Masc"):
                    masc = True
                    if token.tag_ == "PPRON3" and not self.has_morph(
                        token, "Case", "Nom"
                    ):
                        neut = True
                if self.has_morph(token, "Gender", "Fem"):
                    fem = True
                if self.has_morph(token, "Gender", "Neut"):
                    neut = True
                    if token.tag_ == "PPRON3" and not self.has_morph(
                        token, "Case", "Nom"
                    ):
                        masc = True
                if token.pos_ == "PROPN":
                    if token.lemma_ in self.male_names:
                        masc = True
                    if token.lemma_ in self.female_names:
                        fem = True
            if self.has_morph(token, "Number", "Plur"):
                if (
                    self.has_morph(token, "Gender", "Masc")
                    and self.has_morph(token, "Animacy", "Hum")
                    and token.dep_ != "nmod"
                ):  # 'ich'
                    virile = True
                elif (
                    (
                        self.has_morph(token, "Gender", "Masc")
                        and self.has_morph(token, "Animacy", "Nhum")
                    )
                    or (
                        self.has_morph(token, "Gender", "Masc")
                        and self.has_morph(token, "Animacy", "Inan")
                    )
                    or self.has_morph(token, "Gender", "Fem")
                    or self.has_morph(token, "Gender", "Neut")
                ):
                    nonvirile = True
            if token.pos_ == "PROPN" and not directly:
                # common noun and proper noun in same chain may have different genders
                masc = fem = neut = nonvirile = virile = True
            return masc, fem, neut, nonvirile, virile

        def get_gender_number_info_for_single_token(token):

            masc = fem = neut = nonvirile = virile = False
            if not self.is_reflexive_possessive_pronoun(token):
                masc, fem, neut, nonvirile, virile = get_gender_number_info(
                    token
                )
                if (
                    not (masc or fem or neut or nonvirile or virile)
                    and token.dep_.startswith("nsubj")
                    and token.head.pos_ in ("VERB", "AUX")
                ):
                    (
                        masc,
                        fem,
                        neut,
                        nonvirile,
                        virile,
                    ) = get_gender_number_info(token.head)
                if not (masc or fem or neut or nonvirile or virile):
                    if self.has_morph(token, "Number", "Sing"):
                        masc = fem = neut = True
                    if self.has_morph(token, "Number", "Plur"):
                        nonvirile = virile = True
            if not (masc or fem or neut or nonvirile or virile):
                masc = fem = neut = nonvirile = virile = True
            return masc, fem, neut, nonvirile, virile

        def are_coordinated_tokens_possibly_virile(tokens: list) -> int:
            masc = fem = neut = False
            for token in tokens:
                if self.has_morph(token, "Gender", "Masc") and self.has_morph(
                    token, "Animacy", "Hum"
                ):
                    return 2
                if self.has_morph(token, "Gender", "Masc") and self.has_morph(
                    token, "Animacy", "Nhum"
                ):
                    masc = True
                if self.has_morph(token, "Gender", "Masc") and self.has_morph(
                    token, "Animacy", "Inan"
                ):
                    masc = True
                if self.has_morph(token, "Gender", "Fem"):
                    fem = True
                if self.has_morph(token, "Gender", "Neut"):
                    neut = True
            if (masc and fem) or (masc and neut) or (fem and neut):
                if tokens[0].dep_.startswith("nsubj") and tokens[
                    0
                ].head.pos_ in ("VERB", "AUX"):
                    (
                        _,
                        _,
                        _,
                        head_nonvirile,
                        head_virile,
                    ) = get_gender_number_info(tokens[0].head)
                    if head_nonvirile and not head_virile:
                        return 0  # only nonvirile
                    if head_virile and not head_nonvirile:
                        return 2  # only virile
                # The rules about whether to use virile or nonvirile nouns or pronouns where
                # a coordination phrase contains a mixture of genders are very complex and require
                # knowledge of the animacy of feminine and neuter nouns which the Spacy model does
                # not supply us with. For this reason, and because people often get the rules
                # wrong, we accept both virile and nonvirile anaphors when a coordination phrase
                # contained more than one nonvirile gender and there is no governing verb to
                # specify either virile or nonvirile gender.
                return 1  # either virile or nonvirile
            if len([t for t in tokens if self.has_morph(t, "Gender")]) == 0:
                return 1
            return 0  # only nonvirile

        doc = referring.doc
        referred_root = doc[referred.root_index]
        uncertain = False

        (
            referring_masc,
            referring_fem,
            referring_neut,
            referring_nonvirile,
            referring_virile,
        ) = get_gender_number_info_for_single_token(referring)

        if self.is_involved_in_non_or_conjunction(referred_root):
            if referred_root._.coref_chains.temp_governing_sibling is not None:
                all_involved_referreds = [
                    referred_root._.coref_chains.temp_governing_sibling
                ]
            else:
                all_involved_referreds = [referred_root]
            all_involved_referreds.extend(
                all_involved_referreds[
                    0
                ]._.coref_chains.temp_dependent_siblings
            )
        else:
            all_involved_referreds = [referred_root]

        # e.g. 'Janek był w domu. Zadzwonili z żoną ...'
        comitative_siblings = [
            c
            for c in referring._.coref_chains.temp_dependent_siblings
            if referring.pos_ in ("VERB", "AUX")
            and self.has_morph(referring, "Number", "Plur")
            and self.has_morph(c, "Case", "Ins")
            and c.i not in referred.token_indexes
        ]

        if (
            not directly
            and len(comitative_siblings) > 0
            and (referring_nonvirile or referring_virile)
        ):
            return 2

        all_involved_referreds.extend(comitative_siblings)

        referreds_included_here = [doc[i] for i in referred.token_indexes]
        referreds_included_here.extend(comitative_siblings)

        if len(all_involved_referreds) > 1:

            possibly_virile = are_coordinated_tokens_possibly_virile(
                all_involved_referreds
            )

            if len(referreds_included_here) == len(all_involved_referreds):
                if possibly_virile == 2:
                    if not referring_virile:
                        return 0
                elif possibly_virile == 1:
                    if not referring_nonvirile and not referring_virile:
                        return 0
                elif not referring_nonvirile:
                    return 0
                return 2

            if len(referreds_included_here) > 1:
                # implies len(all_involved_referreds) > len(referreds_included_here)
                referreds_included_here_possibly_virile = (
                    are_coordinated_tokens_possibly_virile(
                        referreds_included_here
                    )
                )
                if (
                    referring_nonvirile
                    and possibly_virile == 2
                    and referreds_included_here_possibly_virile == 0
                ):
                    return 2
                return 0

            (
                referred_masc,
                referred_fem,
                referred_neut,
                referred_nonvirile,
                referred_virile,
            ) = get_gender_number_info_for_single_token(referred_root)

            referred_comitative_siblings = [
                c
                for c in referred_root._.coref_chains.temp_dependent_siblings
                if referred_root.pos_ in ("VERB", "AUX")
                and self.has_morph(referred_root, "Number", "Plur")
                and self.has_morph(c, "Case", "Ins")
                and c.i != referring.i
            ]
            if (
                not directly
                and len(referred_comitative_siblings) > 0
                and (referred_nonvirile or referred_virile)
            ):
                return 2

            if (
                possibly_virile == 2
                and referred_nonvirile
                and referring_nonvirile
            ):
                return 2
            if referred_nonvirile or referred_virile:
                return 0
            if possibly_virile != 0 and referring_virile:
                return 0
            if possibly_virile != 2 and referring_nonvirile:
                return 0

        referred_masc = (
            referred_fem
        ) = referred_neut = referred_nonvirile = referred_virile = False

        for working_token in (doc[index] for index in referred.token_indexes):
            (
                working_masc,
                working_fem,
                working_neut,
                working_nonvirile,
                working_virile,
            ) = get_gender_number_info_for_single_token(working_token)
            referred_masc = referred_masc or working_masc
            referred_fem = referred_fem or working_fem
            referred_neut = referred_neut or working_neut
            referred_nonvirile = referred_nonvirile or working_nonvirile
            referred_virile = referred_virile or working_virile

        if (
            not (referred_masc and referring_masc)
            and not (referred_fem and referring_fem)
            and not (referred_neut and referring_neut)
            and not (referred_nonvirile and referring_nonvirile)
            and not (referred_virile and referring_virile)
        ):
            return 0

        if (
            self.is_reflexive_possessive_pronoun(referring)
            and referring.head.i in referred.token_indexes
        ):
            return 0

        if referred_root.head.i == referring.i:
            return 0

        if directly:
            if (
                self.is_potential_reflexive_pair(referred, referring)
                and self.is_reflexive_anaphor(referring) == 0
            ):
                return 0

            if (
                not self.is_potential_reflexive_pair(referred, referring)
                and self.is_reflexive_anaphor(referring) == 2
            ):
                return 0

            # possessive pronouns cannot refer back to the head within a genitive phrase.
            # This functionality is under 'directly' to improve performance.
            working_token = referring
            while working_token.dep_ != self.root_dep:
                if (
                    working_token.head.i in referred.token_indexes
                    and working_token.dep_ not in self.dependent_sibling_deps
                    and self.has_morph(working_token, "Case", "Gen")
                ):
                    return 0
                if (
                    working_token.dep_ not in self.dependent_sibling_deps
                    and (
                        working_token.dep_ != "nmod"
                        or not self.has_morph(working_token, "Case", "Gen")
                    )
                    and not self.is_reflexive_possessive_pronoun(working_token)
                ):
                    break
                working_token = working_token.head

        # Some verbs like 'mówić' require a personal subject
        referring_governing_sibling = referring
        if referring._.coref_chains.temp_governing_sibling is not None:
            referring_governing_sibling = (
                referring._.coref_chains.temp_governing_sibling
            )
        if (
            referring_governing_sibling.dep_.startswith("nsubj")
            and referring_governing_sibling.head.lemma_
            in self.verbs_with_personal_subject
        ) or referring.lemma_ in self.verbs_with_personal_subject:
            for working_token in (
                doc[index] for index in referred.token_indexes
            ):
                if (
                    working_token.pos_ == self.propn_pos
                    or working_token.ent_type_ == "persName"
                ):
                    return 2
            return 1

        return 1 if uncertain else 2

    def is_potentially_indefinite(self, token: Token) -> bool:

        if token.pos_ != "NOUN":
            return False
        for child in (
            child
            for child in token.children
            if child.pos_ in self.term_operator_pos
        ):
            if child.lemma_.lower() in (
                "ten",
                "tego",
                "temu",
                "tym",
                "to",
                "ta",
                "tę",
                "tą",
                "tej",
                "ci",
                "te",
                "tych",
                "tymi",
                "tym",
                "tych",
            ):
                return False
            if (
                child.pos_ == "DET"
                and child.tag_ == "ADJ"
                and child.dep_ == "det"
                and self.has_morph(child, "Poss", "Yes")
            ):
                return False
        return True

    def is_potentially_definite(self, token: Token) -> bool:

        if token.pos_ != "NOUN":
            return False
        for child in (
            child
            for child in token.children
            if child.pos_ in self.term_operator_pos
        ):
            if child.lemma_.lower().startswith("jak"):
                return False
        return True

    def is_reflexive_anaphor(self, token: Token) -> int:
        if token.tag_ == "SIEBIE" or self.is_reflexive_possessive_pronoun(
            token
        ):
            return 2
        if (
            token.tag_ == "PPRON3"
            and token.dep_ == "nmod"
            and self.has_morph(token, "PrepCase", "Npr")
        ):  # e.g. 'jego, jej, ich'
            return 1
        return 0

    def is_potential_reflexive_pair(
        self, referred: Mention, referring: Token
    ) -> bool:

        if (
            referring.pos_ != "PRON"
            and not self.is_reflexive_possessive_pronoun(referring)
        ):
            return False

        referred_root = referring.doc[referred.root_index]

        if referred_root._.coref_chains.temp_governing_sibling is not None:
            referred_root = referred_root._.coref_chains.temp_governing_sibling

        if referring._.coref_chains.temp_governing_sibling is not None:
            referring = referring._.coref_chains.temp_governing_sibling

        if referred_root.dep_.startswith("nsubj") or (
            referred_root.pos_ in ("VERB", "AUX")
            and self.is_potential_anaphor(referred_root)
        ):
            for referring_ancestor in referring.ancestors:

                # Loop up through the ancestors of the pronoun

                if (
                    referred_root == referring_ancestor
                    or referred_root in referring_ancestor.children
                ):
                    return True

                # The ancestor has its own subject, so stop here
                if (
                    len(
                        [
                            t
                            for t in referring_ancestor.children
                            if t.dep_.startswith("nsubj")
                            and t != referred_root
                        ]
                    )
                    > 0
                ):
                    return False

                if (
                    referring_ancestor._.coref_chains.temp_governing_sibling
                    == referred_root
                ):
                    return False

        return (
            referring.dep_ != self.root_dep
            and referred_root.dep_ != self.root_dep
            and (
                referring.head == referred_root.head
                or referring.head.i in referred.token_indexes
            )
            and referring.i > referred_root.i
        )
