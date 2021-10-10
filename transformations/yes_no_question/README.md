# Yes-No Question Perturbation ✔️️ → ❓
This perturbation turns English statements into yes-or-no questions.

Author name: Connor Boyle
Author email: connor.bo@gmail.com
Author affiliation: University of Washington

## What type of a transformation is this?

This transformation turns English non-compound statements into yes-no
questions. The generated questions can be answered by the statements that were
used to generate them. The text is left largely unchanged other than the
fronted/modified/added auxiliaries and be-verbs.

The transformation works by getting dependency parse and POS tags from a
machine learning model and applying human-engineered, rule-based
transformations to those parses/tags.

## What tasks does it intend to benefit?

This transformation would particularly benefit question-answering and
question-generation tasks, as well as providing surplus legal text for language
modeling and masked language modeling.

### Evaluation: Text Classification

The model was evaluated on the `TEXT_CLASSIFICATION` task, using the `evaluate.py` script, with "percentage of
examples" (`-p` set to `20`):

| Model | Dataset | Perturb Rate | Original Performance | Transformation Performance |
|-------|---------|--------------|----------------------|----------------------------|
| textattack/roberta-base-imdb | imdb | 0.967 | 95.0 | 90.0 |
| roberta-large-mnli | multi_nli | 1.0 | 91.0 | 89.0 |
| textattack/bert-base-uncased-QQP | qqp | 1.0 | 92.0 | 91.0 |
| textattack/roberta-base-SST-2 | sst2 | 0.40804597701149425 | 94.0 | 94.0 |

## What are the limitations of this transformation?

More work needs to be done to ensure the generated questions are of reasonably
high quality. The transformation outputs an empty list for compound
sentences, exclamations, and other inappropriate inputs (which is desired
behavior), but still generates malformed output when the input is already a
question (e.g. `"Is my name Fred?" -> "Is my name my name Fred??"`). I am
looking for the cleanest/most robust way of checking whether a statement of
a question is.
