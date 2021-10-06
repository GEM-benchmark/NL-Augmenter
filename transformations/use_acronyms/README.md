# Use Acronyms
This transformation changes groups of works for their equivalent acronyms.

Author name: William Soto
Author email: [williamsotomartinez@gmail.com](mailto:williamsotomartinez@gmail.com)
Author Affiliation: [SyNaLP](https://synalp.loria.fr/)([LORIA](https://www.loria.fr/en/))

## What type of a transformation is this?
This transformation is a simple substitution of groups of words for their acronyms. It helps to increase the size of the dataset as well as improving the understanding of acronyms of models trained on data augmented with this transformation.

## What tasks does it intend to benefit?
This transformations works to increase the data for any task that has input texts. It is specially interesting for tasks on semantic similarity, where models should be aware of the equivalence between a set of words and their acronym.

## What are the limitations of this transformation?
The quality of the transformation depends on the list of acronyms. As of now, this list was scraped from wikipedia's List of Acronyms and naively filtered, which leaves space for improvement .

## Robustness Evaluation
| Transformation                   | roberta-base-SST-2   | bert-base-uncased-QQP   | roberta-large-mnli   | roberta-base-imdb   |
|:---------------------------------|:---------------------|:------------------------|:---------------------|:--------------------|
| UseAcronyms                      | 94.0->94.0 (  0.0)   | 92.0->91.0 ( -1.0)      | 91.0->91.0 (  0.0)   | 95.0->95.0 (  0.0)  |

## Data
The list of acronyms in acronyms.tsv was scrapped from Wikipedia's [Lists of Acronyms](https://en.wikipedia.org/wiki/Lists_of_acronyms), a quick verification of the content was manually done but it was not exhaustive.