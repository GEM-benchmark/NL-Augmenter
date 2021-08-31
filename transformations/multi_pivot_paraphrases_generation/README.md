# From one English Sentence to a list of paraphrases 🦎  + ⌨️ → 🐍
This transformation generates a list of paraphrases for an English sentence by leveraging Pivot-Transaltion approach.
Pivot-Transaltion is an approach where a sentence in a source language is translated to a foreign language called the pivot language then translated back to the source language to get a paraprhase candidate, e.g. translate an English sentence to French, then translate back to English.

The paraphrases generation is divided into two step:
- Step 1: paraphrases Candidate Over-generation by leveraging Pivot-Transaltion. At this step, we generate a Pool of possible parparhases.
- Step 2: apply a candidate selection over the Pool of paraphrases, since the pool can contain semantically unrelated or duplicate paraphrases.
    We leverage Embedding Model such as Universal Sentence Encoder~(USE) to disqualify candidate paraphrases from the pool, by computing the Cosine Similarity socres of the
    USE Embeddings between the reference sentence and the candidate paraphrase. Let R = USE_Embeding(reference_english_sentence) and P = USE_Embeding(candidate):
    - if Cosine(R,P) < alpha => the candidate is semantically unrelated and then removed from the final list of paraphrases
    - if Cosine(R,P) > beta => the candidate is a duplication and then removed from the final list of paraphrases
    - By default Alpha=0.5 and Beta=0.95, we set the value as suggested by [Parikh et al.](https://arxiv.org/pdf/2004.03484.pdf) works

Please refer to the test.json for all of the test cases catered.

This transformation translates an English sentence to a list of predefined languages using Huggingface MariamMT and EasyNMT as Machine Transaltion models.
- The transformation support Two Pivot-Transaltion Level.
    - If Pivot-level = 1 => Transalte to only one foreign language. e.g. English -> French -> English  ||  English -> Arabic -> English  ||  English -> japanese -> English
    - If Pivot-level = 2 => Transalte to only Two foreign language. e.g. English -> French -> Arabic -> English  ||  English -> Russian -> Chinese -> English

Author name: Auday Berro (audayberro@gmail.com)

## What type of a transformation is this?
This transformation is a paraphrase generation for Natural English Sentences by lveraging Pivot-Transaltion techniques. The Pivot-Trnasaltion technique allow to get lexically and syntaxically diverse paraphrases.

## What tasks does it intend to benefit?
This transformation would benefit all tasks with a sentence as input like question generation, sentence generation, etc.

## What are the limitations of this transformation?

1. The transformation does not generate paraphrases for non-English sentences, e.g. Can't generate paraphrases for German or Chinese sentences
 
2. This transformation only generate paraphrases for Natural Language English sentences.

## Previous Work


2) This work is partly inspired by the following work on robustness for Machine Translation:
```bibtex
@article{berroextensible,
  title={An Extensible and Reusable Pipeline for Automated Utterance Paraphrases},
  author={Berro, Auday and Zade, Mohammad-Ali Yaghub and Baez, Marcos and Benatallah, Boualem and Benabdeslem, Khalid}
}
```