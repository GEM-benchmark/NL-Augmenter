## unicode filter

## What type of a filter is this?

This filter filters examples which contain non-ascii characters.
Author: Jan Pfister

## Why is measuring performance on this split important?
This filter can be used to find datapoints containing non-ascii unicode characters. Filtering out and testing on examples containing these characters can provide feedback for improving models accordingly as most models are trained on plain English text mostly containing ascii characters. Sometimes non-ascii character are even explicitly stripped away.
The same applies for German models.

## What are the limitations of this filter?
It does not filter for specific non-ascii characters but only checks for the existence of any such character.
