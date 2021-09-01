# Font Change

The Font Change transformation modifies words in the input to have a stylized appearance using suitable Unicode characters, as often in encountered in social media posts.

Authors: [Shahab Raji](mailto:shahab.raji@rutgers.edu) (Rutgers University) and [Gerard de Melo](http://gerard.demelo.org/)
(Hasso Plattner Institute / University of Potsdam)


## How does the transformation work?

Font Change adapts the appearance of randomly selected words in the input sentence. For each selected word, one of several possible appearance changes is chosen randomly. Such changes are achieved using Unicode characters based on mapping tables from the [𝓾𝓷𝓲𝓬𝓸𝓭𝓮 𝙛𝙤𝙧𝙢𝙖𝙩𝙩𝙚𝙧](https://github.com/DenverCoder1/unicode-formatter) (MIT license) tool.

Examples:

> The quick brown fox jumps over the lazy dog.

to

> The quick brown 🅵🅾🆇 ɾnɯds over the lazy ᴅᴏɢ.

## Target Tasks

This transformation can be used for data augmentation in text classification tasks.

