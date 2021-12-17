# Simple Ciphers

This transformation modifies the input text in ways that a human could rapidly (or with
  a few minutes of work in the case of rot13) decipher, but which make the
  input sequences almost completely unlike typical input sequences which are used
  during language model training.

Author name: Jascha Sohl-Dickstein\
Author email: jaschasd@google.com\
Author Affiliation: Google Brain

## What type of a transformation is this?

This transformation modifies text using a variety of very simple "ciphers", that make the input sequence very dissimilar at the token level from its original form, but without losing any information in the input sequence:
1. Repeat every character twice
```
TThhee  rreedd  ffooxx  jjuummppeedd  oovveerr  tthhee  llaazzyy  ddoogg..
```
3. Repeat every word twice
```
The The red red fox fox jumped jumped over over the the lazy lazy dog. dog.
```
5. Add spaces between all characters
```
T h e   r e d   f o x   j u m p e d   o v e r   t h e   l a z y   d o g .
```
6. Reverse all characters in the input string
```
.god yzal eht revo depmuj xof der ehT
```
7. Reverse the characters in each word in the input string
```
ehT der xof depmuj revo eht yzal .god
```
8. Reverse the order of words in the input string
```
dog. lazy the over jumped fox red The
```
9. Replace each character with a randomly chosen Unicode homoglyph
```
T𝗵𝙴 ꮢ𝑬𝙳 ẝ𝘖𝛸 𝗷𖽂𐌑𝚙Ꭼ𝚍 ੦Ｖ𝖤𝙧 𑢼ℋ𝜠 ⅬA𑣄𝑦 ᑯ𝟘𝖌．
```
10. Apply the [ROT13](https://en.wikipedia.org/wiki/ROT13) substitution cipher to all Latin characters.
```
Gur erq sbk whzcrq bire gur ynml qbt.
```

These transformations all change the input in ways that should be fairly easy for humans to decipher, but which will make interpreting the text far more difficult for existing language models.

## What tasks does it intend to benefit?

This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification,
text generation, etc.

## Related work

I am unaware of previous work requiring language models to adapt to simple ciphers of their input.

## What are the limitations of this transformation?

The ciphers are all very simple -- so this transformation requires the language model to be able to adapt to dramatic changes in how its input is presented, but does *not* require it to learn how to solve ciphers in a meaningful sense.

Each of the transformations included here is likely to occur in the wild on the web. The prevalence of text represented in these ways in the training data of common language models has not been investigated.
