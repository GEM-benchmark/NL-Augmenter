## Factive and Non-Factive verbs Transformation 🦎  + ⌨️ → 🐍
This transformation adds noise to all types if text source (sentence, paragraph, etc.) by adding factive verbs based paraphrases <br>
Reference: http://www.lrec-conf.org/proceedings/lrec2012/pdf/757_Paper.pdf <br>
Example: `Peter published a research paper => Peter acknowledged that he published a research paper.`

+ Author name: Ashish Shrivastava
+ Author email: ashish3586@gmail.com
+ Author affiliation: Agara Labs

### What type of Transformation is this?
This transformation acts like a perturbation to test robustness. Generated transformations display high similarity to the source sentence's semantics. i.e. the code outputs highly precise 
generations.

### What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text generations, text classification etc.

### Data and Code Provenance
The files for simple and phrasal implicatives had been released in the following work.
```bibtex
@inproceedings{karttunen2012simple,
  title={Simple and phrasal implicatives},
  author={Karttunen, Lauri},
  booktitle={* SEM 2012: The First Joint Conference on Lexical and Computational Semantics--Volume 1: Proceedings of the main conference and the shared task, and Volume 2: Proceedings of the Sixth International Workshop on Semantic Evaluation (SemEval 2012)},
  pages={124--131},
  year={2012}
}
```

### What are the limitations of this transformation?
A rule-based transformation, could be slightly incorrect in grammar. (could act as additional noise in the transformation)

