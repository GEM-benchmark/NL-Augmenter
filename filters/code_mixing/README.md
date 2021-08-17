## Code-Mixing Filter

## What type of a filter is this?

This filter selects for code-mixed texts (i.e. texts using multiple 
languages in the same sentence).

### Evaluation Results



## Why is measuring performance on this split important?

It is useful for testing a model's performance on code-mixed/multilingual text,
which is used in life but may not be well-represented in training data.

## What are the limitations of this filter?

Language detection on its own is not a trivial problem, and this filter relies
on a necessarily imperfect model for the task at the token level. The line
between code-mixing and borrowing is not clear.

The filter is also limited to the 166 languages supported by [ftlid
](https://pypi.org/project/ftlid/).
