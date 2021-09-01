# English Noun Compound Paraphraser [N+N]→ 🐍
This transformation replaces two-word noun compounds with a paraphrase, based
on the compound paraphrase dataset from SemEval 2013 Task 4 (Hendrickx et al., 2013).
This currently only works for English.

Author: Juan Diego Rodriguez (juand-r@utexas.edu) <br>  Affiliation: UT Austin

## What does this transformation do?
Any two-word compound that appears in a dataset of noun compound paraphrases
will be replaced by a paraphrase. If more than one two-word compound appears,
then all combinations of compound paraphrases (including no paraphrase at all)
will be returned. For example, the outputs of "After the bike ride, John stopped by the club house."
are:

```
['After the ride on a bike, John stopped by the club house.'],
'After the bike ride, John stopped by the house for club activities.',
'After the ride on a bike, John stopped by the house for club activities.']
```

The number of paraphrases to be returned for each noun compound is specified by the `max_paraphrases`
parameter (set to 1 by default). For example, the paraphrases of "club house"
include "house for club activities", "house for club members", "house in which a club meets", etc.

Currently this uses the dataset from SemEval 2013 Task 4 (Hendrickx et al., 2013),
which has a score for each paraphrase (frequency of annotation). We start with
replacing paraphrases with the highest score, and paraphrases with the same
score (ties) are sorted randomly.

## Why is this transformation important?
This transformation can be used to add diversity to a dataset by rewriting
noun compounds.

## What tasks does it intend to benefit?
This transformation could be used for any task, as a way to augment a dataset
by rewriting noun compounds as short phrases.

## Data and code provenance
We wrote the code for this transformation. The dictionary of noun compound
paraphrases is from SemEval 2013 Task 4 (Hendrickx et al., 2013). We used the
union of the trial (train) and test sets, but we made the following modifications:

- in cases where the same compound appeared in both the train and test set, we
added together their frequency in order to determine the overall paraphrase score.
- determiners at the beginning of the paraphrase were removed.

## What are the limitations of this transformation?

This transformation currently only checks for noun compounds from
(Hendrickx et al., 2013) and therefore has low coverage.
To improve it, other datasets could be added, e.g., from (Ponkiya et al., 2018)
or (Lauer, 1995). To attain even wider-coverage (at the expense of lower precision),
machine learning approaches such as (Shwartz and Dagan, 2018) or
(Ponkiya et al., 2020) could be considered.

In addition, some of the the paraphrases in (Hendrickx et al., 2013)
sound a little odd (e.g., "blood cell" -> "cell of blood") and may not fit
well in context.

Other oddities include:

- mistakes such as "I am an opera buff." -> "I am **an** buff of opera.",
- failure due to a literal interpretation of common metaphorical usage such as:
"Social workers face a mammoth task." -> "Social workers face a task which is performed by mammoth."
- unusual wording of extremely common compounds such as "stock market" -> "market for stock".
- too many prepositions resulting in confusing text, such as: "Yesterday's army coup by the opposition leader of the liberation struggle" -> "Yesterday's coup involving the army by the leader of the opposition of the struggle for liberation"

Also, future versions could include languages other than English.

**TODO:**

Plural or possessive forms of any noun compound may produce unusual or
incorrect results, such as "history books" -> "book about historys".

## Previous Work

```bibtex
@inproceedings{hendrickx2013semeval,
  title={SemEval-2013 Task 4: Free Paraphrases of Noun Compounds},
  author={Hendrickx, Iris and Kozareva, Zornitsa and Nakov, Preslav and S{\'e}aghdha, Diarmuid {\'O} and Szpakowicz, Stan and Veale, Tony},
  booktitle={Second Joint Conference on Lexical and Computational Semantics (* SEM), Volume 2: Proceedings of the Seventh International Workshop on Semantic Evaluation (SemEval 2013)},
  pages={138--143},
  year={2013}
}
```

```bibtex
@inproceedings{ponkiya2018treat,
  title={Treat us like the sequences we are: Prepositional Paraphrasing of Noun Compounds using LSTM},
  author={Ponkiya, Girishkumar and Patel, Kevin and Bhattacharyya, Pushpak and Palshikar, Girish},
  booktitle={Proceedings of the 27th International Conference on Computational Linguistics},
  pages={1827--1836},
  year={2018}
}
```

```bibtex
@inproceedings{ponkiya2020looking,
  title={Looking inside Noun Compounds: Unsupervised Prepositional and Free Paraphrasing using Language Models},
  author={Ponkiya, Girishkumar and Murthy, Rudra and Bhattacharyya, Pushpak and Palshikar, Girish},
  booktitle={Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing: Findings},
  pages={4313--4323},
  year={2020}
}
```

```bibtex
@inproceedings{shwartz2018paraphrase,
  title={Paraphrase to Explicate: Revealing Implicit Noun-Compound Relations},
  author={Shwartz, Vered and Dagan, Ido},
  booktitle={Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)},
  pages={1200--1211},
  year={2018}
}
```

```bibtex
@phdthesis{lauer1995designing,
  title={Designing Statistical Language Learners: Experiments on Noun Compounds},
  author={Lauer, Mark},
  year={1995},
}
```

