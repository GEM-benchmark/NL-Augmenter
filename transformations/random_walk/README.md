# Random Walk using Masked-Languange Modeling
This transformation performs a random walk on the original sentence by randomly masking a word and replacing it with a suggestion by the BERT languange model.

Author names:
 - Chandan Singh (chandan_singh@berkeley.edu, UC Berkeley)
 - Jamie Simon (james.simon@berkeley.edu, UC Berkeley)
 - Sajant Anand (sajant@berkeley.edu, UC Berkeley)
 - Roy Rinberg (royrinberg@gmail.com, Columbia University)

## Extras

This transformation requires the 'bert-large-cased' pretrained model (~1 GB) from the Hugging Face Transformers library and the 'all-mpnet-base-v2' pretrained model (~400 GB) from the Sentence Transformers model. Provided that the libraries are installed (as they should be from 'requirements.txt'), these models will be installed the first time this transformation is ran.

## What type of a transformation is this?
This transformation acts like a perturbation to test robustness and generate sentences with similar syntactic content. By randomly replacing words with their mostly likely replacements, as determined by a bidirectional model that incorporates context clues from prevous and later words, we hope to generate similar sentences that make grammatical sense. We measure the similarity between the original and random-walked sentence by performing sentence embeddings and then calculate the cosine similarity bewteen the embedded vectors.

## How it works
At each step in the random walk, we randomly choose a word and replace it by the mask token recognized by BERT. Care is take to preserve punctuation where possible so that the generated sentence has the same punctuation as the original sentence. With a word masked, we run BERT on the sentence and perform a softmax on the output logits. Then we select the high probability replacement words for the masked token and use these to construct new sentences.

The differences between original and generated sentences are controlled by two class initialization parameters, `steps` and `k`.
 - `steps`: number of random walk steps to do
 - `k`: number of high probability replacements for the masked word to consider

This process generates $k^steps$ new sentences. We then randomly select a subset of these, as specified by `max_outputs`.

The seed of the random generators (both from 'numpy' and the 'random' module) are set by the 'seed' parameter in the class initializer. Choosing a fixed value will lead to reproducable results.

The sentence similarity is done by first mapping the original and random-walked sentence to 768-dimensional vectors using a pre-trained sentence transformer. We then calculate the cosine similarity. We note that generated sentences with low similarity to the original sentence will still typically make grammatical sense; the meaning of the sentence may not be close to the original however (e.g. change the verb 'love' to 'hate'). The class initialization function takes a parameter 'sim_req' which is the minimum similarity score that a generated sentence must have to be considered valid.

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, 
text generation, etc. Evaluating the perturbation using Google Colab is currently in progress.

## What are the limitations of this transformation?

This transformation can generate nonsensical words when the random walk has many steps (steps >~ number of words in sentence).

## References
1) Saketh Kotamraju, "How to use BERT from the Hugging face transformer library", https://towardsdatascience.com/how-to-use-bert-from-the-hugging-face-transformer-library-d373a22b0209

