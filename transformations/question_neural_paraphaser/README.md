# Dialog Rephrasing transformation
This perturbation uses a model to rephrase a sentence in a natural manner and was proposed for paraphrasing questions.


Author name: Pierre Colombo and Emile Chapuis
Author email: colombo.pierre@gmail.com and emile.chapuis@gmail.com
Author Affiliation: Telecom Paris

## What type of a transformation is this?
This transformation uses a neural model finetuned for question rephrasing. 

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, 
text generation, etc. It has been proposed for question paraphrasing.

## Previous Work
This work relies on T5 and was finetuned following ``https://towardsdatascience.com/paraphrase-any-question-with-t5-text-to-text-transfer-transformer-pretrained-model-and-cbb9e35f1555``
```bibtex
@article{raffel2019exploring,
  title={Exploring the limits of transfer learning with a unified text-to-text transformer},
  author={Raffel, Colin and Shazeer, Noam and Roberts, Adam and Lee, Katherine and Narang, Sharan and Matena, Michael and Zhou, Yanqi and Li, Wei and Liu, Peter J},
  journal={arXiv preprint arXiv:1910.10683},
  year={2019}
}
```
Implementation heavily borrowed from 
```bibtex
@inproceedings{wolf2020transformers,
  title={Transformers: State-of-the-art natural language processing},
  author={Wolf, Thomas and Chaumond, Julien and Debut, Lysandre and Sanh, Victor and Delangue, Clement and Moi, Anthony and Cistac, Pierric and Funtowicz, Morgan and Davison, Joe and Shleifer, Sam and others},
  booktitle={Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing: System Demonstrations},
  pages={38--45},
  year={2020}
}
```

## What are the limitations of this transformation?
The quality of transformation depends on the quality of the neural model and it was original proposed for dialog systems.