# German Gender Swap 🦎  + ⌨️ → 🐍
This transformation replaces the masculine nouns and pronouns with their female counterparts for German language.

Author: A.T. (atabassum.bee15seecs@seecs.edu.pk)
Affiliation: --


## What type of a transformation is this?
This transformation will swap the 186 male nouns and pronouns and of input sentences with female nouns and pronouns. It mostly deals with nominative cases, with a few accase replacements. It also takes the most common top 1000 German male names[1] and if they are present in the input, they are  replaced with a random female name from  top 1000 German female names[2]. 

Input --> Output
Ich sehe den Mann -->Ich sehe die Frau
John ist hier →Sandy ist hier *
Er ist mein Vater →Sie ist meine Mutter
Der Ingenieur geht→Die Ingenieurin  geht
der Arzt behandelt ihn→die Arztin behandelt sie


*The female name is picked at random and will always be different.

## What tasks does it intend to benefit?
This transformation can benefit any task which wishes to generate more diverse feminine gendered data in German language, which can be useful in  bias exploration techniques.

## Data and code provenance
The 223 noun pairs are provided by the author, while the 2000 names are scraped from the web. The code is written by the author.

## What are the limitations of this transformation?
The transformation doesn’t consider some other cases like dative of German language, for now, doesn’t consider context sometimes and assumes that the nouns are capitalized.



## References:
[1]https://de.wiktionary.org/wiki/Verzeichnis:Deutsch/Namen/die_h%C3%A4ufigsten_m%C3%A4nnlichen_Vornamen_Deutschlands
[2]https://de.wiktionary.org/wiki/Verzeichnis:Deutsch/Namen/die_h%C3%A4ufigsten_weiblichen_Vornamen_Deutschlands

