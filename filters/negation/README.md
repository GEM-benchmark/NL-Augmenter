## Negation filter

Author: Ashish Shrivastava <br>
Email: ashish3586@gmail.com <br>
Affiliation: Agara Labs <br>

## What type of filter is this?
This filter filters examples contains negated words.

### Evaluation Results

Used default model and datasets <br>
model: `textattack/bert-base-uncased-QQP` <br>
split: `20%`  <br>
dataset: `qqp`

| Question type | Number of samples| Accuracy|
|--------------------|------|--------|
|All | 1000| 92.40|
|Negative | 54| 90.74|
|Non Negative|946| 92.49|


## Why is measuring performance on this split important? 
This filter can be used to separate out negated sentences, it will help to analyse models 
performance on negative sentences. This filter also captures negated words like (shoudnt, cant) 
which are not properly punctuated.

This filter can be used to separate out negated questions. Evaluation Results hint towards the 
fact that negated questions are more challenging hence measuring performance along this filter
is important  <br>

## What are the limitations of this filter?
This is a simple filter and separates out sentence based on lexical and context-free matching.
