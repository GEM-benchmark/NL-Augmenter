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

import importlib
import sys
from abc import ABC, abstractmethod
from os import sep
from threading import Lock

import pkg_resources
from spacy.tokens import Doc, Token

from .data_model import ChainHolder, Mention

language_to_rules = {}
lock = Lock()


class RulesAnalyzerFactory:
    @staticmethod
    def get_rules_analyzer(nlp):
        def read_in_data_files(directory: str, rules_analyzer):
            for data_filename in (
                filename
                for filename in pkg_resources.resource_listdir(
                    __name__, sep.join(("lang", directory, "data"))
                )
                if filename.endswith(".dat")
            ):
                full_data_filename = pkg_resources.resource_filename(
                    __name__,
                    sep.join(("lang", directory, "data", data_filename)),
                )
                with open(full_data_filename, "r", encoding="utf-8") as file:
                    setattr(
                        rules_analyzer,
                        data_filename[:-4],
                        [
                            v.strip()
                            for v in file.read().splitlines()
                            if len(v.strip()) > 1
                            and not v.strip().startswith("#")
                        ],
                    )

        language = nlp.meta["lang"]
        with lock:
            if language not in language_to_rules:
                language_specific_rules_module = importlib.import_module(
                    ".".join(
                        (".lang", nlp.meta["lang"], "language_specific_rules")
                    ),
                    "coreferee",
                )
                rules_analyzer = (
                    language_specific_rules_module.LanguageSpecificRulesAnalyzer()
                )
                language_to_rules[language] = rules_analyzer
                read_in_data_files(language, rules_analyzer)
                read_in_data_files("common", rules_analyzer)
                rules_analyzer.exclusively_male_names = [
                    name
                    for name in rules_analyzer.male_names
                    if name not in rules_analyzer.female_names
                ]
                rules_analyzer.exclusively_female_names = [
                    name
                    for name in rules_analyzer.female_names
                    if name not in rules_analyzer.male_names
                ]
            return language_to_rules[language]


class RulesAnalyzer(ABC):

    # MUST BE IMPLEMENTED BY IMPLEMENTING SUBCLASSES:

    # A word in the language that will have a vector in any model that has vectors
    random_word = NotImplemented

    # A tuple of lemmas meaning 'or'.
    or_lemmas = NotImplemented

    # A dictionary from entity labels to lists of nouns that refer to entities with those labels,
    # e.g. {'PERSON': ['person', 'man', 'woman'], ...}
    entity_noun_dictionary = NotImplemented

    # A list of two-member tuples that can be used to begin and end quotations respectively,
    # e.g. [('“', '”')]
    quote_tuples = NotImplemented

    # Dependency labals that mark dependent siblings
    dependent_sibling_deps = NotImplemented

    # Dependency labels that mark linking elements in a conjunction phrase.
    conjunction_deps = NotImplemented

    # Dependency labels that mark predicates within adverbial clauses.
    adverbial_clause_deps = NotImplemented

    # A tuple of parts of speech that term operators can have. Term operators are determiners and -
    # in languages where prepositions depend on nouns in prepositional phrases - prepositions.
    term_operator_pos = NotImplemented

    # A tuple of parts of speech that can form the root of clauses.
    clause_root_pos = NotImplemented

    @abstractmethod
    def get_dependent_siblings(self, token: Token) -> list:
        """Returns a list of tokens that are dependent siblings of *token*. The method must
        additionally set *token._.coref_chains.temp_has_or_coordination = True* for all
        tokens with dependent siblings that are linked to those siblings by an *or*
        relationship."""

    @abstractmethod
    def is_independent_noun(self, token: Token) -> bool:
        """Returns *True* if *token* heads a noun phrase.
        Being an independent noun and being a potential anaphor are mutually exclusive.
        """

    @abstractmethod
    def is_potential_anaphor(self, token: Token) -> bool:
        """Returns *True* if *token* is a potential anaphor, e.g. a pronoun like 'he', 'she'.
        Being an independent noun and being a potential anaphor are mutually exclusive.
        """

    @abstractmethod
    def is_potential_anaphoric_pair(
        self, referred: Mention, referring: Token, directly: bool
    ) -> bool:
        """Returns *2* if the rules would permit *referred* and *referring* to co-exist
        within a chain, *0* if they would not and *1* if coexistence is unlikely.
        if *directly==True*, the question concerns direct coreference between the two
        elements; if *directly==False* the question concerns coexistence in a chain.
        For example, although 'himself' is unlikely to refer directly to 'he' in a non-reflexive
        situation, the same two pronouns can easily coexist within a chain, while 'he' and 'she'
        can never coexist anywhere within the same chain.

        Implementations of this method may need to exclude special cases of incorrect
        cataphoric (forward-referring) pronouns picked up by the general (non language-
        specific) method below.
        """

    @abstractmethod
    def is_potentially_indefinite(self, token: Token) -> bool:
        """Returns *True* if *token* heads a common noun phrase that is indefinite, or — in
        languages that do not mark indefiniteness — which could be interpreted as being indefinite.

        *False* should be returned if *token* is a proper noun.
        """

    @abstractmethod
    def is_potentially_definite(self, token: Token) -> bool:
        """Returns *True* if *token* heads a common noun phrase that is definite, or — in
        languages that do not mark definiteness — which could be interpreted as being definite.

        *False* should be returned if *token* is a proper noun.
        """

    @abstractmethod
    def is_reflexive_anaphor(self, token: Token) -> int:
        """Returns *2* if *token* expresses an anaphor which MUST be used reflexively, e.g.
        'sich' in German; *1* if *token* expresses an anaphor which MAY be used reflexively,
        e.g. 'himself'; *0* if *token* expresses an anaphor which MUST NOT be used reflexively,
        e.g. 'him'.
        """

    @abstractmethod
    def is_potential_reflexive_pair(
        self, referred: Mention, referring: Token
    ) -> bool:
        """Returns *True* if *referring* stands in a syntactic relationship to
        *referred* that would require a reflexive anaphor if the two elements belonged to the
        same chain e.g. 'he saw himself', but also 'he saw him' (where the non-reflexive
        anaphor would _preclude_ the two elements from being in the same chain).

        *True* should only be returned in syntactic positions where reflexive anaphors are
        observed for the language in question. For example, Polish has reflexive possessive
        pronouns but German does not, so *True* is returned for Polish in situations where
        *False* is returned for German. In a language without reflexive anaphors, *False*
        should always be returned.

        In many languages reflexive anaphors can precede their referents: in languages where
        this is not the case, the method should check that *referred.root_index < referring.i*.
        """

    # MAY BE OVERRIDDEN BY IMPLEMENTING SUBCLASSES:

    maximum_anaphora_sentence_referential_distance = 5

    maximum_coreferring_nouns_sentence_referential_distance = 2

    training_epochs = 4

    root_dep = "ROOT"

    # A tuple of parts of speech that can head predications semantically, i.e. verbs
    # (but not auxiliaries)
    verb_pos = "VERB"

    # A tuple of parts of speech that nouns can have.
    noun_pos = ("NOUN", "PROPN")

    # A tuple of parts of speech that proper nouns can have.
    propn_pos = "PROPN"

    number_morph_key = "Number"

    # COULD BE OVERRIDDEN BY IMPLEMENTING CLASSES, BUT THIS IS NOT EXPECTED
    # TO BE NECESSARY:

    def __init__(self):
        self.reverse_entity_noun_dictionary = {}
        for entity_type, values in self.entity_noun_dictionary.items():
            for value in values:
                assert value not in self.reverse_entity_noun_dictionary
                self.reverse_entity_noun_dictionary[
                    value.lower()
                ] = entity_type

    def initialize(self, doc: Doc) -> None:
        """Adds *ChainHolder* objects to *doc* as well as to each token in *doc*
        and stores temporary information on the objects that will be required during further
        processing."""

        doc._.coref_chains = ChainHolder()
        for token in doc:
            token._.coref_chains = ChainHolder()

        # Adds to *doc* a list of the start indexes of the sentences it contains.
        doc._.coref_chains.temp_sent_starts = [s[0].i for s in doc.sents]

        # Adds to each token in *doc* the index of the sentence that contains it.
        for index, sent in enumerate(doc.sents):
            for token in sent:
                token._.coref_chains.temp_sent_index = index

        # For each token in *doc*, if the token has dependent siblings, adds to the
        # *CorefChainHolder* instance of the token a list containing them, otherwise an empty list.
        # Wherever token B is added as a dependent sibling of token A, A is also added to B as a
        # governing sibling.
        for token in doc:
            siblings_list = self.get_dependent_siblings(token)
            token._.coref_chains.temp_dependent_siblings = siblings_list
            for sibling in (
                sibling for sibling in siblings_list if sibling.i != token.i
            ):
                if token._.coref_chains.temp_governing_sibling is None:
                    # in Polish some nouns can form part of two chains
                    sibling._.coref_chains.temp_governing_sibling = token

        #Adds an array representing which quotes the word is within. Note that the failure
        # to end a quotation within a document will not cause any problems because the neural
        # network is only given the information whether two members of a potential pair have
        # the same quote array or a different quote array.
        working_quote_array = [0 for entry in self.quote_tuples]
        for token in doc:
            for index, quote_tuple in enumerate(self.quote_tuples):
                if (
                    working_quote_array[index] == 0
                    and token.text == quote_tuple[0]
                ):
                    working_quote_array[index] = 1
                elif (
                    working_quote_array[index] == 1
                    and token.text == quote_tuple[1]
                ):
                    working_quote_array[index] = 0
            token._.coref_chains.temp_quote_array = working_quote_array[:]

        # Adds to each potential anaphora a list of potential referred mentions.
        for token in doc:
            token._.coref_chains.temp_potentially_referring = (
                self.is_independent_noun(token)
            )
            if self.is_potential_anaphor(token):
                potential_referreds = []
                this_sentence_start_index = token.sent[0].i
                this_sentence_number = (
                    doc._.coref_chains.temp_sent_starts.index(
                        this_sentence_start_index
                    )
                )
                start_sentence_number = 0
                if (
                    this_sentence_number
                    > self.maximum_anaphora_sentence_referential_distance
                ):
                    start_sentence_number = (
                        this_sentence_number
                        - self.maximum_anaphora_sentence_referential_distance
                    )
                for preceding_token in (
                    t
                    for t in doc[
                        doc._.coref_chains.temp_sent_starts[
                            start_sentence_number
                        ]: token.i
                    ]
                    if (
                        self.is_potential_anaphor(t)
                        or self.is_independent_noun(t)
                    )
                ):
                    simple_referred = Mention(preceding_token, False)
                    if self.language_independent_is_potential_anaphoric_pair(
                        simple_referred, token
                    ) > 0 and not self.is_potential_reflexive_pair(
                        Mention(token, False), doc[simple_referred.root_index]
                    ):
                        potential_referreds.append(simple_referred)
                    if (
                        len(
                            preceding_token._.coref_chains.temp_dependent_siblings
                        )
                        > 0
                    ):
                        complex_referred = Mention(preceding_token, True)
                        if (
                            self.language_independent_is_potential_anaphoric_pair(
                                complex_referred, token
                            )
                            > 0
                        ):
                            potential_referreds.append(complex_referred)
                if this_sentence_number + 1 == len(
                    doc._.coref_chains.temp_sent_starts
                ):
                    succeeding_tokens = doc[token.i + 1:]
                else:
                    succeeding_tokens = doc[
                        token.i
                        + 1: doc._.coref_chains.temp_sent_starts[
                            this_sentence_number + 1
                        ]
                    ]
                for succeeding_token in (
                    t
                    for t in succeeding_tokens
                    if (
                        self.is_potential_anaphor(t)
                        or self.is_independent_noun(t)
                    )
                ):
                    simple_referred = Mention(succeeding_token, False)
                    if self.language_independent_is_potential_anaphoric_pair(
                        simple_referred, token
                    ) > 0 and (
                        self.is_potential_cataphoric_pair(
                            simple_referred, token
                        )
                        or self.is_potential_reflexive_pair(
                            simple_referred, token
                        )
                    ):
                        potential_referreds.append(simple_referred)
                    if (
                        len(
                            succeeding_token._.coref_chains.temp_dependent_siblings
                        )
                        > 0
                    ):
                        complex_referred = Mention(succeeding_token, True)
                        if self.language_independent_is_potential_anaphoric_pair(
                            complex_referred, token
                        ) > 0 and self.is_potential_cataphoric_pair(
                            simple_referred, token
                        ):
                            potential_referreds.append(complex_referred)
                if len(potential_referreds) > 0:
                    token._.coref_chains.temp_potential_referreds = (
                        potential_referreds
                    )

    def is_potentially_introducing_noun(self, token: Token) -> bool:
        # We are not considering coordination

        if self.is_potentially_indefinite(token):
            return True

        # Definite noun phrases with additional children, e.g. 'the man who ...'
        return (
            self.is_potentially_definite(token)
            and len(
                [
                    child
                    for child in token.children
                    if child.pos_ not in self.term_operator_pos
                    and child.dep_ not in self.conjunction_deps
                    and child.dep_ not in self.dependent_sibling_deps
                ]
            )
            > 0
        )

    def is_potentially_referring_back_noun(self, token: Token) -> bool:

        return (
            self.is_potentially_definite(token)
            and len(
                [
                    child
                    for child in token.children
                    if child.pos_ not in self.term_operator_pos
                    and child.dep_ not in self.conjunction_deps
                    and child.dep_ not in self.dependent_sibling_deps
                ]
            )
            == 0
        )

    def is_potential_coreferring_noun_pair(
        self, referred: Token, referring: Token
    ) -> bool:
        """Returns *True* if *referred* and *referring* are potentially coreferring nouns.
        The method presumes that *is_independent_noun(token)* has
        already returned *True* for both *referred* and *referring* and that
        *referred* precedes *referring* within the document.
        """
        if (
            referred.pos_ not in self.noun_pos
            or referring.pos_ not in self.noun_pos
        ):
            return False

        if referring in referred._.coref_chains.temp_dependent_siblings:
            return False

        # If *referred* and *referring* are names that potentially consist of several words,
        # the text of *referring* must correspond to the end of the text of *referred*
        # e.g. 'Richard Paul Hudson' -> 'Hudson'
        referred_propn_subtree = self.get_propn_subtree(referred)
        if referring in referred_propn_subtree:
            return False
        if len(referred_propn_subtree) > 0:
            referring_propn_subtree = self.get_propn_subtree(referring)
            if len(referring_propn_subtree) > 0 and " ".join(
                t.text for t in referred_propn_subtree
            ).endswith(" ".join(t.text for t in referring_propn_subtree)):
                return True
            if len(referring_propn_subtree) > 0 and " ".join(
                t.lemma_.lower() for t in referred_propn_subtree
            ).endswith(
                " ".join(t.lemma_.lower() for t in referring_propn_subtree)
            ):
                return True

        # e.g. 'BMW' -> 'the company'
        if (
            referring.lemma_.lower() in self.reverse_entity_noun_dictionary
            and referred.pos_ in self.propn_pos
            and referred.ent_type_
            == self.reverse_entity_noun_dictionary[referring.lemma_.lower()]
            and self.is_potentially_definite(referring)
        ):
            return True
        if not self.is_potentially_referring_back_noun(referring):
            return False
        if not self.is_potentially_introducing_noun(
            referred
        ) and not self.is_potentially_referring_back_noun(referred):
            return False
        if referred.lemma_ == referring.lemma_ and referred.morph.get(
            self.number_morph_key
        ) == referring.morph.get(self.number_morph_key):
            return True
        return False

    def language_independent_is_potential_anaphoric_pair(
        self, referred: Mention, referring: Token
    ) -> bool:
        """Calls *is_potential_anaphoric_pair*, then sets *referred.temp_is_uncertain* depending
        on the result and on additional language-independent tests. Because this method
        is not called from *Annotator*, all language-independent tests are understood to
        apply to the *directly* situation explained above in *is_potential_anaphoric_pair*."""

        # all common tests are 'directly' tests
        doc = referring.doc
        referred_root = doc[referred.root_index]
        if referring in referred_root._.coref_chains.temp_dependent_siblings:
            return 0

        result = self.is_potential_anaphoric_pair(referred, referring, True)

        # Checks whether there a token with the same lemma as one of the tokens in *referred* that
        # is closer to *referring* in the structure than *referred* is and the two tokens form
        # a potential coreferring noun pair.
        if result == 2 and not self.is_potential_anaphor(referred_root):
            doc = referring.doc
            referring_or_governor = referring
            while True:
                referring_or_governor_subtree = list(
                    referring_or_governor.subtree
                )
                if referred_root in referring_or_governor_subtree:
                    break
                for referring_sub_token in referring_or_governor_subtree:
                    for referred_token in (
                        doc[i] for i in referred.token_indexes
                    ):
                        if self.is_potential_coreferring_noun_pair(
                            referred_token, referring_sub_token
                        ):
                            result = 1
                            break
                    if result == 1:
                        break
                if referring_or_governor.dep_ == "ROOT":
                    break
                referring_or_governor = referring_or_governor.head

        # Checks whether the two words have different quote arrays
        if (
            result == 2
            and referred_root._.coref_chains.temp_quote_array
            != referring._.coref_chains.temp_quote_array
        ):
            result = 1

        if result == 1:
            referred.temp_is_uncertain = True
        elif result == 2:
            referred.temp_is_uncertain = False
        return result

    def has_list_member_in_propn_subtree(
        self, token: Token, word_list: list
    ) -> bool:
        """Returns *True* if a member of the proper-name subtree of *Token*
        corresponds to a member of *word_list*.
        """
        for sub_token in self.get_propn_subtree(token):
            if sub_token.lemma_ in word_list:
                return True
        return False

    def get_propn_subtree(self, token: Token) -> list:
        """Returns a list containing each member M of the subtree of *token* that are proper nouns
        and where all the tokens between M and *token* are themselves proper nouns. If *token*
        is itself not a proper noun or if the head of *token* is a proper noun, an empty list
        is returned.
        """
        if token.pos_ not in self.propn_pos:
            return []
        if (
            token.dep_ != self.root_dep
            and token.dep_ not in self.dependent_sibling_deps
            and token.head.pos_ in self.propn_pos
        ):
            return []
        subtree = list(token.subtree)
        before_start_index = -1
        after_end_index = sys.maxsize
        for subtoken in subtree:
            if (
                subtoken.pos_ not in self.propn_pos
                and subtoken.i < token.i
                and before_start_index < subtoken.i
            ):
                before_start_index = subtoken.i
            elif (
                subtoken.pos_ not in self.propn_pos
                and subtoken.i > token.i
                and after_end_index > subtoken.i
            ):
                after_end_index = subtoken.i
        return [
            t
            for t in subtree
            if t.i > before_start_index and t.i < after_end_index
        ]

    @staticmethod
    def has_morph(token: Token, key: str, value: str = None) -> bool:
        """Returns *True* if  *token* has morphological feature *key*. If *value* is supplied,
        additionally checks that the list contains *value*."""
        if value is None:
            return len(token.morph.get(key)) > 0
        return value in token.morph.get(key)

    @staticmethod
    def is_involved_in_non_or_conjunction(token: Token) -> bool:
        """Returns *True* if *token* is part of a conjunction phrase that does not contain an or-
        lemma."""
        if len(token._.coref_chains.temp_dependent_siblings) > 0:
            return not token._.coref_chains.temp_has_or_coordination
        if token._.coref_chains.temp_governing_sibling is not None:
            return (
                not token._.coref_chains.temp_governing_sibling._.coref_chains.temp_has_or_coordination
            )
        return False

    @staticmethod
    def is_token_in_one_of_phrases(token: Token, phrases: list) -> bool:
        """Checks whether *token* is part of a phrase that is listed in *phrases*."""
        doc = token.doc
        token_text = token.text.lower()
        for phrase in phrases:
            phrase_words = phrase.lower().split()
            if token_text not in phrase_words:
                continue
            possible_index = phrase_words.index(token_text)
            start_index = max(0, token.i - possible_index)
            end_index = token.i + len(phrase_words) - possible_index
            if phrase.lower() == " ".join(
                [t.text.lower() for t in doc[start_index:end_index]]
            ):
                return True
        return False

    def is_potential_cataphoric_pair(
        self, referred: Mention, referring: Token
    ) -> bool:
        """Checks whether *referring* can refer cataphorically to *referred*, i.e.
        where *referring* precedes *referred* in the text. That *referring* precedes
        *referred* is not itself checked by the method.
        """

        doc = referring.doc
        referred_root = doc[referred.root_index]

        if referred_root.sent != referring.sent:
            return False
        if self.is_potential_anaphor(referred_root):
            return False

        referred_verb_ancestors = []
        # Find the ancestors of the referent that are verbs, stopping anywhere where there
        # is conjunction between verbs
        for ancestor in referred_root.ancestors:
            if ancestor.pos_ in self.clause_root_pos:
                referred_verb_ancestors.append(ancestor)
            if ancestor.dep_ in self.dependent_sibling_deps:
                break

        # Loop through the ancestors of the referring pronoun that are verbs,  that are not
        # within the first list and that have an adverbial clause dependency label
        referring_inclusive_ancestors = [referring]
        referring_inclusive_ancestors.extend(referring.ancestors)
        if (
            len(
                [
                    1
                    for ancestor in referring_inclusive_ancestors
                    if ancestor.dep_ in self.adverbial_clause_deps
                ]
            )
            == 0
        ):
            return False
        for referring_verb_ancestor in (
            t
            for t in referring_inclusive_ancestors
            if t.pos_ in self.clause_root_pos
            and t not in referred_verb_ancestors
        ):
            # If one of the elements of the second list has one of the elements of the first list
            # within its ancestors, we have subordination and cataphora is permissible
            if (
                len(
                    [
                        t
                        for t in referring_verb_ancestor.ancestors
                        if t in referred_verb_ancestors
                    ]
                )
                > 0
            ):
                return True
        return False
