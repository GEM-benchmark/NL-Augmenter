# Diverse Paraphrase Generation🦎  + ⌨️ → 🐍
This transformation produces multiple diverse paraphrases for a given sentence in English.

## What type of a transformation is this?
This transformation is a multi-output sentence level paraphrase generation model, specifically catered towards generating `num_outputs` (user specified) diverse outputs. 

It has support for 4 candidate selection methods:

a) dips: Based on Kumar et. al. 2019. (See Below)
b) diverse_beam: Based on Vijaykumar et. al 2018. (See Below)
c) beam: Selects top `num_outputs` candidates in the beam search.
d) random: Randomly selects `num_outputs` candidates.

Eg:
```python
>>> t = DiverseParaphrase(augmenter='dips', num_outputs=4)
>>> t.generate('Joe Biden is the President of USA.')
```

Replace augmenter with any of the above mentioned options. 
Default: augmenter='dips', num_outputs=4. 
In most cases, dips should be the preferred choice.

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which need diverse paraphrase candidates for augmentation in tasks like text classification, text generation, etc. 

## Previous Work
1. DiPS: Original Implementation [here](https://github.com/malllabiisc/DiPS)
```bibtex
@inproceedings{dips2019,
    title = "Submodular Optimization-based Diverse Paraphrasing and its Effectiveness in Data Augmentation",
    author = "Kumar, Ashutosh  and
      Bhattamishra, Satwik  and
      Bhandari, Manik  and
      Talukdar, Partha",
    booktitle = "Proceedings of the 2019 Conference of the North {A}merican Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers)",
    month = jun,
    year = "2019",
    address = "Minneapolis, Minnesota",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/N19-1363",
    pages = "3609--3619"
}
```

2. Diverse Beam
```bibtex
@paper{AAAI1817329,
	author = {Ashwin Vijayakumar and Michael Cogswell and Ramprasaath Selvaraju and Qing Sun and Stefan Lee and David Crandall and Dhruv Batra},
	title = {Diverse Beam Search for Improved Description of Complex Scenes},
	conference = {AAAI Conference on Artificial Intelligence},
	year = {2018},
	keywords = {Recurrent Neural Networks, Beam Search, Diversity},
	url = {https://www.aaai.org/ocs/index.php/AAAI/AAAI18/paper/view/17329}
}
```

## What are the limitations of this transformation?
The base paraphrasing model used by this transformation is backtranslation (En -> De -> En). If the base model is poor, the candidate outputs will be of low-quality.
