# Multilingual Keyboard Change: AZERTY / QWERTY
This transformation acts like a perturbation by replacing some characters regarding a possible change of keyboard. Given a character `c_qwerty` located at a certain position in a QWERTY keyboard, it is replaced with the character `c_azerty` located at the same position of an AZERTY keyboard.

## What type of a transformation is this?
This transformation acts like a perturbation and makes lexical replacement.

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, text generation, etc. 

## Previous Work and References

```bibtex
@article{bi2012multilingual,
  title={Multilingual touchscreen keyboard design and optimization},
  author={Bi, Xiaojun and Smith, Barton A and Zhai, Shumin},
  journal={Human--Computer Interaction},
  volume={27},
  number={4},
  pages={352--382},
  year={2012},
  publisher={Taylor \& Francis}
}
```

## What are the limitations of this transformation?
Unlike a paraphraser, it is not capable of generating linguistically diverse text.