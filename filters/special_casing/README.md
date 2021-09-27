## Special Casing filter

## What type of a filter is this?

This filter checks if the input sentence has a special casing, i.e. the string is either all lowercased, all uppercased or has title casing.

Author: Vikas Raunak (viraunak@microsoft.com)

## Why is measuring performance on this split important?
Traditionally, neural models are trained without any explicit casing information provided to the tokenizer. The most widely used data-driven tokenization algorithms, such as sentencepiece (Unigram LM) or Byte-Pair-Encoding typically do not have any explicit factors to handle casing information. Therefore, tackling edge cases pertaining to case is important in text generation problems, e.g. in Machine Translation if a newspaper headline in title casing is provided to the model, the general expectation is that the output should preseve this title case. Same is true for inputs which are fully uppercased (typical in ALERT messages) or fully lowercased (typical in chat messages).

This filter can be used to create splits of specially cased sentences of 3 types, fully uppercased, fully lowercased or titlecased. Filtering out and testing on examples belonging to such special cased inputs can provide feedback for improving the model or guiding data augmentation accordingly.

## Related Work

The proposed filter is quite simple. Related work in handling cases explicitly in neural models includes the work on factored segmenter [1] and Truecasing [2].

[1] https://github.com/microsoft/factored-segmenter

[2] https://arxiv.org/abs/2108.11943v1

## What are the limitations of this filter?
Only three types of casing have been designated as special. I am not aware of other special casing types, but the proposed filter can be extended easily to increase coverage of such casing types.