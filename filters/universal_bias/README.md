## Universal bias filter

## What type of a filter is this?

This filter is language and topic agnostic, allowing the user to specify the target and the test conditions at the object initialisation step, which filter the text corpus.
Since the testing condition is user defined, it may be applied in any language.
The target is a potentially underrepresented group, defined with its own set of keywords; the test is the set of keywords, representing the dominating group.
The filter returns "True" if the target group is indeed underrepresented, "False" otherwise.

Author: Anna Shvets
Affiliation: FabLab by Inetum in Paris

## Why is measuring performance on this split important?
This filter can be used to measure the underrepresentation of a specific group regarding gender, racial, religion and other criteria.
The filter aims to prevent the propagation of the historial biases usually present in large text datasets.
Finally, it additionally allows to retrieve the corresponding groups, which might be useful for further manipulation of the dataset.

## Example of use
```
target = ["she", "her", "hers"]
test = ["he", "him", "his"]

sentences = [ "He is going to make a cake.",
              "She is going to program",
              "Nobody likes washing dishes",
              "He agreed to help me" ]

f = UniversalBiasFilter(target, test)

f.filter(sentences)
```
Which returns `True`, as the number of sentences flagged as "target" is less than the number of sentences tagged as "test".
You can check the exact number by calling the `count_groups()` static method on the instance of the class and providing it with the extracted tags with the `flag_sentences()` static method:
```
flagged_sentences = f.flag_sentences(sentences, target, test)
target, test, neutral = f.count_groups(flagged_sentences)

print("Target tagged sentences:", target)
print("Test tagged sentences:", test)
print("Neutral tagged sentences:", neutral)
```
Which outputs:
```
Target tagged sentences: 1
Test tagged sentences: 2
Neutral tagged sentences: 1
```
You can also retrieve the arrays of sentences from each group, by calling the `sort_groups()` method on the instance of th class, providing it with flags, extracted by `flag_sentences()` method:
```
flagged_sentences = f.flag_sentences(sentences, target, test)
target_group, test_group, neutral_group = f.sort_groups(flagged_sentences)
print("This is a target group:", target_group)
print("This is a test group:", test_group)
print("This is a neutral group:", neutral_group)
```
Which outputs:
```
This is a target group: ['She is going to program']
This is a test group: ['He is going to make a cake.', 'He agreed to help me']
This is a neutral group: ['Nobody likes washing dishes']
```

## What are the limitations of this filter?
This filter accepts unigram arrays, the n-gramms won't give the desired output.
