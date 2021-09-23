from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

import re
import torch
from string import punctuation

from transformations.gender_neutral_rewrite.myconstants import *

# direct replacement mapping
SIMPLE_REPLACE = EASY_PRONOUNS
SIMPLE_REPLACE.update(GENDERED_TERMS)

# load SpaCy's "en_core_web_sm" model
# English multi-task CNN trained on OntoNotes
# Assigns context-specific token vectors, POS tags, dependency parse and named entities
# https://spacy.io/models/en
from initialize import spacy_nlp
import spacy

self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")

# SpaCy: lowercase is for dependency parser, uppercase is for part-of-speech tagger
from spacy.symbols import (
    nsubj,
    nsubjpass,
    conj,
    poss,
    obj,
    iobj,
    pobj,
    dobj,
    VERB,
    AUX,
    NOUN,
)
from spacy.tokens import Token, Doc

# Load pre-trained language model and tokenizer
# https://huggingface.co/transformers/model_doc/gpt2.html
from transformers import GPT2LMHeadModel, GPT2TokenizerFast

if torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"

model_id = "gpt2"  # can also change to gpt-2 large if size is not an issue
model = GPT2LMHeadModel.from_pretrained(model_id).to(device)
tokenizer = GPT2TokenizerFast.from_pretrained(model_id)


def convert(sentence: str, max_outputs: int) -> str:
    """
    convert a sentence to gender-neutral form
    :param sentence: sentence meeting SNAPE criteria (meaning 1 entity and 1 gender)
    :return: sentence in gender-neutral form
    """
    if max_outputs != 1:
        ValueError(
            "Gender-neutral rewrite is meant to be applied to one sentence. Re-writing more than one sentence can "
            "lead to ambiguity. "
        )

    # check error case when input is a single word and the word is a non function pronoun
    if (
        sentence.strip(punctuation).strip().lower()
        in NON_FUNCTION_PRONOUNS.keys()
    ):
        raise ValueError(
            "Input is a pronoun with a one-to-many mapping. Insufficient context."
        )

    # use a LM to break ties for pronouns when there is a one-to-many mapping
    for word, choices in NON_FUNCTION_PRONOUNS.items():
        sentence = smart_pronoun_replace(sentence, word, choices)

    # replace pronouns and gendered terms that have a clear mapping
    # cannot directly modify "doc" object, so we will instead create a "replacement" attribute
    # in the end, we will create a new doc from original doc and any replacements
    Token.set_extension("simple_replace", getter=simple_replace, force=True)

    # Doc is a SpaCy container comprised of a sequence of Token objects
    doc = nlp(sentence)

    # create a dictionary mapping verbs in sentence from third-person singular to third-person plural
    verbs_auxiliaries = identify_verbs_and_auxiliaries(doc=doc)
    verbs_replacements = pluralize_verbs(verbs_auxiliaries)

    # create a new doc with replacements for pronouns, verbs, and gendered terms
    new_sentence = create_new_doc(doc, verbs_replacements)

    return new_sentence


def smart_pronoun_replace(sentence: str, token: str, choices: list) -> str:
    """
    use an LM to choose between multiple options for a replacement (e.g. her --> their / them)
    :param sentence: input sentence
    :param token: token with more than one choice for replacement
    :param choices: the options for replacement
    :return: the sentence after the LM has chosen the replacement option with lower perplexity
    """
    # generate all choices, then choose best option using LM (one with lowest perplexity)
    sentence_scores = dict()
    for choice in choices:
        new_sentence = regex_token_replace(sentence, token, replacement=choice)
        if sentence != new_sentence:
            new_score = score(sentence=new_sentence, stride=1)
            sentence_scores[new_sentence] = new_score

    if (
        not sentence_scores
    ):  # source pronoun not found in sentence, meaning there are no choices to choose from
        return sentence

    return min(
        sentence_scores, key=sentence_scores.get
    )  # return sentence with lowest score (perplexity)


def regex_token_replace(sentence: str, token: str, replacement: str) -> str:
    """
    replace all occurrences of a target token with its replacement
    :param sentence: input sentence to be modified
    :param token: target token to be replaced
    :param replacement: replacement word for the target token
    :return: sentence with the all occurrences of the target token substituted by its replacement
    """
    replace_map = [
        [token, replacement],
        [token.capitalize(), replacement.capitalize()],
        [token.upper(), replacement.upper()],
    ]

    for j in range(len(replace_map)):
        pattern = re.compile(
            r"\b{}\b".format(replace_map[j][0])
        )  # \b indicates a word boundary in regex
        sentence = re.sub(pattern, replace_map[j][1], sentence)

    return sentence


def score(sentence: str, stride: int = 1) -> float:
    """
    score the perplexity of a sentence
    :param sentence: input sentence
    :param stride: (optional) calculate perplexity for every {stride} tokens, can trade-off speed for accuracy
    :return: perplexity normalized by length of sentence (longer sentences won't have inherently have higher perplexity)
    """
    # Tony's note about the sliding window implementation / stride parameter (08.21.2020):

    # By default, the stride parameter is set to 1. This means that we find the average log probability of each token
    # after the first one (so n-1 probabilities), and then find the perplexity of the sentence. There is a
    # Huggingface implementation of GPT-2 that allows users to get the log probabilities of each token all at once,
    # which is significantly faster than calculating each probability one token at a time. I could be wrong,
    # but I believe the reason that we do not find the probability of the first token is that the Huggingface
    # implementation does not use a start-of-sentence token. This means that the first word becomes the first token
    # upon which the following words are conditioned.

    # For the purpose of rewriting / translating sentences, using a stride of 1 is preferred. However, due to the
    # fixed-length nature of certain models like GPT-2, if the input happens to be longer than the fixed length,
    # calculating perplexity can be a bit tricky. The default approach is to split the input into segments less than
    # or equal to the max fixed length, and then taking some kind of average of the perplexities. This is not a bad
    # approach, but the start of each segment loses a considerable amount of context. This can lead to a higher
    # perplexity than what is reflected in the text.

    # One solution is to use a sliding window (up to size max fixed length). This means that we can use more context
    # when calculating perplexity of tokens in situations where the input length is longer than our max fixed length.
    # On top of this, we can add a stride option to calculate the perplexity every {stride} tokens instead of
    # calculating perplexity for each token in the input. The sliding window with a larger stride is a nice
    # compromise, allowing computation to proceed much faster while still giving the model a large context to make
    # predictions at each step.

    encodings = tokenizer(sentence, return_tensors="pt")

    # can adjust stride based on size of input
    # if (1) input is longer (e.g. document) or (2) we wish to have faster computation, we can set longer stride
    # reference: https://huggingface.co/transformers/perplexity.html

    if (
        stride == 1
    ):  # if stride is 1, just return average log prob of each token (no need to copy and mask)
        input_ids = encodings.input_ids.to(device)
        with torch.no_grad():  # don't need gradients for evaluation
            outputs = model(input_ids, labels=input_ids)
            return float(torch.exp(outputs[0]))  # outputs[0] is avg log prob

    max_length = (
        model.config.n_positions
    )  # max length for gpt2-large and gpt is 1024
    num_tokens = encodings.input_ids.size(
        1
    )  # usually punctuation will count as separate tokens

    # calculate neg log prob for each token given context of previous tokens in the sentence
    # if stride=1, context will be all previous tokens in sentence (assuming # of tokens < max_length)
    log_probabilities = list()
    for i in range(1, num_tokens, stride):
        begin_loc = max(i + stride - max_length, 0)

        # model is trained without a token indicating beginning of sentence, so we start calculation at second token
        # this also means model cannot calculate perplexity for a single token (have added error checking for this case)
        end_loc = i + stride

        input_ids = encodings.input_ids[:, begin_loc:end_loc].to(device)
        target_ids = input_ids.clone()
        target_ids[
            :, :-stride
        ] = (
            -100
        )  # mask prior tokens (the context) since we only care about current token

        with torch.no_grad():  # don't need gradients for evaluation
            outputs = model(input_ids, labels=target_ids)
            log_prob = outputs[0] * stride

        log_probabilities.append(log_prob)

    # formula for perplexity
    # dividing by (num_tokens - 1) because model does not calculate log prob for first token
    perplexity = torch.exp(
        torch.stack(log_probabilities).sum() / (num_tokens - 1)
    )

    return float(perplexity)


def simple_replace(token: Token):
    """
    mainly deals with straightforward cases of pronoun / gendered word replacement using a lookup
    also resolves "her" --> "their" / "them"
    :param token: SpaCy token
    :return: the token's text replacement (if it exists) as a string.
    """
    text = token.text

    # use dependency parser to resolve "her" --> "their" / "them"
    # if "her" is a possessive pronoun, then its replacement should be "their"
    # if "her" is an object, then its replacement should be "them"
    if text.lower() == "her":
        is_obj = (
            token.dep == obj
            or token.dep == iobj
            or token.dep == pobj
            or token.dep == dobj
            or token.dep_ == "dative"
        )
        if token.dep == poss:
            return capitalization_helper(original=text, replacement="their")
        elif is_obj:
            return capitalization_helper(original=text, replacement="them")
        else:
            return None

    # their vs theirs: https://ell.stackexchange.com/questions/18604/how-to-use-their-and-theirs
    if text.lower() == "his":
        implied_head = token.head.pos != NOUN
        if implied_head:
            return capitalization_helper(original=text, replacement="theirs")
        else:
            return capitalization_helper(original=text, replacement="their")

    # use a lookup for direct mappings
    # e.g. he --> they, she --> they, policeman --> police officer
    elif text.lower() in SIMPLE_REPLACE.keys():
        replace = SIMPLE_REPLACE[text.lower()]
        return capitalization_helper(original=text, replacement=replace)

    return None


def capitalization_helper(original: str, replacement: str) -> str:
    """
    helper function to return appropriate capitalization
    :param original: original word from the sentence
    :param replacement: replacement for the given word
    :return: replacement word matching the capitalization of the original word
    """
    # check for capitalization
    if original.istitle():
        return replacement.capitalize()
    elif original.isupper():
        return replacement.upper()

    # otherwise, return the default replacement
    return replacement


def identify_verbs_and_auxiliaries(doc: Doc) -> dict:
    """
    identify the root verbs and their corresponding auxiliaries with 'she' or 'he' as their subject
    :param doc: input Doc object
    :return: dictionary with verbs (SpaCy Token) as keys, auxiliaries as values (SpaCy Token)
    """
    # no need to include uppercase pronouns bc searching for potential_subject checks lower-cased version of each token
    SUBJECT_PRONOUNS = ["she", "he"]

    # identify all verbs
    verbs = set()
    # this deals with repeating verbs, e.g. "He sings and sings."
    # verb Token with same text will have different position (makes them unique)
    for possible_subject in doc:
        is_subject = (
            (
                possible_subject.dep == nsubj
                or possible_subject.dep == nsubjpass
            )
            and  # current token is a subject
            # head of current token is a verb
            (
                possible_subject.head.pos == VERB
                or possible_subject.head.pos == AUX
            )
            and possible_subject.text.lower()
            in SUBJECT_PRONOUNS  # current token is either she / he
        )
        if is_subject:
            verbs.add(possible_subject.head)

    # identify all conjuncts and add them to set of verbs
    # e.g. he dances and prances --> prances would be a conjunct
    for possible_conjunct in doc:
        is_conjunct = (
            possible_conjunct.dep == conj
            and possible_conjunct.head  # current token is a conjunct
            in verbs  # the subject of that verb is she / he
        )
        if is_conjunct:
            verbs.add(possible_conjunct)

    verbs_auxiliaries = dict()
    for verb in verbs:
        verbs_auxiliaries[verb] = list()
    for possible_aux in doc:
        is_auxiliary = (
            possible_aux.pos == AUX
            and possible_aux.head  # current token is an auxiliary verb
            in verbs  # the subject of that verb is she / he
        )
        if is_auxiliary:
            verb = possible_aux.head
            verbs_auxiliaries[verb].append(possible_aux)

    return verbs_auxiliaries


def pluralize_verbs(verbs_auxiliaries: dict) -> dict:
    """
    map each verb and auxiliary to its plural form
    :param verbs_auxiliaries: dictionary with verbs (SpaCy Token) as keys, auxiliaries as values (SpaCy Token)
    :return: dictionary with verbs and auxiliaries (SpaCy Token) as keys, plural form as values (str or None)
    """
    verbs_replacements = dict()

    for verb, auxiliaries in verbs_auxiliaries.items():
        # verb has no auxiliaries
        if not auxiliaries:
            verbs_replacements[verb] = pluralize_single_verb(verb)

        # there are auxiliary verbs
        else:
            verbs_replacements[
                verb
            ] = None  # do not need to pluralize root verb if there are auxiliaries

            # use a lookup to find replacements for auxiliaries
            for auxiliary in auxiliaries:
                text = auxiliary.text
                if text.lower() in IRREGULAR_VERBS.keys():
                    replacement = IRREGULAR_VERBS[text.lower()]
                    verbs_replacements[auxiliary] = capitalization_helper(
                        original=text, replacement=replacement
                    )
                else:
                    verbs_replacements[auxiliary] = None

    return verbs_replacements


def pluralize_single_verb(verb: Token):
    """
    pluralize a single verb
    :param verb: verb as a SpaCy token
    :return: the plural form of the verb as a str, or None if verb doesn't lend itself to pluralization
    """
    verb_text = verb.text

    # check verb tense (expect to be either past simple or present simple)
    verb_tense = verb.morph.get("Tense")[0]  # list with 1 item

    if verb_tense == "Past":
        # was is an irregular past tense verb from third-person singular to third-person plural
        if verb_text.lower() == "was":
            return capitalization_helper(verb_text, "were")

        # other past-tense verbs remain the same
        else:
            return None

    # oftentimes, if there are 2+ verbs in a sentence, each verb after the first (the conjuncts) will be misclassified
    # the POS of these other verbs are usually misclassified as NOUN
    # e.g. He dances and prances and sings. --> "prances" and "sings" are conjuncts marked as NOUN (should be VERB)
    # checking if verb ends with "s" is a band-aid fix
    elif verb_tense == "Pres" or verb.text.endswith("s"):
        return capitalization_helper(
            original=verb_text.lower(),
            replacement=pluralize_present_simple(verb_text),
        )

    return None


def pluralize_present_simple(lowercase_verb: str):
    """
    pluralize a third-person singular verb in the present simple tense
    :param lowercase_verb: original verb (lower-cased)
    :return: 3rd-person plural verb in the present simple tense
    """
    for singular, plural in IRREGULAR_VERBS.items():
        if lowercase_verb == singular:
            return plural

    if lowercase_verb.endswith("ies"):
        return lowercase_verb[:-3] + "y"

    # -es rule: https://howtospell.co.uk/adding-es-plural-rule
    for suffix in VERB_ES_SUFFIXES:
        if lowercase_verb.endswith(suffix):
            return lowercase_verb[:-2]

    if lowercase_verb.endswith("s"):
        return lowercase_verb[:-1]

    return None


def create_new_doc(doc: Doc, verbs_replacements: dict):
    """
    create a new SpaCy doc using the original doc and a mapping of verbs to their replacements
    :param doc: original doc with simple_replace extension (from simple_replace function)
    :param verbs_replacements: dictionary mapping verbs and auxiliaries to their replacements
    :return: the gender-neutral sentence as a str
    """
    token_texts = []
    for token in doc:
        replace_verb = (
            token in verbs_replacements.keys() and verbs_replacements[token]
        )

        if token._.simple_replace:
            token_texts.append(token._.simple_replace)

        elif replace_verb:
            token_texts.append(verbs_replacements[token])

        else:
            token_texts.append(token.text)
        if token.whitespace_:  # filter out empty strings
            token_texts.append(token.whitespace_)

    new_sentence = "".join(token_texts)
    return new_sentence


class GenderNeutralRewrite(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["en"]

    def __init__(self, seed=0, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)

    def generate(self, sentence: str) -> List[str]:
        gender_neutral_sentence = convert(
            sentence=sentence, max_outputs=self.max_outputs
        )
        return [gender_neutral_sentence]
