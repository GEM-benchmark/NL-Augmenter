# Backtranslation for Named Entity Recognition 🦓 ️→ 🐎
This transformation exploits backtranslation (en &rarr; de &rarr; en) to generate diverse linguistic variations of the contexts around the entity mention(s).

Contributors: Usama Yaseen (usama.yaseen@siemens.com), Stefan Langer (langer.stefan@siemens.com)

Affiliation: Siemens AG

## What type of a transformation is this?
This transformation split the token sequences into segments of entity mention(s) or "contexts" around the entity mention(s). *Backtranslation* is used to paraphrase the contexts around the entity mention(s), thus resulting in an augmentation of the original token sequence.

### Example

**Inputs**

tokens: `["Shannon", "received", "his", "PhD", "from", "MIT", "in", "1940", "."]`

tags: `["B-PER", "O", "O", "O", "O", "B-ORG", "O", "O", "O"]`

**Outputs**

tokens: `["Shannon", "received", "his", "doctorate", "from", "MIT", "in", "1940", "."]`

tags: `["B-PER", "O", "O", "O", "O", "B-ORG", "O", "O", "O"]`

## What tasks does it intend to benefit?
This transformation would benefit sequence labelling tasks such as named entity recognition.

## Previous Work and References
1) The transformation was proposed by [Yaseen and Langer, 2021](https://arxiv.org/abs/2108.11703).

```bibtex
@article{yaseen-and-langer-backtranslation-ner,
  author    = {Usama Yaseen and
               Stefan Langer},
  title     = {Data Augmentation for Low-Resource Named Entity Recognition Using Backtranslation},
  journal   = {CoRR},
  volume    = {abs/2108.11703},
  year      = {2021},
  url       = {https://arxiv.org/abs/2108.11703},
  archivePrefix = {arXiv},
  eprint    = {2108.11703},
  abstract = "The state of art natural language processing systems relies on sizable training datasets to achieve high performance. Lack of such datasets in the specialized low resource domains lead to suboptimal performance. In this work, we adapt backtranslation to generate high quality and linguistically diverse synthetic data for low-resource named entity recognition. We perform experiments on two datasets from the materials science (MaSciP) and biomedical domains (S800). The empirical results demonstrate the effectiveness of our proposed augmentation strategy, particularly in the low-resource scenario."
}
```

## What are the limitations of this transformation?
This transformation intends to generate linguistically diverse paraphrases of the contexts around the entity mention(s) using backtranslation. The quality of the generated paraphrases solely depends on the underlying machine translation model; also the generated paraphrase may not always preserve the underlying semantics of the contexts.
Nevertheless, exploiting this transformation as a data augmentation strategy has been empirically shown to improve the performance of the underlying sequence (NER) model ([Yaseen and Langer, 2021](https://arxiv.org/abs/2108.11703)).