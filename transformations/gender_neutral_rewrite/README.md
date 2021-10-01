# Gender Neutral Rewrite
Author name: Tony Sun
Author email: thetonysun@gmail.com
Author Affiliation: UC Santa Barbara / Google

## What type of a transformation is this?
This transformation involves rewriting a gendered sentence in English with its gender-neutral variant. For example, the 
sentence "His dream is to be a fireman when he grows up" can be rewritten as "Their dream is to be a firefighter when 
they grow up."

## Why is this transformation important?
Responsible development of technology involves applications being inclusive of the diverse set of users they hope to 
support. An important part of this is understanding the many ways to refer to a person and being able to fluently change 
between the different forms as needed.

## What tasks does it intend to benefit?
We see many applications of a model which can understand different reference forms and fluently move between them. 
<ol>
<li>One obvious application is machine translation (MT), when translating from a language with gender-neutral pronouns (e.g. 
Turkish) to a language with gendered pronouns (e.g. English). In this setting, many definitions of the MT task require a 
system to decide whether to use a he-pronoun or a she-pronoun in the English translation, even though this is not 
expressed in the source. If there is no disambiguating information available, providing multiple alternatives 
(Kuczmarski and Johnson, 2018) with a genderneutral translation might be more appropriate. </li>
<li>A model trained for this task 
could also be useful for augmented writing tools which provide suggestions to authors as they write, e.g. to reduce 
unintended targeting in job listings. </li>
<li>Finally, given the efficacy of data augmentation techniques for improving model 
robustness (Dixon et al., 2018), we anticipate the sentences our re-writer produces would be useful input for models.
</li>
</ol>

## Previous Work
1) Gender Neutral Rewrite implementation borrowed from this [code](xhttps://github.com/googleinterns/tony-sun-intern-project)

2) Slides for Gender Neutral Rewrite can be found [here](https://docs.google.com/presentation/d/12kQn7YT8sxoYSTktcy-NWiVejJbQ0aaigfGMxxXkW_A/edit?usp=sharing)

3) Gender Neutral Rewrite is based on this [paper](https://arxiv.org/abs/2102.06788) from WeCNLP 2020:
```bibtex
@article{DBLP:journals/corr/abs-2102-06788,
  author    = {Tony Sun and
               Kellie Webster and
               Apurva Shah and
               William Yang Wang and
               Melvin Johnson},
  title     = {They, Them, Theirs: Rewriting with Gender-Neutral English},
  journal   = {CoRR},
  volume    = {abs/2102.06788},
  year      = {2021},
  url       = {https://arxiv.org/abs/2102.06788},
  archivePrefix = {arXiv},
  eprint    = {2102.06788},
  timestamp = {Thu, 18 Feb 2021 15:26:00 +0100},
  biburl    = {https://dblp.org/rec/journals/corr/abs-2102-06788.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```

## What are the challenges of this transformation?
One idea to rewrite gendered sentences in English to its gender-neutral
variant is to use a simple rule-based method,
mapping certain gendered words to their genderneutral variants. This is a tempting solution, since
the pronouns “she” and “he” can always be rewritten as “they.” In fact, we can even extend this
idea to words such as “fireman” and “spokesman,”
which can be mapped to their gender-neutral counterparts “firefighter” and “spokesperson,” respectively.

However, the simple find-and-replace approach
struggles with two types of situations: (1) pronouns with one-to-many mappings and (2) identifying and rewriting verbs. In the former situation,
some pronouns can be rewritten differently depending on the context of the sentence. To give
an example, the pronoun “her” can map to either “their” or “them” depending on its usage.
In the sentence “This is her pen,” “her” should
be rewritten as “their,” but in the sentence “This
pen belongs to her,” “her” should be rewritten as
“them.” Other examples of this one-to-many mapping include “his” &#8594; “their / theirs” and “(s)he’s”
&#8594; “they’re / they’ve.”

Another challenge that the rule-based method
needs to address is how to identify and rewrite the
appropriate verbs. From the example "His dream is to be a fireman when he grows up", the verb “is” remains the same while the verb
“grows” is rewritten as “grow.” The insight is that
verbs that correspond to a non-gendered subject
verbs that correspond to a non-gendered subject
should remain the same and verbs that correspond
to either “she” or “he” as the subject should be
rewritten. Doing this with a list of rules might be
feasible, but would likely require a large set of
handcrafted features that could be expensive to
create and maintain.

## Our Rewriting Algorithm
Our rewriting algorithm is composed of three
main components: regular expressions, a dependency parser, and a language model.

Regular expressions are responsible for finding and replacing certain tokens regardless of
the context. Similar to the aforementioned rulebased approach, we always rewrite “(s)he” to be
“they” and certain stereotypically gendered words
to their gender-neutral counterparts.

We use SpaCy’s (Honnibal and Montani, 2017)
dependency parser for building a parse tree of the
input sentence. Using the parse tree, we tag verbs
that correspond to “(s)he” as their subject and convert them to their third-person plural conjugation
using a list of rules. Verbs that correspond to a
non-gendered subject remain the same.

Finally, we use the pre-trained GPT-2 language
model (Radford et al., 2019) to resolve pronouns
with one-to-many mappings. Given a sentence
with such a pronoun, we would generate all possible variants by substituting each gender-neutral
variant. Then, we rank the perplexity of each
sentence and choose the sentence with the lowest
perplexity as the gender-neutral variant.

## Results

Impressively, the algorithm is able to achieve over 99 BLEU and less than 1% word
error rate on a diverse test set of 500 manually annotated sentence-pairs. Source sentences, which are gendered, in the test set are
taken equally from five diverse domains: Twitter,
Reddit, news articles, movie quotes, and jokes.

## What are the limitations of this transformation?
The rewriting algorithm is not perfect. Occasionally, it can incorrectly resolve pronouns that have one-to-many mappings 
incorrectly, such as "her" &#8594; "their / them". It can also sometimes struggle when multiple verbs correspond to a 
single subject. For example, the sentence "She sings in the shower and dances in the dark" is rewritten as They sing in the shower and
**dances** in the dark. 