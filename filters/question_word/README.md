## Question type filter

## What type of a filter is this?
This filter helps identify the question category either based on question word or type of answer
Authors: Tanay Dixit, Ananya B Sai
Email: tanat.dixit@smail.iitm.ac.in , ananya.b.sai@gmail.com

## Why is measuring performance on this split important?
This filter provides a fine-grained analysis of question answering systems,helps to identify possible biases towards some categories of questions.
### Evaluation
Using default datasets and models 
| Question Type | Number of Samples | EM|
|---------------|-----------|----|
| Numeric |356 |70.22|
| Date    |193  |79.79|
| Person   |301 |65.44|
| Location |176 |56.86|
| Common noun phrases |411| 56.20|
| Adjective phrases  |267| 49.43|
| Verb Phrases |134 | 40.29|

One can infer that answers involving phrases are more challenging

| Question Type | Number of Samples | EM|
|---------------|-----------|----|
|Where | 120| 57.5|
|What | 1117| 55.59  |
|Which | 106 | 58.49  |
|Who |  353  |  66.57  |
|Why |  22  |   27.27  |

One can infer that "Why" type of questions are difficult to answer 

## Related Work
```bibtex
@article{DBLP:journals/corr/RajpurkarZLL16,
  author    = {Pranav Rajpurkar and
               Jian Zhang and
               Konstantin Lopyrev and
               Percy Liang},
  title     = {SQuAD: 100, 000+ Questions for Machine Comprehension of Text},
  journal   = {CoRR},
  volume    = {abs/1606.05250},
  year      = {2016},
  url       = {http://arxiv.org/abs/1606.05250},
  archivePrefix = {arXiv},
  eprint    = {1606.05250},
  timestamp = {Mon, 24 Aug 2020 14:01:25 +0200},
  biburl    = {https://dblp.org/rec/journals/corr/RajpurkarZLL16.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
@article{DBLP:journals/corr/abs-1904-02651,
  author    = {Soham Parikh and
               Ananya B. Sai and
               Preksha Nema and
               Mitesh M. Khapra},
  title     = {ElimiNet: {A} Model for Eliminating Options for Reading Comprehension
               with Multiple Choice Questions},
  journal   = {CoRR},
  volume    = {abs/1904.02651},
  year      = {2019},
  url       = {http://arxiv.org/abs/1904.02651},
  archivePrefix = {arXiv},
  eprint    = {1904.02651},
  timestamp = {Wed, 24 Apr 2019 12:21:25 +0200},
  biburl    = {https://dblp.org/rec/journals/corr/abs-1904-02651.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```
## What are the limitations of this filter?
It relies on lexical and purely context-free matching for filtering out questions. 
