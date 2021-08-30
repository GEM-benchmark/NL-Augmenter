# Subsequence substitution for sequence tagging augmentation 🦎  + 🦎 → 🐍


## What type of a transformation is this?
This transformation performs same-label subsequence substitution for the task of sequence tagging, which replaces a subsequence of the input tokens with another one that has the same sequence of tags.

### Example

**Input**

tokens: `['EU', 'rejects', 'German', 'call', 'to', 'boycott', 'British', 'lamb', '.']`

(POS) tags: `['NNP', 'VBZ', 'JJ', 'NN', 'TO', 'VB', 'JJ', 'NN', '.']`

**Drawn subsequence from input**

tokens: `['British', 'lamb']`

(POS) tags: `['JJ', 'NN']`

**Reference (randomly drawn from datset w.r.t. subsequence tags)**

tokens: `['Germany', 'imported', '47,600', 'sheep', 'from', 'Britain', 'last', 'year', ',', 'nearly', 'half', 'of', 'total', 'imports', '.']`

(POS) tags: `['NNP', 'VBD', 'CD', 'NN', 'IN', 'NNP', 'JJ', 'NN', ',', 'RB', 'NN', 'IN', 'JJ', 'NNS', '.']`

**Substitution content** (with the same label subsequence as the drawn subsequence from input)

tokens: `['last', 'year']`

(POS) tags: `['JJ', 'NN']`

**Output**

tokens: `['EU', 'rejects', 'German', 'call', 'to', 'boycott', 'last', 'year', '.']`

(POS) tags: `['NNP', 'VBZ', 'JJ', 'NN', 'TO', 'VB', 'JJ', 'NN', '.']`

See more details in the paper: [Substructure Substitution: Structured Data Augmentation for NLP](https://aclanthology.org/2021.findings-acl.307).

## What tasks does it intend to benefit?
This perturbation would benefit all sequence labeling tasks, and is originally tested on part-of-speech (POS) tagging.

## What are the limitations of this transformation?
One would need to specify a dataset to operate with when using this pertubation (see the argument `base_dataset: List[Tuple[List[str], List[str]]]` of the `TagSubsequenceSubstitution` class, which should consists of a list of (tokens, tags) tuples); however, this should be easy to obtain in most supervised learning settings, by setting it as the training set.

Another limitation is that this pertubation may not be very helpful to handle unseen words by design, as all generated sequences are within the original vocabulary.

## Reference
```
@inproceedings{shi-etal-2021-substructure,
    title = "Substructure Substitution: Structured Data Augmentation for {NLP}",
    author = "Shi, Haoyue  and
      Livescu, Karen  and
      Gimpel, Kevin",
    booktitle = "Findings of the Association for Computational Linguistics: ACL-IJCNLP 2021",
    year = "2021",
    url = "https://aclanthology.org/2021.findings-acl.307",
    pages = "3494--3508",
}
```