# Tense Tranformation 🦎  + ⌨️ → 🐍
This transformation converts sentences from one tense to the other, example: simple present to simple past.

Author name: Tanay Dixit, Mukund Varma T

## What type of a transformation is this?

In this transformation, we convert a sentence into the target tense based on a verb, subject conjugation.
This ensures that the context of the given sentence remains the same while the attribute of time changes.

The following are some representative examples:

    Input: My father goes to gym every day
    Target Tense: past
    Transformed Text: My father went to gym every day

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
@inproceedings{DBLP:conf/nips/LogeswaranLB18,
  author    = {Lajanugen Logeswaran and
               Honglak Lee and
               Samy Bengio},
  editor    = {Samy Bengio and
               Hanna M. Wallach and
               Hugo Larochelle and
               Kristen Grauman and
               Nicol{\`{o}} Cesa{-}Bianchi and
               Roman Garnett},
  title     = {Content preserving text generation with attribute controls},
  booktitle = {Advances in Neural Information Processing Systems 31: Annual Conference
               on Neural Information Processing Systems 2018, NeurIPS 2018, December
               3-8, 2018, Montr{\'{e}}al, Canada},
  pages     = {5108--5118},
  year      = {2018},
  url       = {https://proceedings.neurips.cc/paper/2018/hash/7cf64379eb6f29a4d25c4b6a2df713e4-Abstract.html},
  timestamp = {Thu, 21 Jan 2021 15:15:20 +0100},
  biburl    = {https://dblp.org/rec/conf/nips/LogeswaranLB18.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```
### Data and Source Code
change tense and verb infliction borrowed from https://github.com/bendichter/tenseflow

## What are the limitations of this transformation?

The transformation is not robust to all complex cases and is limited to only simple past/present/future tense conversions.
Examples where it fails: <br>
Input: I will go for dinner after I am done playing tennis.
to_tense: past
Output: I went for dinner after I was did playing tennis.
