## keywords filter

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
Which returns `True`, as the number of sentences tagged as "target" is less than the number of sentences tagged as "test".
You can also check the exact number by calling the `count_groups()` static method on the instance of the class and providing it with the extracted tags with the `flag_sentences() static method:`
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

## What are the limitations of this filter?
This filter accepts unigram arrays, the n-gramms won't give the desired output.