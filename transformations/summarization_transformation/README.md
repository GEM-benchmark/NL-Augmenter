# Sentence Summarizaiton 🦎  + ⌨️ → 🐍
This perturbation extracts all types of text sources (sentence, paragraph, etc.) for the summarization of the sentence without changing meanings.

Author name: Jing Zhang (jing.zhang2@emory.edu, Emory University)

Author name: Zhexiong Liu (zhexiong@cs.pitt.edu, University of Pittsburgh)

## What type of a transformation is this?
This transformation acts like extracting subjects, verbs, and objects as an summarization of the given sentence. Keep the original basic meanings and retain the negations.

It also robust to generate the summarizaiton of the sentence which contains grammar issues (test case 2).

## What tasks does it intend to benefit?
It is useful for question & answering, sentiment analysis, sentence pair relatedness, and other tasks. No need to require any pretrained model to abstract the sentence, and no need to require entire dataset to generate 
summarization of the sentence (such as TF-IDF method), it summarizes only based on each individual input sentence.

## Previous Work
1) Summarization implementation borrowed and modified from this code https://github.com/NSchrading/intro-spacy-nlp

3) There has been some recent work utilizing this idea:
```bibtex
@inproceedings{zhang2021smat,
  title={SMAT: An Attention-Based Deep Learning Solution to the Automation of Schema Matching},
  author={Zhang, Jing and Shin, Bonggun and Choi, Jinho D and Ho, Joyce C},
  booktitle={European Conference on Advances in Databases and Information Systems},
  pages={260--274},
  year={2021},
  organization={Springer}
}
```
## What are the limitations of this transformation?
The transformation's implementation is not optimized as best, and could not extract compound subject or object.
