# Concatenate Two Random Sentences
This transformation concats two random sentences as explained in [Nguyen et al., 2021](https://arxiv.org/abs/2105.01691). This is the bilingual version. A monolingual version is available under concat monlingual.

## What type of a transformation is this?
This transformation creates longer data sequences.

## What tasks does it intend to benefit?
This concatenation would benefit all text tasks that use a transformer (and likely other sequence-to-sequence architectures). Previously published work has shown a large gain in performance of low-resource machine translation using this method. In particular, the learned model is stronger due to being able to see training data that has context diversity, length diversity, and (to a lesser extent) position shifting.  

## Previous Work and References
1) The transformation is from ["Data Augmentation by Concatenation for Low-Resource Translation: A Mystery and a Solution" (Nguyen et al., 2021)](https://arxiv.org/abs/2105.01691). 
```bibtex
@inproceedings{nguyen2021data,
  title={Data Augmentation by Concatenation for Low-Resource Translation: A Mystery and a Solution},
  author={Nguyen, Toan Q and Murray, Kenton and Chiang, David},
  booktitle = "Proceedings of the International Workshop on Spoken Language Translation",
  month = jul,
  year = "2021",
  address = "Online",
  publisher = "Association for Computational Linguistics",
  url = "https://arxiv.org/abs/2105.01691",
  abstract = "In this paper, we investigate the driving factors behind concatenation, a simple but effective data augmentation method for low-resource neural machine translation. Our experiments suggest that discourse context is unlikely the cause for the improvement of about +1 BLEU across four language pairs. Instead, we demonstrate that the improvement comes from three other factors unrelated to discourse: context diversity, length diversity, and (to a lesser extent) position shifting.",
}
```

## What are the limitations of this transformation?
The transformation has only appeared in publications in Low Resource Settings and for Machine Translation. It is unclear what the benefits will be in a higher resource settting or in a monolingual task.

## Robustness Evaluation 
Undefined task type, switching to default task %s TEXT_CLASSIFICATION
No default evaluation model exists for the interface <class 'interfaces.SentenceOperation.SentenceAndTargetOperation'> in the locale en.It's okay to skip the evaluation for the purpose of the PR. If you are interested to evaluate your perturbation on a task and a dataset, the right place to do it would to add a new class in the evaluation folder and call it from execute_model. That's it!
