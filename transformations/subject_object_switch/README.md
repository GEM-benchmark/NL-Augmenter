# Subject Object Switch
This transformation switches with each other the subject and object of English sentences to generate new sentences with a very high surface similarity but very different meaning. Can be used, for example, for augmenting data for Semantic Similarity English models.

Author name: William Soto
Author email: [williamsotomartinez@gmail.com](mailto:williamsotomartinez@gmail.com)
Author Affiliation: [SyNaLP](https://synalp.loria.fr/)([LORIA](https://www.loria.fr/en/))

## What type of a transformation is this?
If one or both sentences of a pair contain identifiables subject and object it will switch their places, creating new sentences with the different meaning.

## What tasks does it intend to benefit?
This transformation can be used for tasks like Paraphrase Detection, Paraphrase Generation, Semantic Similarity, and Entailment. It was particularly thought to avoid Semantic Similarity models giving high similarity to opposite sentences.

## What are the limitations of this transformation?
The transformation is very simple and can only be applied on a limited set of sentences (namely, those with subject and object and a positive target).

## Robustness Evaluation

### Sentence Operation
| Transformation                   | roberta-base-SST-2   | bert-base-uncased-QQP   | roberta-large-mnli   | roberta-base-imdb   |
|:---------------------------------|:---------------------|:------------------------|:---------------------|:--------------------|
| SentenceSubjectObjectSwitch      | 94.0->93.0 ( -1.0)   | 92.0->88.0 ( -4.0)      | 91.0->88.0 ( -3.0)   | 95.0->95.0 (  0.0)  |

### Sentence Pair Operation
| Transformation                   | paraphrase-xlm-r-multilingual-v1-MSRP | paraphrase-xlm-r-multilingual-v1-PAWS |
|:---------------------------------|:--------------------------------------|:--------------------------------------|
| PairSubjectObjectSwitch          | 69.0->30.0 (-39.0)                    | 44.0->24.0 (-20.0)                    |