# Butter Fingers Perturbation 🦎  + ⌨️ → 🐍
This perturbation removes the possible adjuncts from a sentence and generates new sentences, which convey the same general meaning as the original sentence.

Author name: Ishan Jindal
Author email: ishan.jindal@ibm.com
Author Affiliation: IBM Research

## What type of a transformation is this?
Semantic role labeling (SRL) identifies the predicate-argument structure in a given sentence and represents the semantic meaning of the sentence. 
Given a sentence, SRL first recognizes a set of actions and then their corresponding arguments (Core and Contextual arguments). 
Core arguments identify Who did what to whom, whereas Contextual arguments identify How, Where, When, etc. of an action.
The Core arguments generally explain the general meaning of the sentence. On the other hand, contextual arguments
provide more specific information about an action. This specific information can be used in multiple ways, such as: 
Used to generate adversarial examples for a text classification task. To understand if the sentiment classification model is biased towards some entities in the sentences.
Similarly, This technique generates certain examples by removing these entities from a sentence, and one can expect to observe the same label for the sentence. 

## What tasks does it intend to benefit?
This perturbation would largely benefit textual entailment task where given a sentence pair:
- S1:`Two women are wandering along the shore drinking iced tea.`
- S2:`Two women are sitting on a blanket near some rocks talking about politics.`
- label: `Contradiction`

This transformation is applied to hypothesis and removes all the contextual information. That is the transformed sentence 
won't be a paraphrase instead implied. Transformation leads to:
- S1:`Two women are wandering along the shore drinking iced tea.`
- S2:`Two women are sitting on a blanket near some rocks talking about politics.`
- label: `Contradiction`

Further, this perturbation can benefit other tasks which have a sentence/paragraph/document as input like text classification, 
text generation, etc. 
This perturbation keeps the sentence structure intact and conveys the general meaning of the sentence. 

## Previous Work
1) This work use State-of-the-art semantic role labelers such as:
```

@article{jindal2020improved,
  title={Improved Semantic Role Labeling using Parameterized Neighborhood Memory Adaptation},
  author={Jindal, Ishan and Aharonov, Ranit and Brahma, Siddhartha and Zhu, Huaiyu and Li, Yunyao},
  journal={arXiv preprint arXiv:2011.14459},
  year={2020}
}

@article{shi2019simple,
  title={Simple bert models for relation extraction and semantic role labeling},
  author={Shi, Peng and Lin, Jimmy},
  journal={arXiv preprint arXiv:1904.05255},
  year={2019}
}


```
## What are the limitations of this transformation?
The augmented set may not be be helpful for the question-answering(QA) task as it removes specific information from the task.
