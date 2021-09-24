# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 15:37:10 2021

Script to keep track of some global config

@author: Abinaya.M02
"""

# Mapping of light and heavy transformations
map_transformation = {
    "light": [
        "add_hashtags",
        "adjectives_antonyms_switch",
        "butter_fingers_perturbation",
        "change_char_case",
        "change_date_format",
        "change_person_named_entities",
        "change_two_way_ne",
        "close_homophones_swap",
        "contraction_expansions",
        "country_state_abbreviation_transformation",
        "discourse_marker_substitution",
        "diverse_paraphrase",
        "emoji_icon_transformation",
        "emojify",
        "english_inflectional_variation",
        "entity_mention_replacement_ner",
        "gender_culture_diverse_name",
        "gender_culture_diverse_name_two_way",
        "gender_swap",
        "geonames_transformation",
        "greetings_and_farewells",
        "insert_abbreviation",
        "leet_letters",
        "longer_location_ner",
        "longer_names_ner",
        "mix_transliteration",
        "multilingual_dictionary_based_code_switch",
        "multilingual_lexicon_perturbation",
        "negate_strengthen",
        "number-to-word",
        "numeric_to_word",
        "p1_noun_transformation",
        "propbank_srl_roles",
        "random_deletion",
        "random_upper_transformation",
        "redundant_context_for_qa",
        "replace_numerical_values",
        "replace_spelling",
        "sentiment_emoji_augmenter",
        "suspecting_paraphraser",
        "swap_characters",
        "synonym_substitution",
        "whitespace_perturbation",
        "word_noise",
        "yes_no_question",
    ],
    "heavy": [
        "back_translation",
        "formality_change",
        "lexical_counterfactual_generator",
        "lost_in_translation",
        "mixed_language_perturbation",
        "multilingual_back_translation",
        "pinyin",
        "punctuation",
        "quora_trained_t5_for_qa",
        "sentence_reordering",
        "synonym_substitution",
        "token_replacement",
        "transformer_fill",
    ],
}

# Mapping of light and heavy filters
map_filter = {
    "light": [
        "code_mixing",
        "encoding",
        "group_inequity",
        "keywords",
        "lang",
        "length",
        "numeric",
        "polarity",
        "quantitative_ques",
        "question_filter",
        "repetitions",
        "soundex",
        "speech-tag",
        "token-amount",
        "yesno_question",
    ],
    "heavy": ["quantitative_ques", "toxicity"],
}
