# Random Walk using Masked-Languange Modeling
This transformation performs a random walk on the original sentence by randomly masking a word and replacing it with a suggestion by the BERT languange model.

Author names:
 - Chandan Singh (chandan_singh@berkeley.edu, UC Berkeley)
 - Jamie Simon (james.simon@berkeley.edu, UC Berkeley)
 - Sajant Anand (sajant@berkeley.edu, UC Berkeley)
 - Roy Rinberg (royrinberg@gmail.com, Columbia University)

## Extras

This transformation requires the 'bert-large-cased' pretrained model (~1 GB) from the Hugging Face Transformers library. Provided that the library is installed, this model will be installed the first time this transformation is ran.

## What type of a transformation is this?
This transformation acts like a perturbation to test robustness and generate sentences with similar syntactic content. By randomly replacing words with their mostly likely replacements, as determined by a bidirectional model that incorporates context clues from prevous and later words, we hope to generate similar sentences that make grammatical sense. 

## How it works
At each step in the random walk, we randomly choose a word and replace it by the mask token recognized by BERT. Care is take to preserve punctuation where possible so that the generated sentence has the same punctuation as the original sentence. With a word masked, we run BERT on the sentence and perform a softmax on the output logits. Then we select the high probability replacement words for the masked token and use these to construct new sentences.

The differences between original and generated sentences are controlled by two class initialization parameters, `steps` and `k`.
 - `steps`: number of random walk steps to do
 - `k`: number of high probability replacements for the masked word to consider

This process generates $k^steps$ new sentences. We then randomly select a subset of these, as specified by `max_outputs`.

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, 
text generation, etc. 

```python evaluate.py -t ButterFingersPerturbation -task TEXT_CLASSIFICATION```
```model_name = "aychang/roberta-base-imdb"```
The accuracy of a RoBERTa model (fine-tuned on IMDB) (model: "aychang/roberta-base-imdb") 
on a subset of IMDB sentiment dataset = 95.74
The accuracy of the same model on the perturbed set = 88.26

The average bleu score of a distillbert model (fine-tuned on xsum) (model: "sshleifer/distilbart-xsum-12-6") 
on a subset (10%) of xsum test dataset = 14.9104
The average bleu score of same model on the pertubed set = 11.9221

## What are the limitations of this transformation?

This transformation can generate nonsensical words when the random walk has many steps (steps >~ number of words in sentence).

## References
1) Saketh Kotamraju, "How to use BERT from the Hugging face transformer library", https://towardsdatascience.com/how-to-use-bert-from-the-hugging-face-transformer-library-d373a22b0209

