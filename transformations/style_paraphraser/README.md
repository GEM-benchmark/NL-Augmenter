# Paraphrasing through the use of style transfer

This perturbation provides a range of possible styles of writing, enabling an easy use of style transfer paraphrase models originally introduced in the paper [Reformulating Unsupervised Style Transfer as Paraphrase Generation (2020)](https://aclanthology.org/2020.emnlp-main.55/) (K. Krishna et al.), published at EMNLP 2020.

Author name: Filip Cornell
Author email: c.filip.cornell@gmail.com
Author affiliation: KTH Royal Institute of Technology

## What type of a transformation is this?

This is a paraphraser that transfers between different styles. Several models are enabled and should be usable through this interface. This therefore provides an easy-to-use interface for these large paraphrasing models, giving often high-quality paraphrases.

The current styles of writing supporting are:

- Shakespeare - A Style transfer paraphraser paraphrasing as if Shakespeare would have written the sentence.
- Switchboard - A paraphraser trained on a collection of conversational speech transcripts.
- Tweets - A paraphraser trained on 5.2M English tweets.
- Bible - A paraphraser trained on texts from the Bible.
- Romantic poetry - A paraphraser trained on romantic poetry.
- Basic - A light, basic paraphraser with no specific style.

I will most likely add more pre-trained models as possibilities to use as I add more of the pre-trained models to Huggingface. For more information on these styles, please see the original paper: https://aclanthology.org/2020.emnlp-main.55/.

## What tasks does it intend to benefit?
Given the multiple different models enabled to be used easily through this interface (Basic, Bible, Shakespeare, Tweets, Switchboard and Romantic poetry), this can be used in a variety of cases. However, this can mainly work as an augmentation for improving sentence classification, perhaps from different domains. As shown by the Krishna K. et al. in their original paper, a diverse paraphrasing has the ability to normalize sentence by removing stylistic identifiers (see Figure 2 in the original paper: https://aclanthology.org/2020.emnlp-main.55/).

## Data and Code Provenance
This transformation makes use of code and pre-trained models from: https://github.com/martiansideofthemoon/style-transfer-paraphrase. This is therefore entirely based on the paper [Reformulating Unsupervised Style Transfer as Paraphrase Generation
](https://aclanthology.org/2020.emnlp-main.55/).

The license of the original code is included in the folder, and is an MIT License. Note that the author of this perturbation is not the author of the original code and paper, but has been in direct contact with the main author of the original paper.

## Reference to the original work

The bibtex-reference to the original work is:

```
@inproceedings{style20,
author={Kalpesh Krishna and John Wieting and Mohit Iyyer},
Booktitle = {Empirical Methods in Natural Language Processing},
Year = "2020",
Title={Reformulating Unsupervised Style Transfer as Paraphrase Generation},
}
```

## What are the limitations of this transformation?

This transformation is limited to different styles of writing in English. No other languages are supported. Furthermore, the paraphrasing takes place sentence by sentence in its current implementation, limiting the use of contextual information between the sentences. In other words, the style transfer of one sentence does not affect the style transfer of another.

Also note, that if long sentences are sent in, or two sentences in one, there is a risk sometimes that only a part will be paraphrased (see the example `"Hi there, how are you doing today? "` in the tests).

## Robustness evaluation

Running the evaluator yields:

```python3
python3 evaluate.py --transformation=StyleTransferParaphraser
Undefined task type, switching to default task %s TEXT_CLASSIFICATION
Some weights of the model checkpoint at filco306/gpt2-base-style-paraphraser were not used when initializing GPT2LMHeadModel: ['transformer.extra_embedding_project.bias', 'transformer.extra_embedding_project.weight']
- This IS expected if you are initializing GPT2LMHeadModel from the checkpoint of a model trained on another task or with another architecture (e.g. initializing a BertForSequenceClassification model from a BertForPreTraining model).
- This IS NOT expected if you are initializing GPT2LMHeadModel from the checkpoint of a model that you expect to be exactly identical (initializing a BertForSequenceClassification model from a BertForSequenceClassification model).
Loading <imdb> dataset to evaluate <aychang/roberta-base-imdb> model.
Reusing dataset imdb
Here is the performance of the model aychang/roberta-base-imdb on the test[:20%] split of the imdb dataset
The accuracy on this subset which has 1000 examples = 96.0
Applying transformation:
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1000/1000 [23:42<00:00,  1.42s/it]
Finished transformation! 1000 examples generated from 1000 original examples, with 1000 successfully transformed and 0 unchanged (1.0 perturb rate)
Here is the performance of the model on the transformed set
The accuracy on this subset which has 1000 examples = 96.0
```