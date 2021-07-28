# Multilingual Back Translation
This transformation translates a given sentence from a given language into a pivot language and then back to the original language.

Author name: William Soto
Author email: [williamsotomartinez@gmail.com](mailto:williamsotomartinez@gmail.com)
Author Affiliation: [SyNaLP](https://synalp.loria.fr/)([LORIA](https://www.loria.fr/en/))

## What type of a transformation is this?
This transformation is a simple paraphraser that works on 100 different languages thanks to the m2m100 many-to-many translation model. The user only needs to speciffy the source and target language. It is possible to select the same language as source and pivot, in which case the many-to-many translation model will perform a "Direct Translation" from the source language to itslef (while this is faster the output sentences are usualy very similar or identical to the original ones).

## Supported Languages
Afrikaans (af), Amharic (am), Arabic (ar), Asturian (ast), Azerbaijani (az), Bashkir (ba), Belarusian (be), Bulgarian (bg), Bengali (bn), Breton (br), Bosnian (bs), Catalan; Valencian (ca), Cebuano (ceb), Czech (cs), Welsh (cy), Danish (da), German (de), Greeek (el), English (en), Spanish (es), Estonian (et), Persian (fa), Fulah (ff), Finnish (fi), French (fr), Western Frisian (fy), Irish (ga), Gaelic; Scottish Gaelic (gd), Galician (gl), Gujarati (gu), Hausa (ha), Hebrew (he), Hindi (hi), Croatian (hr), Haitian; Haitian Creole (ht), Hungarian (hu), Armenian (hy), Indonesian (id), Igbo (ig), Iloko (ilo), Icelandic (is), Italian (it), Japanese (ja), Javanese (jv), Georgian (ka), Kazakh (kk), Central Khmer (km), Kannada (kn), Korean (ko), Luxembourgish; Letzeburgesch (lb), Ganda (lg), Lingala (ln), Lao (lo), Lithuanian (lt), Latvian (lv), Malagasy (mg), Macedonian (mk), Malayalam (ml), Mongolian (mn), Marathi (mr), Malay (ms), Burmese (my), Nepali (ne), Dutch; Flemish (nl), Norwegian (no), Northern Sotho (ns), post 1500 Occitan (oc), Oriya (or), Panjabi; Punjabi (pa), Polish (pl), Pushto; Pashto (ps), Portuguese (pt), Romanian; Moldavian; Moldovan (ro), Russian (ru), Sindhi (sd), Sinhala; Sinhalese (si), Slovak (sk), Slovenian (sl), Somali (so), Albanian (sq), Serbian (sr), Swati (ss), Sundanese (su), Swedish (sv), Swahili (sw), Tamil (ta), Thai (th), Tagalog (tl), Tswana (tn), Turkish (tr), Ukrainian (uk), Urdu (ur), Uzbek (uz), Vietnamese (vi), Wolof (wo), Xhosa (xh), Yiddish (yi), Yoruba (yo), Chinese (zh), Zulu (zu).

## What tasks does it intend to benefit?
This transformations works to increase the data for any task that has input texts.

## What are the limitations of this transformation?
The outputs dependend on the accuracy of the translation model for thegiven pair of languages.