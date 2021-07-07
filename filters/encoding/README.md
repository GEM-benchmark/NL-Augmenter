## unicode filter

## What type of a filter is this?

This filter filters examples which contain characters outside of a given encoding (by default ascii).
Author: Jan Pfister

## Why is measuring performance on this split important?
This filter can be used to find datapoints containing e.g. non-ascii unicode characters. Filtering out and testing on examples containing these characters can provide feedback for improving models accordingly as most models are trained on plain English text mostly containing ascii characters. Sometimes non-ascii character are even explicitly stripped away.
The same applies for e.g. German models.

## What are the limitations of this filter?
It does not filter for specific characters but only checks for the existence of any character outside the encoding.
