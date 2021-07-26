## named-entity-count filter

Author: Vikas Raunak (viraunak@microsoft.com)

## What type of a filter is this?

This filter filters data where the number of Named Entities in the input match a specified threshold (based on the supported conditions).

Supported conditions:
- greater than: ">"
- less than: "<"
- greater equal to: ">="
- less equal to: "<="
- equal to: "=="

## Why is measuring performance on this split important?

Errors pertaining to Named Entities are quite common in a range of text generation systems (e.g. MT, Summarization, etc.). This filter will allow measuring performance on more fine-grained splits wrt Named Entities. Besides analysis, uses in error analysis could be devised, e.g. detecting whether inputs and targets have same entity counts, etc.

## Related Work

A number of works (e.g. comapre-mt [1]) analyze text generation model outputs with respect to different input complexity measures, such as length (implemented in the length filter), parse structure, etc.

[1] compare-mt, Neubig et al. NAACL 2019 Demo Paper.

## What are the limitations of this filter?

The limitations of this filter are the limitations of the Named Entity Recognizer used, i.e. the counts could be inaccurate due to NER errors.
