# Homophonic word and sub-word transformations 🦎  + ⌨️ → 🐍
This transformation replaces ~30% of words of a sentence with its homophonic replacements (could be a non english vocab word). <br><br> If the word is not found in homophones dataset this transformation breaks the word into two sub-words and generate homophone from sub-words. <br>
Ex: "Virat" => "Vi" + "rat" => "Voy" + "rat" => "Voyrat". <br>
+ Author name: Suchitra Dubey
+ Author email: suchitra27288@gmail.com
+ Author affiliation: Acko

## How to use this transformation?
This transformation is created for text classification and text to text generation task. you can use it in following ways: <br>
```python evaluate.py -t homophonic_transformation -task TEXT_CLASSIFICATION``` <br>
OR <br>
```python evaluate.py -t homophonic_transformation -task TEXT_TO_TEXT_GENERATION```
## What type of transformation is this?
This transformation acts like a perturbation to test robustness. <br>
Ex: "Virat Kohli made a big hundred against Australia ." --> "Voyrat Kohli made a big hundred 'geynst Australia ."" 

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, 
text generation.