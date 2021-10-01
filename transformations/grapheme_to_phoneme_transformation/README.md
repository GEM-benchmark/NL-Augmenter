# Grapheme to Phoenem Substitution

This perturbration adds noise to sentence. For randomly selected words in a sentence, words are changed to their phoenems. Grapheme to phoenem substitution is useful in human language techonlogies related to speech. An example of grapheme to phoenem substitution is "permit"---> 
[P ER0 M IH1 T']. Since our goal here is to add noise to the sentence, we do not consider stress as indicated by numbers('permit'is transformed as permiht). 

Author name: 
Rabin Banjade(rbnjade1@memphis.edu)
Priti Oli (poli@memphis.edu)

## What type of a transformation is this?
This transformation can help in testing robustness. Humans can understand what the word refers to based on pronunciation and context to some extent. To some extent, this perturbation is similar to introducing spelling errors.

## What tasks does it intend to benefit?
This perturbation would benefit tasks on text classification and generation. 


## Related Work

There are variety of works on grapheme to phoneme conversion. One of such works is[1]. Mohammad[2] highlights phoenem substitution as one of the transformations used in toxic comments.
```
1. @article{bisani2008joint,
  title={Joint-sequence models for grapheme-to-phoneme conversion},
  author={Bisani, Maximilian and Ney, Hermann},
  journal={Speech communication},
  volume={50},
  number={5},
  pages={434--451},
  year={2008},
  publisher={Elsevier}
}

2. @article{mohammad2018preprocessing,
  title={Is preprocessing of text really worth your time for online comment classification?},
  author={Mohammad, Fahim},
  journal={arXiv preprint arXiv:1806.02908},
  year={2018}
}
```



## What are the limitations of this transformation?

For this particular task we have used `pronouncing` python package which uses CMU pronouncing dictionary which might not be exhaustive list of all grapheme to phoneme conversion. 
