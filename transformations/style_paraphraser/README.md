# Paraphrasing through the use of style transfer

This perturbation provides a range of possible styles of writing, enabling an easy use of style transfer paraphrase models originally introduced in the paper [Reformulating Unsupervised Style Transfer as Paraphrase Generation (2020)](https://arxiv.org/abs/2010.05700) (K. Krishna et al.), published at EMNLP 2020.

Author name: Filip Cornell
Author email: c.filip.cornell@gmail.com
Author affiliation: KTH Royal Institute of Technology

## What type of a transformation is this?

This is a paraphraser that transfers between different styles. Several models are enabled and should be usable through this interface. This therefore provides an easy-to-use interface for these large paraphrasing models, giving often high-quality paraphrases.

The current styles of writing supporting are:

- Shakespeare
- Switchboard
- Tweets
- Bible
- Romantic poetry
- Basic

I will most likely add more pre-trained models as possibilities to use as I add more of the pre-trained models to Huggingface. For more information on these styles, please see the original paper: https://arxiv.org/abs/2010.05700.

## What tasks does it intend to benefit?
Given the multiple different models enabled to be used easily through this interface (Basic, Bible, Shakespeare, Tweets, Switchboard and Romantic poetry), this can be used in a variety of cases. However, this can mainly work as an augmentation for improving sentence classification, perhaps from different domains.

## Data and Code Provenance
This transformation makes use of code and pre-trained models from: https://github.com/martiansideofthemoon/style-transfer-paraphrase. This is therefore entirely based on the paper [Reformulating Unsupervised Style Transfer as Paraphrase Generation
](https://arxiv.org/abs/2010.05700).

The license of the original code is included in the folder, and is an MIT License. Note that the author of this perturbation is not the author of the original code and paper, but has been in direct contact with the main author of the original paper.

## Reference to the original work

The bibtex-reference to the original work is:

```
@inproceedings{style20,
author={Kalpesh Krishna and John Wieting and Mohit Iyyer},
Booktitle = {Empirical Methods in Natural Language Processing},
Year = "2020",
Title={Reformulating Unsupervised Style Transfer as Paraphrase Generation},
}
```

## What are the limitations of this transformation?

This transformation is limited to different styles of writing in English. No other languages are supported.

Also note, that if long sentences are sent in, or two sentences in one, there is a risk sometimes that only a part will be paraphrased (see the example `"Hi there, how are you doing today? "` in the tests).

