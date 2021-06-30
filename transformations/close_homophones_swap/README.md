# Close Homophones Swap 🦎  + ⌨️ → 🐍
This perturbation adds perturbation to sentences and paragraphes mimicing writing behaviors where users swap words with similar homophones either intentionally or by accident.

Author name: Kaizhao Liang
Author email: kl2@illinois.edu
Author Affiliation: University of Illinois, Urbana Champaign

## What type of a transformation is this?
This transformation acts like a perturbation to test robustness. Few words picked at random are replaced with words with similar homophones
which sound similar or look similar. Generated transformations display high similarity to the 
source sentences i.e. the code outputs highly precise generations. 

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, 
text generation, etc. 

## Previous Work
1) There has been some recent work studying how to create human-like behavior using phonetic information:
```bibtex
@article{eger2019text,
  title={Text processing like humans do: Visually attacking and shielding NLP systems},
  author={Eger, Steffen and {\c{S}}ahin, G{\"o}zde G{\"u}l and R{\"u}ckl{\'e}, Andreas and Lee, Ji-Ung and Schulz, Claudia and Mesgar, Mohsen and Swarnkar, Krishnkant and Simpson, Edwin and Gurevych, Iryna},
  journal={arXiv preprint arXiv:1903.11508},
  year={2019}
}
```

## What are the limitations of this transformation?
Some of the word choices might not be completely natural to normal human behavior, since humans "prefer" some words over others even they sound exactly the same. So it might not be fully reflecting the natural distribution of intentional or unintentional swapping of words.
