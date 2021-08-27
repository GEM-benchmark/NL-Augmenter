# Man-ify (and Woman-ify) 


> This perturbation takes objects + subjects within a sentence, finds their word2vec representation, and then applies adds the man-vector, and the woman-vector.

Author name: Roy Rinberg
Author email: royrinberg@gmail.com
Author Affiliation: Columbia University

# Extra:
need to run `python -m spacy download en_core_web_sm` before running.

## Roy work to do :
1. get word2vec working - done
2. figure out SVO break down of sentences - close 
3. potentially - figure out gender of the SVO (using french dictionary)
4. mash it into the transformation in the expected format 

1. set up test.json
2. write the readme properly

## What type of a transformation is this?

This transformation acts like a perturbation to test robustness. Few words picked at random are replaced with their common spelling errors if these words are in the [corpus of mis-spell words](https://www.dcs.bbk.ac.uk/~ROGER/corpora.html). Generated transformations display high similarity to the source sentences i.e. the code outputs highly precise generations.



## Data Curation

Dataset Source: [https://www.dcs.bbk.ac.uk/~ROGER/corpora.html](https://www.dcs.bbk.ac.uk/~ROGER/corpora.html)

A json file named spell_errors.json has been created by merging words from below files. Json file has actual word in lowercase as key and list of mis-spelt words of the key as value. The list of mis-spelt words has been created from all the files by taking union of words from below files when key word appears in multiple files. 


## How it works:
1. https://github.com/RaRe-Technologies/gensim 




## What are the limitations of this transformation?
- The transformation applies Word2Vec, but does not check whether the 


- Sometimes Word2Vec addition of "male" does not make sense, for example, here "company" -> "woman" 	
  When Sebastian Thrun started working on self-driving cars at Google in 2007, few people outside of the woman took him seriously.

- A foreign name like "Dev" which is someone's name, may be interpretted as a developer, and changed like a noun.

## References (bibtex)


@inproceedings{rehurek_lrec,
      title = {{Software Framework for Topic Modelling with Large Corpora}},
      author = {Radim {\v R}eh{\r u}{\v r}ek and Petr Sojka},
      booktitle = {{Proceedings of the LREC 2010 Workshop on New
           Challenges for NLP Frameworks}},
      pages = {45--50},
      year = 2010,
      month = May,
      day = 22,
      publisher = {ELRA},
      address = {Valletta, Malta},
      note={\url{http://is.muni.cz/publication/884893/en}},
      language={English}
}







######################### Ignore after this:
* Roger Mitton, A Corpus of Spelling Errors, [https://www.dcs.bbk.ac.uk/~ROGER/corpora.html](https://www.dcs.bbk.ac.uk/~ROGER/corpora.html)

```latex
@article{deorowicz2005correcting,
  title={Correcting spelling errors by modelling their causes},
  author={Deorowicz, Sebastian and Ciura, Marcin G},
  journal={International journal of applied mathematics and computer science},
  volume={15},
  pages={275--285},
  year={2005}
}
```




