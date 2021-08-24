# Use Acronyms
This transformation changes groups of works for their equivalent acronyms.

Author name: William Soto
Author email: [williamsotomartinez@gmail.com](mailto:williamsotomartinez@gmail.com)
Author Affiliation: [SyNaLP](https://synalp.loria.fr/)([LORIA](https://www.loria.fr/en/))

## What type of a transformation is this?
This transformation is a simple substitution of grouops of words for their acronyms. It helps to increase the size of the dataset as well as improving the understanding of acronyms for models test on data augmented in this way.

## What tasks does it intend to benefit?
This transformations works to increase the data for any task that has input texts. It is specially interesting for tasks on semantic similarity, where models should be aware of the equivalence between a set of words and their acronym.

## What are the limitations of this transformation?
The quality of the transformation depends on the list of acronyms. As of no, this list was scraped from wikipedia's List of Acronyms and naively filtered, which leaves space for imporvement.