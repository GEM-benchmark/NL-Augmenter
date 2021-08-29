# Homophonic word and sub-word transformations 🦎  + ⌨️ → 🐍
This transformation replaces words of a sentence with its homophonic replacements (could be a non english vocab word). <br><br> If the word is not found in homophones dataset this transformation breaks the word into two sub-words and generate homophone from sub-words. <br>
Ex: "Virat" => "Vi" + "rat" => "Voy" + "rat" => "Voyrat".
+ Author name: Suchitra Dubey
+ Author email: suchitra27288@gmail.com
+ Author affiliation: Acko

## What type of transformation is this?
This transformation acts like a perturbation to test robustness. <br>
Ex: "Virat Kohli made a big hundred against Australia ." --> "Voyrat kuwlYy meyd ey big hundr'd 'geynst 'streyly' ." 

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, 
text generation.