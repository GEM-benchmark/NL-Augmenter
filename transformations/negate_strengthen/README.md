# Causal Negation & Strengthen 🦎  + ⌨️ → 🐍
This transformation is targetted at augmenting Causal Relations in text and adapts the code from paper ['Causal Augmentation for Causal Sentence Classification'](https://openreview.net/pdf/17eafef9e25b48eb90a9a7f32c4f52e21177cc73.pdf) (Anon, 2021). In a nutshell, we have two operations:
1. **Causal Negation:** We introduce negative words like "not, no, did not" into sentences to unlink the causal relation. 
2. **Causal Strengthening:** We strengthen the causal meaning by converting weaker modal words like "may" to "will" to assert causal strength.

Users have the option to amend causal meaning automatically from root word of sentence, or by explicitly highlighting the index of the word they wish to amend. Additionally, we include WordNet synonyms and tense matching to allow for more natural augmentations.

##### Example Negation:
``` 
"TyG is effective to identify individuals at risk for NAFLD." | "Direct Causal"
--> "TyG is ineffective to identify individuals at risk for NAFLD." | "No Relationship"
```

##### Example Strengthen:
```
"Moreover, TT genotype may reduce the risk of CAD in diabetic patients." | "Conditional Causal"
--> "Moreover, TT genotype will reduce the risk of CAD in diabetic patients." | "Direct Causal"
```

Original test sentences are based on corpus [AltLex (Hidey et al, 2016)](https://github.com/chridey/altlex) and [PubMed by (Yu et al, 2019)](https://github.com/junwang4/causal-language-use-in-science). More expected examples and output grouped by grammar method is available in the Appendix of the [aforementioned code paper](https://openreview.net/pdf/17eafef9e25b48eb90a9a7f32c4f52e21177cc73.pdf).

Note: This augment may work for general relations too (shown below), but is not properly investigated. Longer sentences might result in unnatural edits.
```
"She is related to John" | "Direct Relation" 
--> "She is not related to John." | "No Relationship"
```

In summary, the current available transformation of targets are 
* "Direct Causal" -> "No Relationship"
* "Conditional Causal" -> "Direct Causal"
* "Direct Relation" -> "No Relationship"

**Author name:** Fiona Anting Tan <br>
**Author email:** tan.f@u.nus.edu <br>
**Author Affiliation:** Institute of Data Science, National University of Singapore

## What type of a transformation is this?
This transformation acts like a perturbation to test robustness. Root word or signal word of a sentence is highlighted for negation or strengthening via insert/replace operations Generated transformations display high similarity to the source sentences i.e. the code outputs highly precise generations. 

## What tasks does it intend to benefit?
This perturbation would benefit tasks which have a cause-effect sentence/paragraph/document as input like text classification, text generation, etc. In the main paper, the authors report improved performance and generalisability to out-of-domain contexts across models.

## Previous Work
This work is predominantly inspired by the aforementioned paper, ['Causal Augmentation for Causal Sentence Classification'](https://openreview.net/pdf/17eafef9e25b48eb90a9a7f32c4f52e21177cc73.pdf) (Anon, 2021), which is related to previous work ['Evaluating Models' Local Decision Boundaries via Contrast Sets'](https://arxiv.org/abs/2004.02709) by Gardner et al., 2020.

## What are the limitations of this transformation?
The transformation's outputs do not apply for all sentence structures as they are based on grammar rules and pattern matching. Outputs are also not linguistically diverse like paraphrasers.
