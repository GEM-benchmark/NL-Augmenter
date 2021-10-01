# Sentence Additions 🦎  + ⌨️ → 🐍
This perturbation adds generated sentence to all types of text sources (sentence, paragraph, etc.) by passing the input text to a GPT-2 Text Generation model.

Author name: Timothy Sum Hon Mun (timothy22000@gmail.com)

## What type of a transformation is this?
This transformation will take in an input text and generate additional sentences to perturbe the inputs that have been shown by Jia and Liang, 2017 to impact model performance. This can be used to test model robustness.

The AddSent method in the paper which is in the Q&A setting requires mutation of the original question asked and generating a fake answer based on that. Then, converting them into a statement that is added a sentence to the input text as an adversarial example.

This transformation uses GPT-2 to generate new grammatical sentence that will be added to the input text so it does not require any question mutation and fake answer.

Run code below to evaluate:
```python evaluate.py -t ButterFingersPerturbation -task TEXT_CLASSIFICATION -m "textattack/roberta-base-SST-2" -d "sst2"```

Accuracy of a RoBERTa model tuned on SST-2 (model: "textattack/roberta-base-SST-2") on a subset of the SST-2 dataset = 95.74

Accuracy of the same model on the perturbed set = 89.0

## What tasks does it intend to benefit?
This perturbation would benefit all tasks on text classification and generation.

## Related work

This is inspired by ideas that are related to the AddSent and AddOneSent adversarial examples covered in this EMNLP 2017 paper:

```bibtex
@article{jia2017adversarial,
  title={Adversarial examples for evaluating reading comprehension systems},
  author={Jia, Robin and Liang, Percy},
  journal={arXiv preprint arXiv:1707.07328},
  year={2017}
}
}
```

The GPT-2 text generation model is from the following paper:

```bibtex
@article{radford2019language,
  title={Language Models are Unsupervised Multitask Learners},
  author={Radford, Alec and Wu, Jeff and Child, Rewon and Luan, David and Amodei, Dario and Sutskever, Ilya},
  year={2019}
}
```

We use its implementation from huggingface (https://huggingface.co/gpt2).

## What are the limitations of this transformation?

The text generated from this transformation is dependent on the pre-trained GPT-2 language model so it would perform less well on topics it has not seen. It is also less robust than the GPT-3 model which was trained on a much larger dataset and has more parameters.

