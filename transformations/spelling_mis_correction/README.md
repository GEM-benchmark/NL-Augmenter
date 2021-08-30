# Spelling Mis-correction 🦎  + ⌨️ → 🐍 → 🦖 🦕 🌠 🌋 💀
Authors:

Nicholas Roberts <nick11roberts@cs.wisc.edu>
Vinay Prabhu <vinay@unify.id>
Sang Han <sanghan@protonmail.com>
Ryan Teehan <rsteehan@gmail.com>

## What type of a transformation is this?
This transformation is a mechanism for data augmentation which applies (neural) spelling correction to sentences whose words have been so heavily misspelled that spelling correction fails to recover the original word. This is inspired by text messages I often receive from certain anonymous sources. 

The transformation first applies a variant of the butter fingers perturbation with a high perturbation rate, and then applies [NeuSpell](https://aclanthology.org/2020.emnlp-demos.21/) to the resulting sentence. Words which have been corrected from the perturbed sentence are retained and inserted back into the original sentence. 

Examples include:
- Vinay got a cool whiteboard from the old office → Vinay may a could dashboard from the old office
- Andrew finally returned the French book to Chris that I bought last week → Andrew formally regained the French going to Chris that I caught pass week
- I make big lebowski references and collect plants in lieu of a personality → I make bat lebowski references and complete plants is also of a personality

This transformation is realistic and reprentative of spelling mis-corrected text that I have observed in personal correspondence, often due to pressing the wrong neighboring keys on a smartphone keyboard, or by mistakes made while using a keyboard with swipe-based input. One interpretation of this transformation is as a nondeterministic cipher of the input text which can be deciphered by a human annotator with some effort. 

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, 
text generation, etc. 

## Previous Work
1) Butter Finger implementation borrowed from this code: https://github.com/GEM-benchmark/NL-Augmenter/tree/main/transformations/butter_fingers_perturbation, which in turn was borrowed from this code: https://github.com/alexyorke/butter-fingers

2) NeuSpell is a neural spelling correction toolkit, which is used in this implementation: 

```bibtex
@inproceedings{jayanthi-etal-2020-neuspell,
    title = "{N}eu{S}pell: A Neural Spelling Correction Toolkit",
    author = "Jayanthi, Sai Muralidhar  and
      Pruthi, Danish  and
      Neubig, Graham",
    booktitle = "Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing: System Demonstrations",
    month = oct,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2020.emnlp-demos.21",
    doi = "10.18653/v1/2020.emnlp-demos.21",
    pages = "158--164",
    abstract = "We introduce NeuSpell, an open-source toolkit for spelling correction in English. Our toolkit comprises ten different models, and benchmarks them on naturally occurring misspellings from multiple sources. We find that many systems do not adequately leverage the context around the misspelt token. To remedy this, (i) we train neural models using spelling errors in context, synthetically constructed by reverse engineering isolated misspellings; and (ii) use richer representations of the context. By training on our synthetic examples, correction rates improve by 9{\%} (absolute) compared to the case when models are trained on randomly sampled character perturbations. Using richer contextual representations boosts the correction rate by another 3{\%}. Our toolkit enables practitioners to use our proposed and existing spelling correction systems, both via a simple unified command line, as well as a web interface. Among many potential applications, we demonstrate the utility of our spell-checkers in combating adversarial misspellings. The toolkit can be accessed at neuspell.github.io.",
}
```
## What are the limitations of this transformation?
The transformation's outputs are sometimes indecipherable (by me, at least), but this is something which can be tuned - to some degree - by varying the perturbation rate of the initial butter fingers perturbation. If the perturbation rate is too low, however, the transformed sentences might be largely similar to the original sentence. On the other hand, if the perturbation rate is too high, the sentence might not be linguistically plausible (however this is, to some degree, the desired effect). 
