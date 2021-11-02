## Universal bias filter

## What type of a filter is this?

This filter is currently contains lexical seeds for 10 categories () in English, however it can be extended to any language or topic by simple addition of desired entries to `lexicals.json` 
file in current directoryalong with the text corpus in corresponding language.
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
The problematics of the gender fairness is an active domain of research in NLP, however the existing methods of the bias measurement, such as PCA [[1]](https://arxiv.org/abs/1607.06520) or WEAT [[2]](https://arxiv.org/abs/1608.07187), may suffer from unclearness in the lexical seeds selection, pointed in a recent ACL 2021 paper [[3]](https://www.aclanthology.org/2021.acl-long.148), the intrinsic measurements showed no correlation with extrinsic methods results, as showed a recent research [[4]](https://www.aclanthology.org/2021.acl-long.150). On the other hand, the gender bias datasets (Winobias, Winogender, StereoSet, CrowS-Pairs) can present the unconsistencies, pointed by another ACL paper [[5]](https://aclanthology.org/2021.acl-long.81) and might be far from  optimal in terms if bias measurement. 
The beneficial impact of the current extrinsic filter is its complete transparency and extensibility, which offers the user a great amont of control over the bias measurement parameters.


## Example of use
```
sentences = [ "He is going to make a cake.",
              "Olivia is going to program",
              "Nobody likes washing dishes",
              "He agreed to help me" ]

language = "en"
category = "gender"
minority = "female"
majority = "male"


f = UniversalBiasFilter(language, category, minority, majority)

f.filter(sentences)
```
Which returns `True`, as the number of sentences flagged as "minority" is less than the number of sentences tagged as "majority".
You can check the exact number by calling the `count_groups()` static method on the instance of the class and providing it with the extracted flags with the `flag_sentences()` static method:
```
f = UniversalBiasFilter("en", "gender", "female", "male")
flagged_sentences = f.flag_sentences(sentences)
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
flagged_sentences = f.flag_sentences(sentences)
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

## Structure of lexical seeds
Current struncture of the `lexicals.json` is as follows:
```
"en": {
		"religion": {
			"christianity": [],
			"buddhism_hinduism_jainism": [],
			"confucianism": [],
			"islam": [],
			"judaism": [],
			"atheism": []			
		},
		
		"race" : {
			"white": [],
			"black": [],
			"asian": [],
			"latino": [],
			"american_indian": []		
		},
		
		"ethnicity" : {
			"european": [],
			"african": [],
			"eurasian": [],
			"asian": [],
			"hispanic": [],
			"american_indian": []
		},
		
		"gender" : {
			"male": [],
			"female": []			
		},
		
		"sexual_orientation": {
			"hetero": [],
			"homo": []
		},
		
		"age": {
			"young": [],
			"old": []			
		},
		
		"appearencence": {
			"attractive": [],
			"unattractive": []
		},
		
		"disability": {
			"healthy": [],
			"disabled": []			
		},
		
		"experience": {
			"experienced": [],
			"inexperienced" : []
		},
		
		"education": {
			"educated": [],
			"uneducated": []
		},
		
		"economic_status": {
			"rich": [],
			"poor": []
		}	
	}
```
Changing the language key with the corresponding lexical seeds precision allows adapt this data structure to any language. 
The categories with their respective attributes can also be modified (the data extraction is made dynamicaly in the code). 


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

