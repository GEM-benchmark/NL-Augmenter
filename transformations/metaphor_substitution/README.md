# Metaphor Substitution

This transformation augments the input sentence by making a part of it use a
metaphor instead of its literal meaning.

Author: Marek Suppa

## What type of a transformation is this?

This transformation acts like a paraphraser by changing parts of the input
sentence from their literal to metaphorical meaning. This can help check the
model's robustness and generalizability on language that contains non-literal
elements.

Some examples:

> My heart _beats_ when he walks in the room
would become
> My heart _jumps_ when he walks in the room

> After a glass of wine, he relaxed up a bit
would become
> After a glass of wine, he loosened up a bit

> The tax cut will help the economy
would become
> The tax cut will uplift the economy


## What tasks does it intend to benefit?

This perturbation would benefit all tasks which take a sentence / paragraph /
document as input like text classification or text generation and possibly even
summarization, and question answering.

## What are the limitations of this transformation?

Metaphor generation / substitution is an open area of research, with the
current state-of-the-art systems being prone to generating sentences whose
meaning may diverge from that of the input sentence.

## Previous Work and References

```
@inproceedings{chakrabarty-etal-2021-mermaid,
    title = "{MERMAID}: Metaphor Generation with Symbolism and Discriminative Decoding",
    author = "Chakrabarty, Tuhin  and
      Zhang, Xurui  and
      Muresan, Smaranda  and
      Peng, Nanyun",
    booktitle = "Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies",
    month = jun,
    year = "2021",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2021.naacl-main.336",
    doi = "10.18653/v1/2021.naacl-main.336",
    pages = "4250--4261",
}
```

```
@article{stowe2021metaphor,
  title={Metaphor Generation with Conceptual Mappings},
  author={Stowe, Kevin and Chakrabarty, Tuhin and Peng, Nanyun and Muresan, Smaranda and Gurevych, Iryna},
  journal={arXiv preprint arXiv:2106.01228},
  year={2021}
}
```

```
@article{bhagat2013paraphrase,
  title={What is a paraphrase?},
  author={Bhagat, Rahul and Hovy, Eduard},
  journal={Computational Linguistics},
  volume={39},
  number={3},
  pages={463--472},
  year={2013},
  publisher={MIT Press One Rogers Street, Cambridge, MA 02142-1209, USA journals-info~…}
}
```
