## Quantitative question filter

## What type of a filter is this?

This filter is used to identify the quantitative questions
Evaluation Results

default model and datasets were used : `mrm8488/bert-tiny-5-finetuned-squadv2`, validation[:20%] split of the `squad`

| Question type | Number of samples| EM|
|--------------------|------|--------|
|All| 2114| 60.31|
| Quant | 230| 70.86|
|Non Quant|1884| 59.02|

Results hint towards the fact that non quantitative questions are more challenging hence measuring performance along this split is important  <br>

## Why is measuring performance on this split important?
This filter can be used to sepearte out quantiative questions, it helps to analyse models performance on questions which require numerical understanding.It is also usefull to study possible biases in question generation.

## Related Work

## What are the limitations of this filter?
This is a simple filter and separtes out questions based lexical and context-free matching
