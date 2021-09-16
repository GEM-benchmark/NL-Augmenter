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
This filter can be used to measure the underrepresentation of a specific group regarding gender, ethnicity, religion and other criteria.
The filter aims to prevent the propagation of the historial biases usually present in large text datasets.
Finally, it additionally allows to retrieve the groups in question, which might be useful for further manipulation of the dataset.

## Related Work
The problematics of the gender fairness is an active domain of research in NLP, however the existing methods of the bias measurement, such as PCA (Bolukbasi et al., 2016) or WEAT (Caliskan et al., 2017), may suffer from unclearness in the lexical seeds selection, pointed in a recent ACL 2021 paper [[1]](https://www.aclanthology.org/2021.acl-long.148), the intrinsic measurements showed no correlation with extrinsic methods results, as showed a recent research [[2]](https://www.aclanthology.org/2021.acl-long.150). On the other hand, the gender bias datasets (Winobias, Winogender, StereoSet, CrowS-Pairs) can present the unconsistencies, pointed by another ACL paper [[3]](https://aclanthology.org/2021.acl-long.81.pdf) and might be far from  optimal in terms if bias measurement. 
The beneficial impact of the current extrinsic filter is its complete transparency and extensibility, which offers the user a great amont of control over the bias measurement parameters.


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
Output:
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
Output:
```
This is a minority group: ['She is going to program']
This is a majority group: ['He is going to make a cake.', 'He agreed to help me']
This is a neutral group: ['Nobody likes washing dishes']
```

## What are the limitations of this filter?
This filter accepts unigram arrays, the n-gramms won't give the desired output, since the intersection with keywords is calculated after the sentence being passed through split() function, wich returs an array of unigrams.
