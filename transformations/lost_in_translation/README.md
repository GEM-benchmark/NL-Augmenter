# Lost in Translation
Lost in Translation (LiT) is a generalization of the BackTranslation transformation to any languages supported by Helsinki-NLP OpusMT models (https://huggingface.co/Helsinki-NLP). The `generate()` method implements a transformation consisting of an arbitrary number of layers, each of which is a single encode-decode (en->lang->en) cycle.

Example:
```
Input: "Sentences with gapping, such as Paul likes coffee and Mary tea,
lack an overt predicate to indicate the relation between two or more 
arguments."

Layers (5): en -> es -> de -> zh -> fr -> ru -> en

Output: "Because Paul loves coffee and tea, there is a gap in the verdict,
and there is no clear prerequisite for the relationship between two or 
more arguments."
```

Author name: M. Yee

## What type of a transformation is this?
For few encode-decode layers, LiT functions similarly to BackTranslation, in that its output is analgous to a light paraphraser. However, complexity and information loss increase with addition of subsequent layers, allowing users to specify the degree to which the input should be corrupted via the `layers` argument. LiT is reminiscent of the game of "telephone" in some ways.

## What tasks does it intend to benefit?
This perturbation is intended for the `SentenceOperation` task, although it may be suited for a machine translation task as well.

## Usage
The `LostInTranslation` class supports a number of options. A list of languages (`lang`) can be passed, and encode-decode cycles draw from this list in different manners via the `how` argument. The default behavior is `strict` which simply iterates through the list as-is; this was selected for reproducibility of `task.json`. However, the transformation is intended to use the `random` strategy, in which successive language layers are drawn from the provided list with replacement. `layers` specifies the total number of encode-decode cycles, and in the case of both `strict` and `layers>len(langs)` will restart the list from the beginning.

## Data and code provenance
This code was based upon the `ButterFingersPerturbation` transformation template. The en->xx and xx->en models are provided by the Helsinki-NLP OpusMT project, cited below.

## Previous Work
BackTranslation: https://github.com/GEM-benchmark/NL-Augmenter/tree/main/transformations/back_translation

```bibtex
@InProceedings{TiedemannThottingal:EAMT2020,
  author = {J{\"o}rg Tiedemann and Santhosh Thottingal},
  title = {{OPUS-MT} — {B}uilding open translation services for the {W}orld},
  booktitle = {Proceedings of the 22nd Annual Conferenec of the European Association for Machine Translation (EAMT)},
  year = {2020},
  address = {Lisbon, Portugal}
 }
```

```bibtex
@article{li2019improving,
  title={Improving neural machine translation robustness via data augmentation: Beyond back translation},
  author={Li, Zhenhao and Specia, Lucia},
  journal={arXiv preprint arXiv:1910.03009},
  year={2019}
}
```
## What are the limitations of this transformation?
LiT takes a significant amount of time to run as it calls the Hugging Face pipeline `<layers>` times for each example. It also requires bandwidth and disk space for `<2*len(langs)>` datasets.
