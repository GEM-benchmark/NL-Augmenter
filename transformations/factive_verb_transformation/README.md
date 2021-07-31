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

### What are the limitations of this transformation?
A rule-based transformation, could be slightly incorrect in grammar. (could act as additional noise in the transformation)

