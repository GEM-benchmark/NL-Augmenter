# Discourse Marker Substitution 
This perturbation replaces a discourse marker in a sentence by a semantically equivalent marker.
It is currently implemented for the english language and could be extended to other languages for which discourse relation corpus exists.
This method assumes untokenized text and uses whitespace tokenization.
Author name: Damien Sileo (damien.sileo@kuleuven.be)

## What type of a transformation is this?
This transformation acts like a perturbation to test robustness. If a discourse marker is detected, it is replaced with a semantically equivalent marker.
We use a corpus analysis on PDTB 2.0 to identify discourse markers that are associated with a discourse relation with a chance of at least 0.5.
Then, we replace a marker with a different marker that is associated to the same semantic class.


## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document as input like text classification, 
text generation, etc. 

```python evaluate.py -t DiscourseMarkerSubstitution -task TEXT_CLASSIFICATION```
```model_name = "aychang/roberta-base-imdb"```
The accuracy of a RoBERTa model (fine-tuned on IMDB) (model: "aychang/roberta-base-imdb") 
on a subset of IMDB sentiment dataset = 95.74
The accuracy of the same model on the perturbed set = 95.6


## Previous Work

1) Previous work has identified discourse markers that have a low ambiguity.
```bibtex
@inproceedings{pitler-etal-2008-easily,
    title = "Easily Identifiable Discourse Relations",
    author = "Pitler, Emily  and
      Raghupathy, Mridhula  and
      Mehta, Hena  and
      Nenkova, Ani  and
      Lee, Alan  and
      Joshi, Aravind",
    booktitle = "Coling 2008: Companion volume: Posters",
    month = aug,
    year = "2008",
    address = "Manchester, UK",
    publisher = "Coling 2008 Organizing Committee",
    url = "https://www.aclweb.org/anthology/C08-2022",
    pages = "87--90",
}
```
2) The corpus analysis relies on PDTB 2.0
```bibtex
@inproceedings{prasad-etal-2008-penn,
    title = "The {P}enn {D}iscourse {T}ree{B}ank 2.0.",
    author = "Prasad, Rashmi  and
      Dinesh, Nikhil  and
      Lee, Alan  and
      Miltsakaki, Eleni  and
      Robaldo, Livio  and
      Joshi, Aravind  and
      Webber, Bonnie",
    booktitle = "Proceedings of the Sixth International Conference on Language Resources and Evaluation ({LREC}'08)",
    month = may,
    year = "2008",
    address = "Marrakech, Morocco",
    publisher = "European Language Resources Association (ELRA)",
    url = "http://www.lrec-conf.org/proceedings/lrec2008/pdf/754_paper.pdf",
    abstract = "We present the second version of the Penn Discourse Treebank, PDTB-2.0, describing its lexically-grounded annotations of discourse relations and their two abstract object arguments over the 1 million word Wall Street Journal corpus. We describe all aspects of the annotation, including (a) the argument structure of discourse relations, (b) the sense annotation of the relations, and (c) the attribution of discourse relations and each of their arguments. We list the differences between PDTB-1.0 and PDTB-2.0. We present representative statistics for several aspects of the annotation in the corpus.",
}
```


## What are the limitations of this transformation?
The heuristic is not perfectly accurate.
