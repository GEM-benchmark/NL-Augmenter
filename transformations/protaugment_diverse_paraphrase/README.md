# ProtAugment Diverse Paraphrasing

[![acl](http://img.shields.io/badge/ACL-2021-f31f32)](https://arxiv.org/abs/2105.12995)

This transformation method is from the paper **PROTAUGMENT: Unsupervised diverse short-texts paraphrasing for intent detection meta-learning**. The paraphrase generation model is a BART ([article](https://ai.facebook.com/research/publications/bart-denoising-sequence-to-sequence-pre-training-for-natural-language-generation-translation-and-comprehension/), [model](https://huggingface.co/facebook/bart-base)) model, trained on the paraphrase generation task using 3 datasets: Google-PAWS, MSR, Quora. The model is available on the 🤗 HuggingFace hub, named `tdopierre/ProtAugment-ParaphraseGenerator`.

## Methodology

Our parpahrasing method was used to enrich unlabeled data in a few-shot semi-supervised text classification task. We found out that the more diverse the generated paraphrases, the more it helped the downstream classification model!
 
When parpahrasing a sentence, we use Diverse Beam Search (DBS, [paper](https://arxiv.org/abs/161.02424)) to generate diverse outputs. The diversity penalty term is set to `0.5` but can be experimented with. 

Additionally, to generate even more diverse paraphrases, we introduce generation constraints:

- **Unigram**: a portion of the words in the input sentence are forbidden in the paraphrase. In the paper's experiments, we found the portion `p_mask=0.7` to be a good value. Again, this parameter can be changed if you want to increase or decrease the constraint
- **Bigram**: all bi-grams in the input sentence are forbidden in the paraphrase. This means the paraphrase cannot contain any bi-gram that are in the input sentence. This constraint enforces the paraphrase generation model to change the sentence structure

Those constraints are not performed at the same time. We did not yexperiment having both constraints at the same time yet.

## Reference

If you consider our augmentation method made of paraphrase generation, feel free to have a look at our complete paper and cite our work!

```bash
@article{Dopierre2021ProtAugmentUD,
  title={ProtAugment: Unsupervised diverse short-texts paraphrasing for intent detection meta-learning},
  author={Thomas Dopierre and C. Gravier and Wilfried Logerais},
  journal={ArXiv},
  year={2021},
  volume={abs/2105.12995}
}
```

If you have any questions or suggestions, contact the author, Thomas Dopierre (@tdopierre)
