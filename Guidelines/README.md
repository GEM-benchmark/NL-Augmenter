



| Implementation | Type  | Tasks | Comments | Prior Work / Source | Example                                                                     
| ------- | ---------- | -----------   | ----------- | ----------- | -----------                   
| [butter_fingers_perturbation](https://github.com/GEM-benchmark/NL-Augmenter/tree/main/transformations/butter_fingers_perturbation) | Transformation | All NLP tasks which take in a text as input     | Adds noise to all types of text sources (sentence, paragraph, etc.) in rough proportion to noise emanating from keyboard typos making common spelling errors. | [Alex Yorke's repo](https://github.com/alexyorke/butter-fingers) | TODO
| Coref replacement  | Transformation | All NLP tasks which take in sufficiently long / multi-sentence text as input     | Replaces nominal or pronominal mentions by coreferent named mentions (and vice-versa) | TODO | John is a great archer. He plays football too. --> John is a great archer. John plays football too.
