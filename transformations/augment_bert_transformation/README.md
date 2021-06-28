# Butter Fingers Perturbation 🦎  + ⌨️ → 🐍
This perturbation change one word to all types of text sources (sentence, paragraph, etc.) using the masked token from BERT. 

Author name: Colombo Pierre and Emile Chapuis
Author email: colombo.pierre@gmail.com and chapuis.emile@gmail.com
Author Affiliation: Telecom Paris

## What type of a transformation is this?
This transformation acts as a perturbation to test robustness, BERT will generate a highly probable word given a random masked token.
Generated sentences display high similarity to the source sentences. 

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, 
text generation, etc. 

## Previous Work
1) There has also been some recent work in using BERT to augment text sentences:
```bibtex
@article{kumar2020data,
  title={Data augmentation using pre-trained transformer models},
  author={Kumar, Varun and Choudhary, Ashutosh and Cho, Eunah},
  journal={arXiv preprint arXiv:2003.02245},
  year={2020}
}
```

```bibtex
@inproceedings{wu2019conditional,
  title={Conditional bert contextual augmentation},
  author={Wu, Xing and Lv, Shangwen and Zang, Liangjun and Han, Jizhong and Hu, Songlin},
  booktitle={International Conference on Computational Science},
  pages={84--95},
  year={2019},
  organization={Springer}
}
```
## What are the limitations of this transformation?
The quality of transformation depends on the quality of the pretrained language model. That is why our implementation allows using a LM model finetuned on specific the dataset we would like to augment (using the str_id parameter).
