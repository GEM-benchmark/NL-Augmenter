## Language filter

## What type of a filter is this?
This filter returns a list of texts that match any of a given set of ISO 639-1 language codes (defaults to ['en']).
Language matching is performed using a pre-trained ``langid.py`` model instance.
The model provides normalized confidence scores, so we allow the user to specify the minimum required probability to
return a positive result (defaults to 0.5).

More model details can be [found here](https://github.com/saffsd/langid.py).

Author: [Richard Plant](https://orcid.org/0000-0002-0239-2090)

Based on prior work by [Marco Lui](https://github.com/saffsd)

## Why is measuring performance on this split important?

This filter can help remove texts in languages other than the desired set, promoting more rapid and efficient training.

```
python evaluate.py -f LanguageFilter
Undefined task type, switching to default task %s TEXT_CLASSIFICATION
Loading <imdb> dataset to evaluate <aychang/roberta-base-imdb> model.
Here is the performance of the model aychang/roberta-base-imdb on the test[:20%] split of the imdb dataset
Applying filtering:
100%|███████████████████████████████████████| 1000/1000 [22:39<00:00,  1.36s/it]
Here is the performance of the model on the filtered set
The accuracy on this subset which has 1000 examples = 96.0
```

## Related Work

[Marco Lui and Timothy Baldwin (2012) langid.py: An Off-the-shelf Language Identification Tool](https://aclanthology.org/P12-3005/)

## What are the limitations of this filter?

Requires >= Python 2.7 and numpy.

Langid.py is pre-trained on the following languages (ISO 639-1 codes):

af, am, an, ar, as, az, be, bg, bn, br, bs, ca, cs, cy, da, de, dz, el, en, eo, es, et, eu, fa, fi, fo, fr, ga, gl, gu,
he, hi, hr, ht, hu, hy, id, is, it, ja, jv, ka, kk, km, kn, ko, ku, ky, la, lb, lo, lt, lv, mg, mk, ml, mn, mr, ms, mt,
nb, ne, nl, nn, no, oc, or, pa, pl, ps, pt, qu, ro, ru, rw, se, si, sk, sl, sq, sr, sv, sw, ta, te, th, tl, tr, ug, uk,
ur, vi, vo, wa, xh, zh, zu
