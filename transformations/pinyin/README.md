# Pinyin Chinese Character Transcription 🀄  → 🅰

This transformation transcribes Chinese characters into their Mandarin 
pronunciation using the [Pinyin romanization
scheme](https://en.wikipedia.org/wiki/Pinyin).

Author name: Connor Boyle
Author email: connor.bo@gmail.com
Author Affiliation: University of Washington

## What type of a transformation is this?

This transformation segments the input Mandarin sentence using Spacy's default
Chinese NLP pipeline, then transcribes those segments (without tone markers) 
using the Pinyin romanization scheme. The resulting outputs represent the 
same content in a different writing system.

## What tasks does it intend to benefit?

This task would benefit any Chinese NLP task that has a 
sentence/paragraph/document as input.

## Previous Work

The character-to-pinyin converter at the core of this project is a neural 
model described in this paper:

```bibtex
@article{DBLP:journals/corr/abs-2004-03136,
  author    = {Kyubyong Park and
               Seanie Lee},
  title     = {g2pM: {A} Neural Grapheme-to-Phoneme Conversion Package for MandarinChinese
               Based on a New Open Benchmark Dataset},
  journal   = {CoRR},
  volume    = {abs/2004.03136},
  year      = {2020},
  url       = {https://arxiv.org/abs/2004.03136},
  archivePrefix = {arXiv},
  eprint    = {2004.03136},
  timestamp = {Wed, 08 Apr 2020 17:08:25 +0200},
  biburl    = {https://dblp.org/rec/journals/corr/abs-2004-03136.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```

## What are the limitations of this transformation?

Chinese word segmentation (CWS) is a difficult task. This transformation relies
on Spacy's default segmentation, which is of unknown quality. Transcription to
pinyin is also non-trivial, but the model used for that step is nearly 
state-of-the-art, while remaining lightweight.
