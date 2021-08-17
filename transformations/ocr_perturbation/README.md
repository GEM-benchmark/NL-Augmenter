# OCR Perturbation 🦎+ ⌨️ → 🐍
This transformation directly induces Optical Character Recognition (OCR) errors into the input text. It renders the input sentence as an image and recognizes the rendered text using an OCR engine:

<p align="center"> 
  <b>Neil Alden Armstrong was an American astronaut.</b>
  <br>
    <font size="+3">&#8595;</font>
  <br>
  <img src="example.png" style="zoom:200%;" />
  <br>
    <font size="+3">&#8595;</font>
  <br>
    <font size="+3">&#128441;&#128269;</font><font size="+4" color="blue">Tesseract 4 OCR</font>
  <br>
    <font size="+3">&#8595;</font>
  <br>
    <b>Neil: Alden Armstrong was an 'Ametican astronaut:</b>
</p>


Author: [Marcin Namysl](https://github.com/mnamysl/)

## What type of transformation is this?
This transformation acts like a sentence-level perturbation. Multiple variations can be created via changing parameters, e.g., various image rendering options can be specified.

This transformation employs the [trdg](https://pypi.org/project/trdg/) package for image rendering and the [tesserocr](https://pypi.org/project/tesserocr/) package for OCR. Currently, it can be applied to text in English, French, Spanish, or German.

#### Prerequisites 

1) Download [spaCy](https://pypi.org/project/spacy/) models for the supported languages:

```sh
python -m spacy download en_core_web_sm
python -m spacy download fr_core_web_sm
python -m spacy download es_core_web_sm
python -m spacy download de_core_web_sm
```
2. Install *libtesseract* and *libleptonica*. Please refer to the documentation of the [tesserocr](https://pypi.org/project/tesserocr/) package for more details.

3. Download [Tesseract models](https://tesseract-ocr.github.io/tessdoc/Data-Files) and copy them to the *tessdata* path on your machine (see [documentation](https://tesseract-ocr.github.io/tessdoc/Data-Files)):
[Orientation and script detection](https://github.com/tesseract-ocr/tessdata/raw/3.04.00/osd.traineddata), 
[English](https://github.com/tesseract-ocr/tessdata/raw/4.00/eng.traineddata), 
[French](https://github.com/tesseract-ocr/tessdata/raw/4.00/fra.traineddata), 
[Spanish](https://github.com/tesseract-ocr/tessdata/raw/4.00/spa.traineddata), 
[German](https://github.com/tesseract-ocr/tessdata/raw/4.00/deu.traineddata).

#### Example Usage

An example of how to use this transform can be found in [example.py](./example.py).

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph as input like text classification, text generation, etc. It could be primarily used for robustness evaluation but could also be employed for data augmentation.

As a result of applying this transformation, the following preliminary results of the robustness evaluation were obtained:

- The accuracy of the RoBERTa model ("*aychang/roberta-base-imdb*"), evaluated on a subset of 1000 examples from the IMDB sentiment dataset, dropped from 96.0 (original examples) to 93.0 (perturbed examples).
- The average BLEU score of the DistilBART model ("*sshleifer/distilbart-xsum-12-6*"), evaluated on a subset (10%) of XSum dataset, dropped from 15.25 (original examples) to 12.50 (perturbed examples).

## Previous Work

1) This transformation is an adapted version of the method from the [Noise-Aware Training (NAT) v2](https://github.com/mnamysl/nat-acl2021) project, introduced in the following paper:

```bibtex
@inproceedings{namysl-etal-2021-empirical,
    title = "Empirical Error Modeling Improves Robustness of Noisy Neural Sequence Labeling",
    author = {Namysl, Marcin  and
      Behnke, Sven  and
      K{\"o}hler, Joachim},
    booktitle = "Findings of the Association for Computational Linguistics: ACL-IJCNLP 2021",
    month = aug,
    year = "2021",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2021.findings-acl.27",
    doi = "10.18653/v1/2021.findings-acl.27",
    pages = "314--329",
}
```


## What are the limitations of this transformation?
Image distortion parameters were balanced based on the recognition quality of the supported OCR models. In some cases, using too strong distortions may cause the rendered text to be illegible or poorly recognized by the OCR model.

This Transformation currently employs the Tesseract OCR engine. Errors made by different OCR engines may have different characteristics.

