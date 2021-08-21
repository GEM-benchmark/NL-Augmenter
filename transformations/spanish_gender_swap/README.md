# Spanish Gender Swap ♂️ → ♀️
This transformation changes the gender of all animate entities (mostly referring to people, and some animals) in a given Spanish sentence from masculine to feminine. This includes masculine nouns with feminine equivalents (e.g., *doctor* → *doctora* ), nouns with a common gender ("sustantivos comunes en cuanto al género", e.g., *el violinista* → *la violinista*), personal pronouns, and (optionally) given names often used with a given gender (e.g., *Pedro* → *Alicia*). Epicene nouns are excluded. In addition, the gender of adjectives, determiners, pronouns and participles are modified in order to maintain grammatical agreement.

Author: Juan Diego Rodriguez (juand-r@utexas.edu) <br>  Affiliation: UT Austin

**NOTE: given names swapping is not implemented yet, but will be there soon.**

## What does this transformation do?
All masculine nouns, pronouns and (optionally) given names are swapped from masculine to feminine. Then the gender of any adjectives, determiners, pronouns and participles associated with the gender-swapped nouns are changed as well. This was done using a gazeteer, a list of adjective modification rules, and *spacy*'s dependency parser and POS tagger.

## Why is this transformation important?
Gender stereotypes in natural language can be replicated or amplified by NLP systems. Much work so far has focused on mitigating this problem for English, but gender stereotypes are present in other langauges such as Spanish. For example, *engineer* is more likely to be translated as *ingeniero*, and *nurse* is more likely to be translated as *enfermera* (Stanovsky et al., 2019; Zhou et al., 2019; Zmigrod et al., 2019). In addition to being widely spoken, Spanish is also interesting because all Spanish nouns -- and many words associated with them -- have grammatical gender. There is an existing "Gender swap" transformation, but it only targets English.

## What tasks does it intend to benefit?
This transformation could be used to:
- create feminine-only versions of evaluation datasets for wide variety of tasks, in order to explore the gender bias of existing models. 
- augment training data with more gender diversity.

One advantage of changing every animate entity from masculine to feminine (rather than selectively changing only a few), is that one does not need to worry about possible co-reference errors when applying this transformation to text-to-text tasks such as summarization.

## Data and code provenance
We wrote the code for this transformation. The list of nouns to be changed was obtained from the following sources:
- a couple hundred masculine/feminine word pairs from (Zmigrod et al., 2019), available at https://github.com/rycolab/biasCDA/blob/master/animacy/spanish.tsv, with a few small corrections
- a list of demonym pairs from https://www.rae.es/dpd/ayuda/paises-y-capitales-con-sus-gentilicios (*Diccionario panhispánico de dudas*)
- an extensive list of Spanish nouns with feminine equivalents from Wiktionary (https://en.wiktionary.org/)
- a selection of anglicisms (e.g., *teen*, *ranger*, *troleador*) from (Moreno-Fernández, F. 2018a), available at https://cervantesobservatorio.fas.harvard.edu/sites/default/files/diccionario_anglicismos.pdf
- a list of nouns with a common gender ("sustantivos comunes en cuanto al género") from the following sources:
  - https://www.rae.es/dpd/g%C3%A9nero (*Diccionario panhispánico de dudas*)
  - over 1000 nouns ending in *-nte* or *-ista*. These were extracted from a list of fasttext word vectors trained on Common Crawl and Wikipedia, obtained from  https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.es.300.bin.gz (these can be extracted using the function *get_words* in the Python binding of the fastText library at https://github.com/facebookresearch/fastText)
- a list of frequently used diminutive forms (e.g., *abuelito*, *perrito*) and augmentative forms (e.g., *cabezón*, *jefazo*)

## What are the limitations of this transformation?

This transformation currently has a few limitations:

- Gender swapping of clitic pronouns (lo(s), la(s), le(s), and enclitic pronouns) is not implemented. Doing this would require co-reference resolution in many cases.
- Gender won't be swapped in cases where the pronoun is implicit (e.g., *Está cansado*, *Estamos encerrados en nuestro apartamento.*) or where the subject is implicit (e.g., *Sólo algunos conocen eso.* ["Only some know that."]). Many of these cases are hard to determine without further context.
- In Spanish, masculine nouns are used to designate groups of people of any gender (e.g., *los franceses* for all French people). Similarly, masculine nouns are used for generics (i.e., when referring to a general category as in the sentence *Los osos comen miel.* ["Bears eat honey"]; for more on this see (Gelman et al., 2016)). In these cases one likely wouldn't want to swap the gender, but there is no easy way to prevent this. Detecting Spanish generics (in sentences without context) would be very difficult, if not impossible, because unlike in English they need to be preceded by a determiner.
- There are other situations where a gender change would result in anomalous language. For example: `Los reyes y reinas` -> `Las reinas y reinas` ["The kings and queens" -> "The queens and queens"].
- Part-of-speech or dependency parse errors could lead to incorrect gender swaps or to gender-modifiable sentences that are not modified (e.g., *viejo* as used in "Ese viejo me debe dinero" is currently incorrectly tagged as an adjective, resulting in no change in gender).

We also limited the gender swaps to be from masculine to femenine:

- Various non-binary pronouns have been proposed (e.g., elle, ell@). Our transformation only swaps from masculine to feminine, since these are the grammatical gender categories for Spanish.
- Feminine to masculine gender swapping is not considered. A number of complications would arise if swapping from feminine to masculine: (1) there would be a greater amount of polysemy (e.g., swapping the gender of words such as *física*, *música*, *curiosa*, *pata*, or *bosnia* would lead to mistakes in many contexts), (2) the rules for swapping the gender of adjectives would not be straightforward for adjectives which already end in *a* for the masculine form (e.g., *agrícola*, *belga*), and (3) great care would need to be taken for words such as *ninguna* and *alguna*, which have two masculine equivalents which are used in different contexts (*ninguno*/*ningún*, and *alguno*/*ningún*, respectively).
- In addition, we don't selectively swap only certain nouns and not others -- doing so would likely introduce more grammatical agreement errors, and one advantage of swapping all gender-bearing nouns is that less mistakes are likely to be made when applying the transformation for text-to-text tasks. Future work could consider extending this transformation in these ways.

## Previous Work

```bibtex
@article{savoldi2021gender,
  title={Gender bias in machine translation},
  author={Savoldi, Beatrice and Gaido, Marco and Bentivogli, Luisa and Negri, Matteo and Turchi, Marco},
  journal={arXiv preprint arXiv:2104.06001},
  year={2021}
}
```

```bibtex
@inproceedings{stanovsky2019evaluating,
  title={Evaluating Gender Bias in Machine Translation},
  author={Stanovsky, Gabriel and Smith, Noah A and Zettlemoyer, Luke},
  booktitle={Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics},
  pages={1679--1684},
  year={2019}
}
```

```bibtex
@inproceedings{zmigrod2019counterfactual,
  title={Counterfactual Data Augmentation for Mitigating Gender Stereotypes in Languages with Rich Morphology},
  author={Zmigrod, Ran and Mielke, Sabrina J and Wallach, Hanna and Cotterell, Ryan},
  booktitle={Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics},
  pages={1651--1661},
  year={2019}
}
```

```bibtex
@inproceedings{zhou2019examining,
  title={Examining Gender Bias in Languages with Grammatical Gender},
  author={Zhou, Pei and Shi, Weijia and Zhao, Jieyu and Huang, Kuan-Hao and Chen, Muhao and Cotterell, Ryan and Chang, Kai-Wei},
  booktitle={Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)},
  pages={5276--5284},
  year={2019}
}
```

## Further References

[1] Gelman, S. A., Tapia, I. S., & Leslie, S. J. (2016). Memory for generic and quantified sentences in Spanish-speaking children and adults. Journal of Child Language, 43(6), 1231-1244.

[2] Moreno-Fernández, F. 2018a. Diccionario de anglicismos del español estadounidense (DAEE). Boston: Instituto Cervantes at Harvard University. Available online at https://cervantesobservatorio.fas.harvard.edu/sites/default/files/diccionario_anglicismos.pdf

[3] Real Academia Española y Asociación de Academias de la Lengua Española, Diccionario panhispánico de dudas, Madrid: Santillana, 2005. Available online at https://www.rae.es/dpd
