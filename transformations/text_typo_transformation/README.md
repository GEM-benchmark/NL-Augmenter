# Butter Fingers Perturbation 🦎  + ⌨️ → 🐍

This perturbation simulates typos in each text using misspellings, keyboard distance, and swapping.

Author name: Priyank Soni (priyanksonigeca7@gmail.com)

## What type of a transformation is this?
Here letters in each words are replaced with probability given as argument, probability of words to be augmented also given as argument, also minimum # of letters in a word for a valid augmentation,
minimum # of letters to be replaced/swapped in each word, maximum # of letters to be replaced/swapped in each word,
minimum # of words to be augmented, maximum # of words to be augmented, number of augmentations to be performed for each text,
list of target words that the augmenter should prioritize to augment first are given as arguments.

####Example:
Ujjal Dev Dosanjh served as 33rd Premier of British Columbia from 2000 to 2001  --> Jujal Dev Dosanjh served as 3r3d Premier of Brittish Columbia frome 2000 to 2001
## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, 
text generation, etc. 

## Previous Work
1) Text Typo Transformation borrowed from this code https://github.com/facebookresearch/AugLy

```bibtex
@misc{bitton2021augly,
  author       = {Joanna Bitton and Zoe Papakipos},
  title        = {AugLy: A data augmentations library for audio, image, text, and video.},
  year         = {2021},
  howpublished = {\url{https://github.com/facebookresearch/AugLy}},
  doi          = {10.5281/zenodo.5014032}
}
```

## What are the limitations of this transformation?
The transformation's outputs are too simple to be used for data augmentation. Unlike a paraphraser, it is not capable of
 generating linguistically diverse text.
