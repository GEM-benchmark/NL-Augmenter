## Group inequity filter

## What type of a filter is this?

This is a bilingual filter (for English and French languages), which filters helps to discover potential group inequity issues in the text corpus.
This is a topic agnostic filter which accepts user-defined parameters, consisting of keywords inherent to minor group (which potentially might suffer from the discrimination), 
major group, minor factor and major factor.
The filter first flags the sentences to be inherent to minor and major groups, with `flag_sentences()` and `sort_groups()` methods, 
then, the the sentences from each of the groups are passed through the `find_intersection()` method to define the intersection with both factors.
The final boolean value is calculated in regards of the values retrived from `count_itersections()` method.

The main idea lies in a balance between groups in regards of the factors: let's suppose, that we have three sentences in a dataset and the word "nurse" is applied in two sentences, containing the pronon "she", on the other hand, the word "doctor" is applied in one sentence, containing the pronon "he". We may suggest that the gender discrimination in regards of the profession stereotypes takes place. 
The minority group array, therefore, will contain the word "she" and the minority factor array will contain the word "nurse", while the majority group array will contain "he" and the major factor array - "doctor".
In a described situation, the filter will return `True`, which means, that the minority group is indeed potentially discriminated.
However, if in one of the sentences containing the word "nurse", the pronoun will be replaced by "he" - the filter will return `False`, as both genders represent the profession "nurse", therefore there is no group inequity in this regard.


Author: Anna Shvets
Company:
Fablab by Inetum in Paris
157 Boulevard MacDonald
75019 Paris
France


## Why is measuring performance on this split important?
This filter aims to help with discovering potential inequity issues in regards of on group, compared to another. 
This might help fighting historical gender/ethnic/regilious prejudices in existing and newly created NLP datasets.

## Related Work
The problematics of the gender fairness is an active domain of research in NLP, however the existing methods of the bias measurement, such as PCA [[1]](https://arxiv.org/abs/1607.06520) or WEAT [[2]](https://arxiv.org/abs/1608.07187), may suffer from unclearness in the lexical seeds selection, pointed in a recent ACL 2021 paper [[3]](https://www.aclanthology.org/2021.acl-long.148), the intrinsic measurements showed no correlation with extrinsic methods results, as showed a recent research [[4]](https://www.aclanthology.org/2021.acl-long.150). On the other hand, the gender bias datasets (Winobias, Winogender, StereoSet, CrowS-Pairs) can present the unconsistencies, pointed by another ACL paper [[5]](https://aclanthology.org/2021.acl-long.81) and might be far from  optimal in terms if bias measurement. 
The beneficial impact of the current extrinsic filter is its complete transparency and extensibility, which offers the user a great amont of control over the bias measurement parameters.

## Examples of use
```
minority_group = ["she", "her", "hers"]
majority_group = ["he", "him", "his"]

minority_factor = ["cake"]
majority_factor = ["program"]

sentences = [ "He is going to make a cake.",
              "She is going to make a cake.",              
              "She is going to make a computer program",              
              ]

f = DiscriminationFilter("en", minority_group, majority_group, minority_factor, majority_factor)
f.filter(sentences)
```

The above statement returns False, as the intersection of the minority group with the minority factor is the same as with the majority factor.
However, in the following example, the filter indicates a potential inequity issue towards minority group, since the number of intersections with the minority factor is bigger, than with the majority factor:
```
minority_group = ["she", "her", "hers"]
majority_group = ["he", "him", "his"]

minority_factor = ["cake"]
majority_factor = ["program"]

sentences = [ "She is going to make a cake.",
              "She makes good cakes",             
              "She is going to make a computer program",
              "He is going to make a computer program",
              ]

f = DiscriminationFilter("en", minority_group, majority_group, minority_factor, majority_factor)
f.filter(sentences)
```

You can retrieve the arrays of sentences from each group, by calling the `sort_groups()` method on the instance of the class, providing it with flags, extracted by `flag_sentences()` method:

```
minority_group = ["she", "her", "hers"]
majority_group = ["he", "him", "his"]

minority_factor = ["cake"]
majority_factor = ["program"]

sentences = [ "He is going to make a cake.",
              "She is going to make a cake.",              
              "She is going to make a computer program",
              "As she is a good programmer, he makes her a cake",
              "Nobody likes making cakes!"                          
              ]

f = DiscriminationFilter("en", minority_group, majority_group, minority_factor, majority_factor)

flagged_corpus = f.flag_sentences(sentences, minority_group, majority_group)
minority_group, majority_group, union_group, neutral_group = f.sort_groups(flagged_corpus)

print("Sentences from the minority group:", minority_group)
print("Sentences from the majority group:", majority_group)
print("Sentences from the union group:", union_group)
print("Sentences from the neutral group:", neutral_group)

```

which outputs:
```
Sentences from the minority group: ['She is going to make a cake.', 'She is going to make a computer program', 'As she is a good programmer, he makes her a cake']
Sentences from the majority group: ['He is going to make a cake.', 'As she is a good programmer, he makes her a cake']
Sentences from the union group: ['As she is a good programmer, he makes her a cake']
Sentences from the neutral group: ['Nobody likes making cakes!']
```

For the statistics of the potential discrimination, use the `count_intersections()` method:

```
language = "en"
minority_group = ["she", "her", "hers"]
majority_group = ["he", "him", "his"]

minority_factor = ["cake"]
majority_factor = ["program"]

sentences = [ "He is going to make a cake.",
              "She is going to make a computer program",            
              "Nobody likes making cakes!"                          
              ]
f = DiscriminationFilter(language , minority_group, majority_group, minority_factor, majority_factor)

# Retrieve the flags for each of the sentences
flagged_corpus = f.flag_sentences(sentences, minority_group, majority_group)

# Use the flagged objects to get the groups
minority_group, majority_group, union_group, neutral_group = f.sort_groups(flagged_corpus)

# Retrive the flags of intersection for the miority and majority groups
doubble_flagged_corpus = f.find_intersection(language, minority_group, majority_group, minority_factor, majority_factor)

# Count the number of intersections with the minority and majority factors
minority_group_intersection_count, majority_group_intersection_count = f.count_intersections(doubble_flagged_corpus)
print("The intersections of the minority group with the minority factor:", minority_group_intersection_count)
print("The intersections of the majority group with the minority factor:", majority_group_intersection_count)
```
which outputs:
```
The intersections of the minority group with the minority factor: 0
The intersections of the majority group with the minority factor: 1
```

You are free to change the language at the class initialisation step:
```
minority_group = ["elle", "sienne"]
majority_group = ["il", "sien"]

minority_factor = ["gâteau"]
majority_factor = ["logiciel"]

sentences = ["Il va faire un gâteau.",
             "Elle va faire un gâteau.",
             "Personne va faire un logiciel"            
              ]

f = DiscriminationFilter("fr", minority_group, majority_group, minority_factor, majority_factor)
f.filter(sentences)
```

If you want to use a filter with French texts, you might want to install the spacy French model first, as spacy dependecy is used for lemmatization on the sentences before comparing them to the factor arrays:
```
python -m spacy download fr_core_news_sm
```


## What are the limitations of this filter?
The filter does not take into calculation condition the the sentences from the `union_group`, which where flagged as inherent to both - minor and major groups at the same time. 
You might want to expract the content of this group using "sort_groups()" method ad check it manually or using other methods.

## References
_[1]_
```bibtex
@misc{bolukbasi2016man,
      title={Man is to Computer Programmer as Woman is to Homemaker? Debiasing Word Embeddings}, 
      author={Tolga Bolukbasi and Kai-Wei Chang and James Zou and Venkatesh Saligrama and Adam Kalai},
      year={2016},
      eprint={1607.06520},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```
_[2]_
```bibtex
@article{Caliskan_2017,
   title={Semantics derived automatically from language corpora contain human-like biases},
   volume={356},
   ISSN={1095-9203},
   url={http://dx.doi.org/10.1126/science.aal4230},
   DOI={10.1126/science.aal4230},
   number={6334},
   journal={Science},
   publisher={American Association for the Advancement of Science (AAAS)},
   author={Caliskan, Aylin and Bryson, Joanna J. and Narayanan, Arvind},
   year={2017},
   month={Apr},
   pages={183–186}
}
```
_[3]_
```bibtex
@inproceedings{antoniak-mimno-2021-bad,
    title = "Bad Seeds: Evaluating Lexical Methods for Bias Measurement",
    author = "Antoniak, Maria  and
      Mimno, David",
    booktitle = "Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume 1: Long Papers)",
    month = aug,
    year = "2021",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2021.acl-long.148",
    doi = "10.18653/v1/2021.acl-long.148",
    pages = "1889--1904",    
}
```
_[4]_
```bibtex
@inproceedings{goldfarb-tarrant-etal-2021-intrinsic,
    title = "Intrinsic Bias Metrics Do Not Correlate with Application Bias",
    author = "Goldfarb-Tarrant, Seraphina  and
      Marchant, Rebecca  and
      Mu{\~n}oz S{\'a}nchez, Ricardo  and
      Pandya, Mugdha  and
      Lopez, Adam",
    booktitle = "Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume 1: Long Papers)",
    month = aug,
    year = "2021",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2021.acl-long.150",
    doi = "10.18653/v1/2021.acl-long.150",
    pages = "1926--1940",   
}
```
_[5]_
```bibtex
@inproceedings{blodgett-etal-2021-stereotyping,
    title = "Stereotyping {N}orwegian Salmon: An Inventory of Pitfalls in Fairness Benchmark Datasets",
    author = "Blodgett, Su Lin  and
      Lopez, Gilsinia  and
      Olteanu, Alexandra  and
      Sim, Robert  and
      Wallach, Hanna",
    booktitle = "Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume 1: Long Papers)",
    month = aug,
    year = "2021",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2021.acl-long.81",
    doi = "10.18653/v1/2021.acl-long.81",
    pages = "1004--1015", 
}
```
