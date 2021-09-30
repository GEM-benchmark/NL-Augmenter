# German Gender Swap 🦎  + ⌨️ → 🐍
This transformation replaces the masculine nouns and pronouns with their female counterparts for German language.

Author: A.T. (atabassum.bee15seecs@seecs.edu.pk)


Affiliation: --


## What type of a transformation is this?
This transformation will swap the 226 male nouns and pronouns and of input sentences with female nouns and pronouns. It mostly deals with nominative singular  cases, and some accusative ones. It also takes the most common top 1000 German male names[1] and if they are present in the input, they are  replaced with a random female name from  top 1000 German female names[2]. 


|         Input                                            |                  Output                                 |
| -------------------------------------------------------- | ------------------------------------------------------- |
|                                                          |                                                         |
| Ich sehe den Mann                                        | Ich sehe die Frau                                       |
|                                                          |                                                         |
| John ist hier                                            | Sandy ist hier *                                        |
|                                                          |                                                         |
| Ich sehe, dass der Dichter und die Schauspielerin        | Ich sehe, dass die Dichterin und die Schauspielerin     |                     
|                                                          |                                                         |
 |  jetzt Freunde sind!                                     | jetzt Freunde sind!                                     |                     


 
*The female name is picked at random and will always be different.

## What tasks does it intend to benefit?
This transformation can benefit any task which wishes to generate more diverse feminine gendered data in German language, which can be useful in  bias exploration techniques.

## Data and code provenance
The 226 noun pairs are provided by the author, while the 2000 names are scraped from the web. The code is written by the author.

## What are the limitations of this transformation?
* This transformation does not replace words for cases other than nominative and possessive(the dative and genitive cases of German language).
* Some outputs may not make sense: 
“Dieser Mann hat mehr Testosteron als die Frau.” transforms into  “Diese Frau hat mehr Testosteron als die Frau." which is nonsensical
* It acts upon the singular formS of nouns only, not on their plural forms. It also does not act upon the interrogative forms of pronouns present in the sentence.

## References:
* [1]https://de.wiktionary.org/wiki/Verzeichnis:Deutsch/Namen/die_h%C3%A4ufigsten_m%C3%A4nnlichen_Vornamen_Deutschlands
* [2]https://de.wiktionary.org/wiki/Verzeichnis:Deutsch/Namen/die_h%C3%A4ufigsten_weiblichen_Vornamen_Deutschlands


