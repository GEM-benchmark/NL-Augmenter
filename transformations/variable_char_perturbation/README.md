# Variable Character Perturbation 🦎 + 🎮 → 🐍
This perturbation performs 5 way perturbations on non numeric words, either deletion insertion substitution swapping and duplication, with configurable probability and subset of perturbations to choose from.

For example: Banana -> Banan | Banabna | Banama | Baanna | Bannana


Author name: Abhilash Pal
<br/>
Author email: abhilash.pal@tum.de / abhilashpal8@gmail.com
<br/>
Author Affiliation: Technische Universität München

## What type of a transformation is this?
This transformation adds random noise to the input word. Based on a predefined probability, words of atleast length 3 are perturbed with either random insertion deletion substitution swapping or duplication. Users can set which of the transformations they want as well.
Generated transformations display high similarity to the source sentences i.e. the code outputs highly precise generations. 



## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, 
text generation, etc. 

```python evaluate.py -t VariableCharPerturbation -task TEXT_CLASSIFICATION```
```model_name = "aychang/roberta-base-imdb"```

The accuracy of a RoBERTa model (fine-tuned on IMDB) on a subset of IMDB sentiment dataset = 96% The accuracy of the same model on the perturbed set = 94%


## Previous Work

```bibtex
@inproceedings{karpukhin-etal-2019-training,
    title = "Training on Synthetic Noise Improves Robustness to Natural Noise in Machine Translation",
    author = "Karpukhin, Vladimir  and
      Levy, Omer  and
      Eisenstein, Jacob  and
      Ghazvininejad, Marjan",
    booktitle = "Proceedings of the 5th Workshop on Noisy User-generated Text (W-NUT 2019)",
    month = nov,
    year = "2019",
    address = "Hong Kong, China",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/D19-5506",
    doi = "10.18653/v1/D19-5506",
    pages = "42--47",
    abstract = "Contemporary machine translation systems achieve greater coverage by applying subword models such as BPE and character-level CNNs, but these methods are highly sensitive to orthographical variations such as spelling mistakes. We show how training on a mild amount of random synthetic noise can dramatically improve robustness to these variations, without diminishing performance on clean text. We focus on translation performance on natural typos, and show that robustness to such noise can be achieved using a balanced diet of simple synthetic noises at training time, without access to the natural noise data or distribution.",
}

```


## What are the limitations of this transformation?
- If perturbation probability is kept very high, output sentences might be extremely perturbed, with perturbations on every word with len>3.

