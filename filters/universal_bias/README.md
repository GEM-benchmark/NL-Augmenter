## Universal bias filter

## What type of a filter is this?

This filter is language and topic agnostic, allowing the user to specify the minority and the majority parameters at the object initialisation step, which filter the text corpus.
Since the filtering parameters are user defined, it may be applied in any language.
The minority parameter is a potentially underrepresented group, defined with its own set of keywords; the majority parameter is a set of keywords, representing the dominating group.
The filter returns "True" if the minority group is indeed underrepresented, "False" otherwise.

Author: Anna Shvets
Affiliation: 
FabLab by Inetum, 
157 Boulevard MacDonald
75019 Paris - France 

## Why is measuring performance on this split important?
This filter can be used to measure the underrepresentation of a specific group regarding gender, race, religion and other criteria.
The filter aims to prevent the propagation of the historial biases usually present in large text datasets.
Finally, it additionally allows to retrieve the groups in question, which might be useful for further manipulation of the dataset.

## Example of use
```
minority = ["she", "her", "hers"]
majority = ["he", "him", "his"]

sentences = [ "He is going to make a cake.",
              "She is going to program",
              "Nobody likes washing dishes",
              "He agreed to help me" ]

f = UniversalBiasFilter(minority, majority)

f.filter(sentences)
```
Which returns `True`, as the number of sentences flagged as "minority" is less than the number of sentences tagged as "majority".
You can check the exact number by calling the `count_groups()` static method on the instance of the class and providing it with the extracted flags with the `flag_sentences()` static method:
```
flagged_sentences = f.flag_sentences(sentences, minority, majority)
minority, majority, neutral = f.count_groups(flagged_sentences)

print("minority tagged sentences:", minority)
print("majority tagged sentences:", majority)
print("Neutral tagged sentences:", neutral)
```
Which outputs:
```
minority tagged sentences: 1
majority tagged sentences: 2
Neutral tagged sentences: 1
```
You can also retrieve the arrays of sentences from each group, by calling the `sort_groups()` method on the instance of th class, providing it with flags, extracted by `flag_sentences()` method:
```
flagged_sentences = f.flag_sentences(sentences, minority, majority)
minority_group, majority_group, neutral_group = f.sort_groups(flagged_sentences)
print("This is a minority group:", minority_group)
print("This is a majority group:", majority_group)
print("This is a neutral group:", neutral_group)
```
Which outputs:
```
This is a minority group: ['She is going to program']
This is a majority group: ['He is going to make a cake.', 'He agreed to help me']
This is a neutral group: ['Nobody likes washing dishes']
```

## What are the limitations of this filter?
This filter accepts unigram arrays, the n-gramms won't give the desired output, since the intersection with keywords is calculated after the sentence being passed throug split() function, wich returs an array of unigrams.
