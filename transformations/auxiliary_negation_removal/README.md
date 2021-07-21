# Auxiliary Negation Removal
This transformation removes the negation of English auxiliaries to generate new sentences with oposite meanings. Can be used, for example, for augmenting examples for Semantic Similarity English models.

Author name: William Soto
Author email: [williamsotomartinez@gmail.com](mailto:williamsotomartinez@gmail.com)
Author Affiliation: [SyNaLP](https://synalp.loria.fr/)([LORIA](https://www.loria.fr/en/))

## What type of a transformation is this?
If one or both sentences of a pair contain negated auxiliaries it will remove the negation, creating new sentences with the oposite meaning. A new pair with both sentence negated (when possible) will keep the original target label and new pairs changing just the first or the second sentence will invert the trget label.

## What tasks does it intend to benefit?
This transformation can be used for tasks like Paraphrase Detection, Paraphrase Generation, Semantic Similarity, and Entailment. It was particularly thought to avoid Semantic Similarity models giving high similarity to oposite sentences.

## What are the limitations of this transformation?
The transformation is very simple and can only be applied on a limited set of sentences (namely, those with negated auxiliaries).
