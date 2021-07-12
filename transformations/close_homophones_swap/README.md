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
1) There has been some recent work studying the adversarial effects of swapping out similarly sounding words:
```bibtex
@article{eger2020hero,
  title={From Hero to Z$\backslash$'eroe: A Benchmark of Low-Level Adversarial Attacks},
  author={Eger, Steffen and Benz, Yannik},
  journal={arXiv preprint arXiv:2010.05648},
  year={2020}
}
```

## What are the limitations of this transformation?
Some of the word choices might not be completely natural to normal human behavior, since humans "prefer" some words over others even they sound exactly the same. So it might not be fully reflecting the natural distribution of intentional or unintentional swapping of words.
