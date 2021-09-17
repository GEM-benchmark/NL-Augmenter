# Contextual Meaning Perturbation🦎  + ☎️️ → 🐍
This transformation changes the meaning of the sentence while avoiding grammar, spelling and logical mistakes.

*Author:
Hanna Behnke, Imperial College London
(hanna.behnke20@imperial.ac.uk)*

## What type of a transformation is this?
This transformation's effect is comparable to the <i>"Chinese Whispers"</i> or <i>"Telephone"</i> children's game: The transformed sentence
appears fluent and somewhat logical, but the meaning of the original sentence is not preserved.
To achieve logical coherence, a pre-trained language model is used to replace words with alternatives that match the context of the sentence.
Grammar mistakes are reduced by limiting the type of words considered for changes (based on POS tagging) and replacing adjectives with adjectives,
nouns with nouns, etc. where possible.


## What tasks does it intend to benefit?
This transformation benefits users who seek perturbations that preserve fluency but not the meaning of the sentence.
For instance, it can be used in scenarios where the meaning is relevant to the task, but the model shows a tendency
to over-rely on simpler features such as the grammatical correctness and general coherence of the sentence.
A real-world example would be the training of quality estimation models for machine translation
(does the translation maintain the meaning of the source?) or for text summarisation (does the summary capture the content of the source?).


## What kind of configurations are tweakable?
- <b>pos_to_change</b>: Determines which tokens are eligible for change based on the part of speech – default: ['ADV','ADJ', 'VERB', 'NOUN', 'PROPN']
- <b>perturbation_rate</b>: The percentage of eligible tokens that should be changed – default: 0.3
- <b>language</b>: Currently supported languages include English (en) and German (de) – default: "en"
- <b>top_k</b>: Determines how many replacement candidates should be proposed – default: 10

With the pre-configured settings, the risk of introducing small grammar mistakes
is about 5% for English and about 10% for German data for sentences of average length. The meaning of the original sentence is preserved in <1% of the cases (as intended).
Lowering the perturbation rate increases the risk of paraphrasing the sentences without changing their meaning.


## Previous Work
Word substitution with pre-trained language models has been explored in different settings. For example, the augmentation
library [nlpaug](https://github.com/makcedward/nlpaug "nlpaug") and the adversarial attack library
[TextAttack](https://github.com/QData/TextAttack "TextAttack") include contextual perturbation methods.
However, their implementations do not offer control over the type of words that should be perturbed and introduce
a large number of grammar mistakes. If the aim is to change the sentence's meaning while preserving its fluency,
this transformation can help to get the same effect with significantly fewer grammatical errors. Li et al. (2021) propose an alternative approach to achieve a similar objective in their paper
"Contextualized Perturbation for Textual Adversarial Attack".


## What are the limitations of this transformation?
Without using an additional grammar correction tool, it is difficult to avoid grammar mistakes completely.
Since this transformation requires the use of a pre-trained language model (via HuggingFace), it is comparatively heavy-weighted.
