from datasets import load_dataset
from collections import namedtuple, defaultdict, Counter
import json


##############################################################################
# General-purpose functions.

Triple = namedtuple('Triple', field_names=['arg1', 'predicate', 'arg2'])

def get_triple(triple_text):
    "Get Triple from textual representation of a triple."
    return Triple(*triple_text.split(' | '))


def get_triples(entry):
    "Get all triples for an entry."
    return [get_triple(triple_text) for triple_text in entry['input']]


##############################################################################
# Functions to build challenge sets.

def challenge_combinations(webnlg):
    "Compare seen and unseen combinations of predicates."
    challenge_set = defaultdict(list)
    train_combos = set()
    for entry in webnlg['train']:
        triples = get_triples(entry)
        if len(triples) > 1:
            current_tuple = tuple([triple.predicate for triple in triples])
            train_combos.add(current_tuple)
    for entry in webnlg['test']:
        triples = get_triples(entry)
        if len(triples) > 1:
            current_tuple = tuple([triple.predicate for triple in triples])
            if current_tuple in train_combos:
                challenge_set['seen'].append(entry['gem_id'])
            else:
                challenge_set['unseen'].append(entry['gem_id'])
    return challenge_set


def challenge_input_size(webnlg):
    "Compare items with different input sizes."
    challenge_set = defaultdict(list)
    for entry in webnlg['test']:
        challenge_set[f"input_length_{len(entry['input'])}"].append(entry['gem_id'])
    return challenge_set


def challenge_single_predicates(webnlg):
    "Compare seen and unseen single predicates."
    challenge_set = defaultdict(list)
    train_preds = set()
    for entry in webnlg['train']:
        triples = get_triples(entry)
        train_preds.update([triple.predicate for triple in triples])
    for entry in webnlg['test']:
        triples = get_triples(entry)
        if len(triples) == 1:
            if triples[0].predicate in train_preds:
                challenge_set['seen'].append(entry['gem_id'])
            else:
                challenge_set['unseen'].append(entry['gem_id'])
    return challenge_set


def challenge_args(webnlg):
    "Compare inputs based on whether all arg1s and arg2s were seen or not."
    challenge_set = defaultdict(list)
    train_arg1s = {triple.arg1 for entry in webnlg['train'] 
                              for triple in get_triples(entry)}
    train_arg2s = {triple.arg2 for entry in webnlg['train'] 
                              for triple in get_triples(entry)}
    for entry in webnlg['test']:
        triples = get_triples(entry)
        arg1s = {triple.arg1 for triple in triples}
        arg2s = {triple.arg2 for triple in triples}
        unseen_arg1 = arg1s - train_arg1s
        unseen_arg2 = arg2s - train_arg2s
        if unseen_arg1 and unseen_arg2:
            challenge_set['both_unseen'].append(entry['gem_id'])
        elif unseen_arg1:
            challenge_set['arg1_unseen'].append(entry['gem_id'])
        elif unseen_arg2:
            challenge_set['arg2_unseen'].append(entry['gem_id'])    
        else:
            challenge_set['both_seen'].append(entry['gem_id'])
    return challenge_set


def compile_challenges(webnlg):
    "Compile all challenge sets."
    return {"challenge_input_size": challenge_input_size(webnlg),
            "challenge_single_predicates": challenge_single_predicates(webnlg),
            "challenge_combinations": challenge_combinations(webnlg),
            "challenge_args": challenge_args(webnlg)}


webnlg = load_dataset("gem", "web_nlg_en")
challenges = compile_challenges(webnlg)
with open("webnlg_en_challenge_sets.json",'w') as f:
    json.dump(challenges, f, indent=4)

    
webnlg = load_dataset("gem", "web_nlg_ru")
challenges = compile_challenges(webnlg)
with open("webnlg_ru_challenge_sets.json",'w') as f:
    json.dump(challenges, f, indent=4)