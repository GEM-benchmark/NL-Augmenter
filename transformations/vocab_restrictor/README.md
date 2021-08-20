# Vocabulary Restrictor
The vocabulary restrictor restricts words in a sentence to only those appearing in a given text.  If a word does not appear in the text, it is replaced with the semantically closest word according to the universal sentence encoder.  If the model does not recognize the word, it is replaced with the lexically closest.

The transformation comes equipped with the following books, taken from Project Gutenberg:
The Tempest, by William Shakespeare
Shakespeare's Sonnets, by William Shakespeare
The Communist Manifesto, by Karl Marx and Friedrich Engels
The Iliad, by Homer
Beowulf, Translated From The Heyne-Socin Text by Lesslie Hall
The Adventures of Tom Sawyer, by Mark Twain
The Medicinal Plants of the Philippines, by T. H. Pardo de Tavera
Alice’s Adventures in Wonderland, by Lewis Carroll
Celtic Fairy Tales, by Joseph Jacobs
Pride and Prejudice, by Jane Austen

More books can be included by adding a txt file to the books directory.

The transformation attempts to preserve the tense, part of speech, capitalization, and punctuation during transformation, and to preserve proper nouns, but mistakes are sometimes made, and the code comes without warranty.

Authors: McCullen Sandora and Tabitha Sugumar

## What type of a transformation is this?
This transformation takes a sentence (or snippet of text) and returns a list of sentences, each restricted to a book in the books directory.
Example: I'll teach you the electric slide! --> 
[I'll teach you the powerful tumble!,
 I'll teach you the powerful slide!,
 I'll educate you the electric slavish!,
 I'll teach you the powerful slide!,
 I'll learn you the powerful slay!,
 I'll teach you the electric landslide!,
 I'll learn you the fusible boussingault!,
 I'll teach you the energetic skim!,
 I'll teach you the powerful glide!,
 I'll teach you the powerful slack!]

## What tasks does it intend to benefit?
This can increase the number of training samples for a task, allow a model to learn synonomy, may be used to restrict text to/from a particular domain, and can act as a source of noise to regularize input text.  It can also be quite amusing sometimes, if you're in the right mood.

## What are the limitations of this transformation?
The transformation does not perfectly preserve meaning or grammar in all cases.  It also is not fast, taking ~ 6 seconds/book to initialize and ~ .2 seconds/book to execute for each sentence, depending on machine and input text.  Also, some books may contain potentially insensitive terms which can be substituted sometimes, so watch out.

## Data and Code Provenance
This transformation makes use of texts from Project Gutenberg, which contain the following license information:

  This eBook is for the use of anyone anywhere in the United States and
  most other parts of the world at no cost and with almost no
  restrictions whatsoever. You may copy it, give it away or re-use it
  under the terms of the Project Gutenberg License included with this
  eBook or online at www.gutenberg.org. If you are not located in the
  United States, you will have to check the laws of the country where
  you are located before using this eBook.
  
The code was written specifically for this project, and may be used and modified at will.