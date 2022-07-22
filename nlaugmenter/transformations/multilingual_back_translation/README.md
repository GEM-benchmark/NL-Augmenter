# Multilingual Back Translation
This transformation translates a given sentence from a given language into a pivot language and then back to the original language.

Author name: William Soto
Author email: [williamsotomartinez@gmail.com](mailto:williamsotomartinez@gmail.com)
Author Affiliation: [SyNaLP](https://synalp.loria.fr/)([LORIA](https://www.loria.fr/en/))


## What type of a transformation is this?
This transformation is a simple paraphraser that works on 100 different languages thanks to the m2m100 many-to-many translation model. The user only needs to specify the source and target language. It is possible to select the same language as the source and pivot, in which case the many-to-many translation model will perform a "Direct Translation" from the source language to itself. While the "Direct Translation is faster (only calls the model once), the output sentences are usually very similar or even identical to the original ones.


## Supported Languages
Afrikaans (af), Amharic (am), Arabic (ar), Asturian (ast), Azerbaijani (az), Bashkir (ba), Belarusian (be), Bulgarian (bg), Bengali (bn), Breton (br), Bosnian (bs), Catalan; Valencian (ca), Cebuano (ceb), Czech (cs), Welsh (cy), Danish (da), German (de), Greeek (el), English (en), Spanish (es), Estonian (et), Persian (fa), Fulah (ff), Finnish (fi), French (fr), Western Frisian (fy), Irish (ga), Gaelic; Scottish Gaelic (gd), Galician (gl), Gujarati (gu), Hausa (ha), Hebrew (he), Hindi (hi), Croatian (hr), Haitian; Haitian Creole (ht), Hungarian (hu), Armenian (hy), Indonesian (id), Igbo (ig), Iloko (ilo), Icelandic (is), Italian (it), Japanese (ja), Javanese (jv), Georgian (ka), Kazakh (kk), Central Khmer (km), Kannada (kn), Korean (ko), Luxembourgish; Letzeburgesch (lb), Ganda (lg), Lingala (ln), Lao (lo), Lithuanian (lt), Latvian (lv), Malagasy (mg), Macedonian (mk), Malayalam (ml), Mongolian (mn), Marathi (mr), Malay (ms), Burmese (my), Nepali (ne), Dutch; Flemish (nl), Norwegian (no), Northern Sotho (ns), post 1500 Occitan (oc), Oriya (or), Panjabi; Punjabi (pa), Polish (pl), Pushto; Pashto (ps), Portuguese (pt), Romanian; Moldavian; Moldovan (ro), Russian (ru), Sindhi (sd), Sinhala; Sinhalese (si), Slovak (sk), Slovenian (sl), Somali (so), Albanian (sq), Serbian (sr), Swati (ss), Sundanese (su), Swedish (sv), Swahili (sw), Tamil (ta), Thai (th), Tagalog (tl), Tswana (tn), Turkish (tr), Ukrainian (uk), Urdu (ur), Uzbek (uz), Vietnamese (vi), Wolof (wo), Xhosa (xh), Yiddish (yi), Yoruba (yo), Chinese (zh), Zulu (zu).


## Previous Work
Zhenhao Li and Lucia Specia. 2019. [Improving neural machine translation robustness via data augmentation: Beyond backtranslation](https://arxiv.org/pdf/1910.03009.pdf).

Amane Sugiyama and Naoki Yoshinaga. 2019. [Data augmentation using back-translation for context-aware neural machine translation](https://aclanthology.org/D19-6504.pdf).

Angela Fan, Shruti Bhosale, Holger Schwenk, Zhiyi Ma, Ahmed El-Kishky, Siddharth Goyal, Mandeep Baines, Onur Celebi, Guillaume Wenzek, Vishrav Chaudhary, Naman Goyal, Tom Birch, Vitaliy Liptchinsky, Sergey Edunov, Edouard Grave, Michael Auli and Armand Joulin. 2021. [Beyond English-Centric Multilingual Machine Translation](https://www.jmlr.org/papers/volume22/20-1307/20-1307.pdf).

This transformation extends the idea behind the [back_translation](https://github.com/GEM-benchmark/NL-Augmenter/tree/main/transformations/back_translation) transformation by making it possible to apply the same strategy to source texts in 100 differente languages and allowing for 99 different pivot languages. Furthermore, this transformation only requires to download a single model ([m2m100](https://huggingface.co/facebook/m2m100_418M)) to perform any of the 9900 source and pivot language combinations.

Unlike the [lost_in_translation](https://github.com/GEM-benchmark/NL-Augmenter/tree/main/transformations/lost_in_translation) transformation, this transformation only performs one translation to the pivot language and back to the source language. It intends to generate accurate variations of the original input instead of adding noise to it.


## What tasks does it intend to benefit?
This transformations works to increase the data for any task that has input texts.


## What are the limitations of this transformation?
The transformation depends on the accuracy of the translation model being used for the given pair of languages.

## Robustness Evaluation
| Transformation                   | roberta-base-SST-2   | bert-base-uncased-QQP   | roberta-large-mnli   | roberta-base-imdb   |
|:---------------------------------|:---------------------|:------------------------|:---------------------|:--------------------|
| MultilingualBackTranslation      | 94.0->86.0 ( -8.0)   | 92.0->84.0 ( -8.0)      | 91.0->80.0 (-11.0)   | |
