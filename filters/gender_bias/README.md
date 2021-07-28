## gender bias filter

## What type of a filter is this?

This is a bilingual filter (for English and French languages), which filters a text corpus to measure gender fairness in regards of a female gender representation.
It is based on a pre-defined set words, such as personal pronouns, words defining the relation and titles, corresponding to the female and male genders accordingly.
Two utility methods - flag_sentences(), count_genders() and sort_groups() give supplementary information to the boolean value returned by the main filter() method.

Author: Anna Shvets
Company:
Fablab by Inetum in Paris
157 Boulevard MacDonald
75019 Paris
France


## Why is measuring performance on this split important?
This filter can be used to define whether the female gender is sufficiently represented in a tested subset of sentences.
Being currently implemented for English and French language, this filter is potentially language-agnostic, since does not rely on any external dependencies.

## Related Work
While the problematics of the gender fairness is an active domain of research in NLP, the current code represents an original implementation.

## Examples of use

```
f = GenderBiasFilter("en")
sentences = [ "He is going to make a cake.",
              "She is going to program",
              "Nobody likes washing dishes",
              "He agreed to help him" ]

f.filter(sentences)
```

The above statement returns True, as the number of sentences flagged as "masculine" is less than the number of sentences tagged as "feminine". 
You can check the exact number by calling the `count_genders()` static method on the instance of the class and providing it with the extracted flags with the `flag_sentences()` static method:
```
flagged_sentences = f.flag_sentences(sentences, "en")
feminine, masculine, neutral = f.count_genders(flagged_sentences)
print("Feminine flagged sentences:", feminine)
print("Masculine flagged sentences:", masculine)
print("Neutral flagged sentences:", neutral)
```

which outputs:
```
Feminine tagged sentences: 1
Masculine tagged sentences: 2
Neutral tagged sentences: 1
```
You can also retrieve the arrays of sentences from each group, by calling the `sort_groups()` method on the instance of th class, providing it with flags, extracted by `flag_sentences()` method:

```
flagged_sentences = f.flag_sentences(sentences, "en")
feminine_group, masculine_group, neutral_group = f.sort_groups(flagged_sentences)
print("This is a feminine group:", feminine_group)
print("This is a masculine group:", masculine_group)
print("This is a neutral group:", neutral_group)
```

which outputs:
```
This is a feminine group: ['She is going to program']
This is a masculine group: ['He is going to make a cake.', 'He agreed to help him']
This is a neutral group: ['Nobody likes washing dishes']
```
You are free to change the language at the class initialisation step:
```
sentences = [ "Il va preparer un gateau",
              "Elle va créer un logiciel",
              "Personne n'aime pas faire la vaiselle",
              "Maman va à la conférence" ]

f = GenderBiasFilter("fr")
f.filter(sentences)
```
## What are the limitations of this filter?
The filter result is based on n-gram intersection counting approach, which assumes that the word should have the exact form as the internally defined keywords.