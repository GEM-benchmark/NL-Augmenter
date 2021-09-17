# Visual Attack Letter
This perturbation replaces letters with visually similar, but different, letters.
Every letter was embedded into 576-dimensions. The nearest neighbors are obtained through cosine distance.
How was the embedding obtained? The letter was resized into a 24x24 image, then flattened and scaled.
This follows the Image Based Character Embedding (ICES) described in this paper: https://arxiv.org/pdf/1903.11508v1.pdf

The top neighbors from each letter are chosen. Some were removed by judgment (e.g. the nearest neighbors for 'v' are many variations of the letter 'y') which did not qualify from the image embedding.
You should be able to add more typefaces as they are created. (e.g. 🅰🅱🅲🅳🅴, 𝕒𝕓𝕔𝕕𝕖) if you want. For this version, I focused only on visual similarity.

Author name: Corey James Levinson
Author email: thecoreylevinson@gmail.com
Author Affiliation: None

## What type of a transformation is this?
This transformation acts like a perturbation to test robustness and visual intuition of letters. 
Transformations are chosen according to their ICES embedding. The embeddings were downloaded here: https://public.ukp.informatik.tu-darmstadt.de/naacl2019-like-humans-visual-attacks/
Generated transformations display high similarity to the source sentences i.e. the code outputs highly precise generations. 

## What tasks does it intend to benefit?
This perturbation would benefit tasks which measure effectiveness against visual attacks. For example, it can be used to test robustness of profanity filters.

```python evaluate.py -t VisualAttackLetters -task TEXT_CLASSIFICATION```
```model_name = "aychang/roberta-base-imdb"```


## Previous Work

```bibtex
@article{DBLP:journals/corr/abs-1903-11508,
  author    = {Steffen Eger and
               G{\"{o}}zde G{\"{u}}l Sahin and
               Andreas R{\"{u}}ckl{\'{e}} and
               Ji{-}Ung Lee and
               Claudia Schulz and
               Mohsen Mesgar and
               Krishnkant Swarnkar and
               Edwin Simpson and
               Iryna Gurevych},
  title     = {Text Processing Like Humans Do: Visually Attacking and Shielding {NLP}
               Systems},
  journal   = {CoRR},
  volume    = {abs/1903.11508},
  year      = {2019},
  url       = {http://arxiv.org/abs/1903.11508},
  archivePrefix = {arXiv},
  eprint    = {1903.11508},
  timestamp = {Tue, 02 Apr 2019 11:16:55 +0200},
  biburl    = {https://dblp.org/rec/journals/corr/abs-1903-11508.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```


## What are the limitations of this transformation?
- Not all characters were visually embedded. For example, many emojis and other rare characters are missing. There were only 29,971 characters used. You can verify which ones were used by looking at the Gensim model.
- I subjectively removed some letters. You could make it automatic, but I feared there would be some errors in it. For example, if you take the top 20 most visually similar letters to 'v', you would get a lot of variations on the letter 'y', but obviously that would conflict with another letter, so I subjectively removed some visually similar letters that were suggested by Eger et al.'s model.
- This perturbation will not work well to non-alphabetic writing systems, e.g. logographic alphabets like Hanzi (Chinese), abjads like Arabic, and abugidas like Bengali. 

Visually attacking the letters negatively affects the tokenization process. It can be improved by using Unicode Normalization (https://unicode.org/reports/tr15/) For example, Unicode Normalization could convert "Héllò hôw are ü?" to "Hello how are u?". Check out https://huggingface.co/docs/tokenizers/python/latest/api/reference.html#tokenizers.normalizers.Normalizer for a Normalizer offered by Huggingface.

Anyway, usually the affected words will just be replaced by an [UNK] token in BERT. For Roberta-base, the tokenizer fails spectacularly, see example: https://github.com/huggingface/transformers/issues/1189 . For example, in evaluation, -m "roberta-large-mnli" -d "multi_nli" decreased score from 91.0 to 47.0

XLM-Roberta tokenizer fares much better; it still usually tokenizes one character at a time, but since it has encountered a variety of characters, it can fare better.
