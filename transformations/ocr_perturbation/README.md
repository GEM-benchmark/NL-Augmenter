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
2. Install [Tesseract](https://github.com/tesseract-ocr/tesseract) (including dependencies and models). See the [installation instructions](https://tesseract-ocr.github.io/tessdoc/#compiling-and-installation) for your operating system. For example, On Debian or Ubuntu, you can simply use its developer tools:

```bash
apt-get install tesseract-ocr libtesseract-dev libleptonica-dev pkg-config \
  tesseract-ocr-eng tesseract-ocr-osd tesseract-ocr-deu tesseract-ocr-fra tesseract-ocr-spa
```

3. Install dependencies to other Python packages using [pip](https://pypi.org/project/pip/):

```bash
pip3 install -r requirements.txt
```

#### Example Usage

An example of how to use this transformation can be found in the *generate_test_cases()* function in [helper.py](../../test/helper.py).

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph as input like text classification, text generation, etc. It could be primarily used for robustness evaluation but could also be employed for data augmentation.

As a result of applying this transformation, the following results of the robustness evaluation were obtained:

- The accuracy of the *textattack/roberta-base-imdb* model,  evaluated on a subset of 1000 examples from the IMDB test set, dropped  from 95.0 (original examples) to 94.0 (perturbed examples).

```
python evaluate.py -t OcrPerturbation -task "TEXT_CLASSIFICATION" -m "textattack/roberta-base-imdb" -d "imdb" -p 20
```

- The accuracy of the *roberta-large-mnli* model, evaluated on a subset of 1000 examples from the MNLI validation set, dropped from 91.0 (original examples) to 89.0 (perturbed examples).

```
python evaluate.py -t OcrPerturbation -task "TEXT_CLASSIFICATION" -m "roberta-large-mnli" -d "multi_nli" -p 20
```

- The accuracy of the *textattack/bert-base-uncased-QQP* model, evaluated on a subset of 1000 examples from the QQP validation set,  dropped from 92.0 (original examples) to 87.0 (perturbed examples).

```
python evaluate.py -t OcrPerturbation -task "TEXT_CLASSIFICATION" -m "textattack/bert-base-uncased-QQP" -d "qqp" -p 20
```

- The accuracy of the *textattack/roberta-base-SST-2* model,  evaluated on a subset of 174 examples from the SST-2 validation set,  dropped from 94.0 (original examples) to 89.0 (perturbed examples).

```
python evaluate.py -t OcrPerturbation -task "TEXT_CLASSIFICATION" -m "textattack/roberta-base-SST-2" -d "sst2" -p 20
```

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

