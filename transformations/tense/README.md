# Tense Tranformation 🦎  + ⌨️ → 🐍
This transformation converts sentences from one tense to the other, example: simple present to simple past. 

Author name: Tanay Dixit, Mukund Varma T

## What type of a transformation is this?

In this transformation, we convert a sentence into the target tense based on a verb, subject conjugation. 
This ensures that the context of the given sentence remains the same while the attribute of time changes. 

The following are some representative examples:

    Input: I can come to the party
    Target Tense: past
    Transformed Text: I can came to the party

    Input: I went to the park
    Target Tense: future
    Transformed Text: I will go to the park

    Input: I will go to the park.
    Target Tense: present
    Transformed Text: I go to the park.

## What tasks does it intend to benefit?

The task is designed to measure the capacity of language understanding in language models, specifically to understand the given tense of a sentence. 
This task is nominally simple for humans, since we have an understanding of time / a sequence of events but is difficult for a language model as they do not have any prior information about time. 
There have been a couple of attempts to perform controlled attribute text transformation (Logeswaran et. al) but is yet to be seen on language models trained in a general setting.  

## Citations

```bibtex
@article{DBLP:journals/corr/abs-1811-01135,
    author    = {Lajanugen Logeswaran and
                Honglak Lee and
                Samy Bengio},
    title     = {Content preserving text generation with attribute controls},
    journal   = {CoRR},
    volume    = {abs/1811.01135},
    year      = {2018},
    url       = {http://arxiv.org/abs/1811.01135},
    archivePrefix = {arXiv},
    eprint    = {1811.01135},
    timestamp = {Thu, 22 Nov 2018 17:58:30 +0100},
    biburl    = {https://dblp.org/rec/journals/corr/abs-1811-01135.bib},
    bibsource = {dblp computer science bibliography, https://dblp.org}
}
```

## What are the limitations of this transformation?

The transformation is not robust to all complex cases and is limited to only simple past/present/future tense conversions.
