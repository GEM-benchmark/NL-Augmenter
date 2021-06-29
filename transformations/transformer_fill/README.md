# Transformer Fill

This perturbation replaces words based on recommendations from a Huggingface transformer model.

We can use a pre-trained transformer model to replace certain words and use the context of the sentence to guide the replacement. We allow users to pass in a set of POS tags (all enabled by default) by which to select replacement words. The transformer model can also be primed using the `context_text` parameter.

Author name: Gautier Dagan

## What type of a transformation is this?

This is a contextual augmentation. This transformation acts as a way to augment the text by changing certain words (according to their POS tag) and replacing `n` of them with words which are most likely under a chose Transformer model.

## What tasks does it intend to benefit?

This augmentation would benefit tasks in low-data settings and can help generalisation. It can also be used to created adversarial examples.

`python evaluate.py -t TransformerFill -task TEXT_CLASSIFICATION`
`model_name = "aychang/roberta-base-imdb"`

## Previous Work

1. While this code/implementation was written from scratch, I later found that it has some overlap with a previous blog post: https://www.depends-on-the-definition.com/data-augmentation-with-transformers/

2. Augmenting NLP data using Bert's Masked Language capabalities is not new. Multiple works have suggested doing so and showed that it can be used to augment low-resource settings (Wu et. al., 2018; Kumar et. al., 2020) and even create adversarial examples (Garg and Ramakrishnan, 2020).

```bibtex
@inproceedings{wu2019conditional,
  title={Conditional bert contextual augmentation},
  author={Wu, Xing and Lv, Shangwen and Zang, Liangjun and Han, Jizhong and Hu, Songlin},
  booktitle={International Conference on Computational Science},
  pages={84--95},
  year={2019},
  organization={Springer}
}
```

````bibtex
@article{kumar2020data,
  title={Data augmentation using pre-trained transformer models},
  author={Kumar, Varun and Choudhary, Ashutosh and Cho, Eunah},
  journal={arXiv preprint arXiv:2003.02245},
  year={2020}
}

```bibtex
@article{garg2020bae,
  title={Bae: Bert-based adversarial examples for text classification},
  author={Garg, Siddhant and Ramakrishnan, Goutham},
  journal={arXiv preprint arXiv:2004.01970},
  year={2020}
}
````

## What are the limitations of this transformation?

There are many limitations to such approach and any use of this augmentation will need to be carefully monitored and guided for the task at hand.

1. It is possible that the new augmented sentence has a different meaning from the original, since it is highly dependent on what words the model is asked to replace.

   For instance the sentence `"This is pretty cool"`. If you want choose to replace adjectives, you might end up asking the model to fill in the blank for the sentence: `"This is pretty <mask>"`. In which case it might decide that the most likely word would make: `"This is pretty bad"`.

   A way to alleviate this is to condition the augmentation or prime the model towards certain words. For instance, by prepending `"Positive review:"` to the aformentioned sentence, we are more likely to obtain predictions that will also align with the prompt or primer.

2. While this augmentation has the potential to help low-data regimes and models generalise more, **there is the risk of introducing or reinforcing additional biases** which may and likely do exist in the large masked language models.

Finally, the Huggingface tokenizer used might have an impact on the quality of the resulting augmentatation. For instance, the Roberta Tokenizer includes the spacing to the left of tokens, whereas the standard Bert implementation does not. This might occasionally introduce an extra spacings between words.
