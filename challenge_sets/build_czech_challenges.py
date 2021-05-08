from datasets import load_dataset
from collections import namedtuple, defaultdict, Counter
import json


##############################################################################
# Functions to build challenge sets.

def challenge_acts(restaurants):
    "Compare different acts."
    challenge_set = defaultdict(list)
    for entry in restaurants['test']:
        info = extract_info(entry)
        challenge_set[info['act']].append(entry['gem_id'])
    return challenge_set


def challenge_input_size(restaurants):
    "Compare items with different input sizes."
    challenge_set = defaultdict(list)
    for entry in restaurants['test']:
        info = extract_info(entry)
        preds = tuple(sorted(info['lexicalised'].keys()))
        challenge_set[f"input_length_{len(preds)}"].append(entry['gem_id'])
    return challenge_set


def compile_challenges(webnlg):
    "Compile all challenge sets."
    return {"challenge_acts": challenge_acts(restaurants),
            "challenge_input_size": challenge_input_size(restaurants)}

##############################################################################
# Functions to parse the data.

def get_components(act):
    "Get components from a dialog act."
    components = dict()
    for item in act[:-1].split('(')[1].split(','):
        if item:
            if '=' in item:
                key, value = item.split('=')
                components[key] = value
            else:
                components['item'] = None
    return components


def extract_info(entry):
    "Extract information from an entry."
    input_data = dict(act = entry['dialog_act'].split('(')[0])
    input_data['lexicalised'] = get_components(entry['dialog_act'])
    input_data['delexicalised'] = get_components(entry['dialog_act_delexicalized'])
    return input_data

##############################################################################
# Main code.

restaurants = load_dataset("gem", "cs_restaurants")
challenges = compile_challenges(restaurants)
with open("cs_restaurants_challenges.json",'w') as f:
    json.dump(challenges, f, indent=4)
