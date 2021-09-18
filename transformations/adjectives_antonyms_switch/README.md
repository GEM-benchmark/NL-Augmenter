# Adjectives Antonyms Switch
This transformation switches English adjectives in a sentence with their antonyms to generate new sentences with oposite meanings. Can be used, for example, for augmenting examples for Semantic Similarity English models.

Author name: William Soto
Author email: [williamsotomartinez@gmail.com](mailto:williamsotomartinez@gmail.com)
Author Affiliation: [SyNaLP](https://synalp.loria.fr/)([LORIA](https://www.loria.fr/en/))

## What type of a transformation is this?
When there are adjectives present in a sentences, if those adjectives have an antonym in wordnet, it will switch the original adjective with its antonym. This willcreate new sentences with the oposite meaning. A new pair where both sentences have had changes will keep the original target label and new pairs where just the first or the second sentence have been changed will invert the target label.

## What tasks does it intend to benefit?
This transformation can be used for tasks like Paraphrase Detection, Paraphrase Generation, Semantic Similarity, and Entailment. It was particularly thought to avoid Semantic Similarity models giving high similarity to oposite sentences.

## What are the limitations of this transformation?
The transformation is very simple and can only be applied on a limited set of sentences (namely, those with adjectives that have antonyms in wordnet).
