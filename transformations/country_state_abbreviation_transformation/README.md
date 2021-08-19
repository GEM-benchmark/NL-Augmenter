# Country/State Abbreviation 🦎  + ⌨️ → 🐍
This perturbation adds Country/State name/abbreviation with flexiable options: Pennsylvania -> PA or PA -> Pennsylvania

Author name: Yiwen Shi
Author email: yiwen.shi@drexel.edu
Author Affiliation: Drexel University

Author name: Hualou Liang
Author email: hualou.liang@drexel.edu
Author Affiliation: Drexel University

## What type of a transformation is this?
This transformation acts as a perturbation and makes lexical substitutions. 

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document that contains worldwide country and state name or abbreviation as input like text classification, text generation, etc. It could be widely used in news datasets (eg. CNN/DailyMail)

This transformation provides flexible options for Country/State abbreviation and full name transformation. 

| Parameter  | Type  | Description  | Default |
|---|---|---|---|
| country | Boolean  | Enable/disable transformation of country abbreviation/full name   | True | 
| state  | Boolean  |  Enable/disable transformation of state abbreviation/full name   | True | 
| country_filter  | String  | Only apply transformation of state abbreviation/full name of a specific country. If set it as '', it will use all of the states. | 'USA'  | 
| abbr  |  Boolean | Enable/disable full name -> abbreviation  |  True  | 
| exp  | Boolean  | Enable/disable abbreviation -> full name | True  |  

## Data provenance
This transformation uses country/state name and abbreviation as a lite version of Countries States Cities Database (https://github.com/dr5hn/countries-states-cities-database). We use iso3 country as the abbreviation and state_code of states as the abbreviation.

The Countries States Cities Database is licensed under the Open Database License, see https://github.com/dr5hn/countries-states-cities-database/blob/master/LICENSE.

## What are the limitations of this transformation?
The transformation's outputs are simple to be used for data augmentation. Unlike a paraphraser, it is not capable of generating linguistically diverse text.

When full name/abbreviation transformations are enabled to both country and state, the former suppresses the latter if a text belongs to both a country and a state name. For example, ‘Mexico’ will be treated as a country (with abbreviation as ‘MEX’), resulting in the transformation of ‘New Mexico’ to ‘New MEX’ instead of ‘NM’.