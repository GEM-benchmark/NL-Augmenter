# Random Walk using Masked-Languange Modeling
This transformation performs a random walk on the original sentence by randomly masking a word and replacing it with a suggestion by the BERT languange model.

Author names:
        
 - Sajant Anand (sajant@berkeley.edu, UC Berkeley)
 - Roy Rinberg (royrinberg@gmail.com, Columbia University)
 - Jamie Simon (james.simon@berkeley.edu, UC Berkeley)
 - Chandan Singh (chandan_singh@berkeley.edu, UC Berkeley)

## Data and Code Provenance

This transformation requires the 'bert-large-cased' pretrained model (~1 GB) from the Hugging Face Transformers library and the 'all-mpnet-base-v2' pretrained model (~400 GB) from the Sentence Transformers library. Provided that the libraries are installed (as they should be from 'requirements.txt'), these models will be installed the first time this transformation is ran. Both libraries operates under the Apache 2.0 license. Additionally the Spacy library is necessary but is installed by default when using this benchmark.

## What type of a transformation is this?
This transformation acts like a perturbation to test robustness and generate sentences with similar syntactic content. By randomly replacing words with their mostly likely replacements, as determined by a bidirectional model that incorporates context clues from prevous and later words, we hope to generate similar sentences that make grammatical sense. We measure the similarity between the original and random-walked sentence by performing sentence embeddings and then calculate the cosine similarity bewteen the embedded vectors.

## How it works
At each step in the random walk, we randomly choose a word and replace it by the mask token recognized by BERT. Care is take to preserve punctuation where possible so that the generated sentence has the same punctuation as the original sentence. Additionally, we can exclude named entities found by the Spacy model from random selection for repalcement. With a word masked, we run BERT on the sentence and perform a softmax on the output logits. Then we select the high probability replacement words for the masked token and use these to construct new sentences. Note that BERT has a max input token length of 512, so for long inputs, we split the sentence into chunks less than 512 tokens.

The differences between original and generated sentences are generally controlled by two class initialization parameters, `steps` and `k`.
 - `steps`: number of random walk steps to do
 - `k`: number of high probability replacements for the masked word to consider

This process generates $k^steps$ new sentences. We then randomly select a subset of these, as specified by `max_outputs`.

The seed of the random generators (both from `numpy` and the `random` module) are set by the `seed` parameter in the class initializer. Choosing a fixed value will lead to reproducable results.

The sentence similarity is done by first mapping the original and random-walked sentence to 768-dimensional vectors using a pre-trained sentence transformer. We then calculate the cosine similarity. We note that generated sentences with low similarity to the original sentence will still typically make grammatical sense; the meaning of the sentence may not be close to the original however (e.g. change the verb 'love' to 'hate'). The class initialization function takes a parameter `sim_req` which is the minimum similarity score that a generated sentence must have to be considered valid.

Finally a boolean `names` specifies whether or not we replace named entities and a boolean `descending` controls the order of the most probable tokens for masked-word replacement.

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, text generation, etc. Evaluating the perturbation using Google Colab is currently in progress.

## Robustness Evaluation

This model was evaluated with the model aychang/roberta-base-imdb on the test[:20%] split of the imdb dataset. Note: due to the computational demands of this transformation and the lack of resources at our disposal (only GPU access is Colab), we evaluate the transformation with the following parameters:
 - `seed = 0`
 - `max_outputs = 1` : Produce a single sentence
 - `steps = 5` : Randomly select a word to replace 5 times
 - `k = 1`: Number of high probability replacements for the masked word to consider
 - `sim_req = 0` : Similarity requirement for generated sentences (long sentences tend to have low similarity
 - `named_entities = True` : Do not replace named entities
 - `descending = True` : Choose most probable replacements (we will rarely use `False`; we included it for kicks.)

Wall Time: 00:03:52 (DD:HH:MM)
Performance: Of 1000 original sentences, 985 successfully transformed and 15 unchanged (0.985 perturb rate). Accuracy: 96.0 -> 96.0

Performance is strongly affected by parameters `steps` and `k`, as larger values of each will lead to greater variation in generated sentences, at the expense of longer runtimes.

## What are the limitations of this transformation?

This transformation can generate nonsensical words when the random walk has many steps (steps >~ number of words in sentence).

## References
1) Saketh Kotamraju; "How to use BERT from the Hugging face transformer library"; https://towardsdatascience.com/how-to-use-bert-from-the-hugging-face-transformer-library-d373a22b0209

As far as we know, this type of transformation where words are randomly perturbed has not been studied in published literature. Random walks have been used to measure sentence similarity, e.g. the papers listed below.

2) Daniel Ramage, Anna N. Rafferty, and Christopher D. Manning; "Random Walks for Text Semantic Similarity"; https://nlp.stanford.edu/pubs/wordwalk-textgraphs09.pdf
3) Ahmed Hassan, Amjad Abu-Jbara, Wanchen Lu, and Dragomir Radev; "A Random Walk–Based Model for Identifying Semantic Orientation"; https://aclanthology.org/J14-3003.pdf
