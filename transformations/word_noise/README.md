# Word Noise
This transformation chooses a set of words at random from the context and the question and forms a sentence out of them. The sentence is then prepended or appended to the context.

Author: Saqib N. Shamsi

## What type of a transformation is this?
This transformation is a perturbation to the context of the QA pair and is analogous to adding noise in image augmentation. The transformation is inspired by the **AddAny** method described in [Adversarial SQUAD](https://arxiv.org/abs/1707.07328). However, instead of probing the model to generate adversaries, we simply select words at random from the context and question and join them together into a sentence, ignoring the grammar. Thus, the method is model agnostic unlike **AddAny**.

## What tasks does it intend to benefit?
The transformation is aimed at augmenting QA data since the introduction of random words to the context is unlikely to change the semantics of the context. However, there is still a small chance that the perturbation changes the semantics of the context.

## What are the limitations of this transformation?
The transformation might cause a change in the semantics of the context thus invalidating the answer for the question.