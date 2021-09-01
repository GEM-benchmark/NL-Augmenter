# Syntactically Diverse Paraphrasing using Sow Reap models 🦎  + ⌨️ → 🐍
This transformation produces syntactically diverse paraphrases for a given input sentence in English.


## What type of a transformation is this?
This transformation is capable of generating multiple syntactically diverse paraphrases for a given sentence.
The number of outputs can be specified by the user through `max_outputs`.

The model paraphrases inputs using a two step framework:
1. SOW (Source Order reWriting): This step enumerates multiple feasible syntactic transformations of the input sentence.
2. REAP (REarrangement Aware Paraphrasing): This step conditions on the multiple reorderings/ rearragements produces by SOW and outputs diverse paraphrases corresponds to these reoderings.


## What tasks does it intend to benefit?
This perturbation would benefit all tasks which need paraphrases for data augmentation.

## Previous Work
Based on the paper '[Neural Syntactic Preordering for Controlled Paraphrase Generation](https://aclanthology.org/2020.acl-main.22.pdf)' by Goyal et. al 2020.

Original Implementation: [here](https://github.com/malllabiisc/DiPS)
```bibtex
@inproceedings{goyal-durrett-2020-neural,
    title = "Neural Syntactic Preordering for Controlled Paraphrase Generation",
    author = "Goyal, Tanya  and
      Durrett, Greg",
    booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2020.acl-main.22",
    doi = "10.18653/v1/2020.acl-main.22",
    pages = "238--252",
    abstract = "Paraphrasing natural language sentences is a multifaceted process: it might involve replacing individual words or short phrases, local rearrangement of content, or high-level restructuring like topicalization or passivization. Past approaches struggle to cover this space of paraphrase possibilities in an interpretable manner. Our work, inspired by pre-ordering literature in machine translation, uses syntactic transformations to softly {``}reorder{''} the source sentence and guide our neural paraphrasing model. First, given an input sentence, we derive a set of feasible syntactic rearrangements using an encoder-decoder model. This model operates over a partially lexical, partially syntactic view of the sentence and can reorder big chunks. Next, we use each proposed rearrangement to produce a sequence of position embeddings, which encourages our final encoder-decoder paraphrase model to attend to the source words in a particular order. Our evaluation, both automatic and human, shows that the proposed system retains the quality of the baseline approaches while giving a substantial increase in the diversity of the generated paraphrases.",
}
```
## What are the limitations of this transformation?
The model are trained on the ParaNMT-50M dataset, which tends to be quite noisy. A better paraphrase dataset would improve performance.
