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
@inproceedings{eger-benz-2020-hero,
    title = "From Hero to Z{\'e}roe: A Benchmark of Low-Level Adversarial Attacks",
    author = "Eger, Steffen  and
      Benz, Yannik",
    booktitle = "Proceedings of the 1st Conference of the Asia-Pacific Chapter of the Association for Computational Linguistics and the 10th International Joint Conference on Natural Language Processing",
    month = dec,
    year = "2020",
    address = "Suzhou, China",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2020.aacl-main.79",
    pages = "786--803",
    abstract = "Adversarial attacks are label-preserving modifications to inputs of machine learning classifiers designed to fool machines but not humans. Natural Language Processing (NLP) has mostly focused on high-level attack scenarios such as paraphrasing input texts. We argue that these are less realistic in typical application scenarios such as in social media, and instead focus on low-level attacks on the character-level. Guided by human cognitive abilities and human robustness, we propose the first large-scale catalogue and benchmark of low-level adversarial attacks, which we dub Z{\'e}roe, encompassing nine different attack modes including visual and phonetic adversaries. We show that RoBERTa, NLP{'}s current workhorse, fails on our attacks. Our dataset provides a benchmark for testing robustness of future more human-like NLP models.",
}
```

## What are the limitations of this transformation?
Some of the word choices might not be completely natural to normal human behavior, since humans "prefer" some words over others even they sound exactly the same. So it might not be fully reflecting the natural distribution of intentional or unintentional swapping of words.
