import json
import os
import random
import re

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


class CountryStateAbbreviation(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
    ]
    languages = ["en"]

    def __init__(self, seed=0, country=True, state=True, country_filter='USA', abbr=True, exp=True):
        super().__init__(seed)
        self.country = country
        self.state = state
        self.country_filter = country_filter
        self.abbr = abbr
        self.exp = exp

    def generate(self, sentence: str):
        perturbed_texts = self.country_state_abbreviation(text=sentence)
        return perturbed_texts

    def build_mapping(self):
        abbr_file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "country_state_abbreviation.json",
        )
        abbr_json = json.load(open(abbr_file_path, "r"))
        country_abbr = {}
        country_exp = {}
        state_abbr = {}
        state_exp = {}
        for country in abbr_json:
            country_abbr[country['name']] = country['abbr']
            country_exp[country['abbr']] = country['name']

        if self.country_filter:
            country = next((x for x in abbr_json if x['abbr'] == self.country_filter), None)
            if country:
                for state in country['states']:
                    state_abbr[state['name']] = state['abbr']
                    state_exp[state['abbr']] = state['name']
        else:
            for country in abbr_json:
                states = country['states']
                for state in states:
                    if state['abbr'] in state_exp:
                        if type(state_exp[state['abbr']]) is list:
                            state_exp[state['abbr']].append(state['name'])
                        else:
                            state_exp[state['abbr']] = [state_exp[state['abbr']]]
                    else:
                        state_exp[state['abbr']] = state['name']
                    if state['name'] in state_abbr:
                        if type(state_abbr[state['name']]) is list:
                            state_abbr[state['name']].append(state['abbr'])
                        else:
                            state_abbr[state['name']] = [state_abbr[state['name']]]
                    else:
                        state_abbr[state['name']] = state['abbr']

        country_mapping = {}
        state_mapping = {}
        if self.country:
            if self.abbr:
                country_mapping = {**country_mapping, **country_abbr}
            if self.exp:
                country_mapping = {**country_mapping, **country_exp}
        if self.state:
            if self.abbr:
                state_mapping = {**state_mapping, **state_abbr}
            if self.exp:
                state_mapping = {**state_mapping, **state_exp}

        return country_mapping, state_mapping

    def country_state_abbreviation(self, text):
        # Build mapping dictionary of abbreviation -> full name and full name -> abbreviation
        # country_mapping contains mapping between country's full name and abbreviation
        # country_mapping = {
        #   ...,
        #   "United States": "USA",
        #   ...,
        #   "USA": "United States",
        #   ...
        # }
        # state_mapping contains mapping between state's full name and abbreviation
        # state_mapping = {
        #   ...,
        #   "Pennsylvania": "PA",
        #   ...,
        #   "PA": "Pennsylvania",
        #   ...
        # }
        country_mapping, state_mapping = self.build_mapping()

        # Build regex pattern for country abbreviation/full name by joining country_mapping keys
        # eg. country_pattern = '...|United States|...|USA|...'
        country_pattern = '|'.join(country_mapping.keys())
        # Adding backslash before '(' and ')' in country name as the escape character (eg. Virgin Islands (US))
        country_pattern = country_pattern.replace('(', '\(')
        country_pattern = country_pattern.replace(')', '\)')
        country_regex = re.compile("(^|\s+)(" + country_pattern + ")(\s+|\?|!|$|\.|,)")
        perturbed_text = country_regex.sub(
            lambda y: y[1] + country_mapping[y[2]] + y[3],
            text,
        )

        # Build regex pattern for state abbreviation/full name by joining state_mapping keys
        # eg. state_pattern = '...|Pennsylvania|...|PA|...'
        state_pattern = '|'.join(state_mapping.keys())
        # Adding backslash before '(' and ')' in state name as the escape character
        state_pattern = state_pattern.replace('(', '\(')
        state_pattern = state_pattern.replace(')', '\)')
        state_regex = re.compile("(^|\s+)(" + state_pattern + ")(\s+|\?|!|$|\.|,)")
        perturbed_text = state_regex.sub(
            lambda y: y[1] + self.dict_value_helper(state_mapping, y[2]) + y[3],
            perturbed_text,
        )
        return [perturbed_text]

    def dict_value_helper(self, d, key):
        if type(d[key]) is list:
            random.seed(self.seed)
            return random.choice(d[key])
        else:
            return d[key]
