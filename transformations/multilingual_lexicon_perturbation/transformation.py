import os
import random
import string
import pandas as pd

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

import nltk
nltk.download('punkt')
from nltk import word_tokenize


"""
Multilingual Lexicon Perturbation

This perturbation translates words in the text from any supported languages (e.g., English) to other supported languages (e.g., German) by using a multilingual lexicon. It can be used to test the robustness of a model in a multilingual setting. 

There are 100 langauges supported as listed below:
Afrikaans (af), Amharic (am), Arabic (ar), Asturian (ast), Azerbaijani (az), Bashkir (ba), Belarusian (be), Bulgarian (bg), Bengali (bn),
Breton (br), Bosnian (bs), Catalan; Valencian (ca), Cebuano (ceb), Czech (cs), Welsh (cy), Danish (da), German (de), Greeek (el), English (en),
Spanish (es), Estonian (et), Persian (fa), Fulah (ff), Finnish (fi), French (fr), Western Frisian (fy), Irish (ga), Gaelic; Scottish Gaelic (gd),
Galician (gl), Gujarati (gu), Hausa (ha), Hebrew (he), Hindi (hi), Croatian (hr), Haitian; Haitian Creole (ht), Hungarian (hu), Armenian (hy),
Indonesian (id), Igbo (ig), Iloko (ilo), Icelandic (is), Italian (it), Japanese (ja), Javanese (jv), Georgian (ka), Kazakh (kk), Central Khmer (km),
Kannada (kn), Korean (ko), Luxembourgish; Letzeburgesch (lb), Ganda (lg), Lingala (ln), Lao (lo), Lithuanian (lt), Latvian (lv), Malagasy (mg),
Macedonian (mk), Malayalam (ml), Mongolian (mn), Marathi (mr), Malay (ms), Burmese (my), Nepali (ne), Dutch; Flemish (nl), Norwegian (no),
Northern Sotho (ns), Occitan (post 1500) (oc), Oriya (or), Panjabi; Punjabi (pa), Polish (pl), Pushto; Pashto (ps), Portuguese (pt),
Romanian; Moldavian; Moldovan (ro), Russian (ru), Sindhi (sd), Sinhala; Sinhalese (si), Slovak (sk), Slovenian (sl), Somali (so), Albanian (sq),
Serbian (sr), Swati (ss), Sundanese (su), Swedish (sv), Swahili (sw), Tamil (ta), Thai (th), Tagalog (tl), Tswana (tn), Turkish (tr),
Ukrainian (uk), Urdu (ur), Uzbek (uz), Vietnamese (vi), Wolof (wo), Xhosa (xh), Yiddish (yi), Yoruba (yo), Chinese (zh), Zulu (zu)
"""

FOLDER_PATH = '/'.join(os.path.abspath(__file__).split('/')[:-1])

def translate(model, tokenizer, text, src_lang, target_lang):
    tokenizer.src_lang = src_lang
    encoded = tokenizer(text, return_tensors="pt")
    generated_tokens = model.generate(**encoded, forced_bos_token_id=tokenizer.get_lang_id(target_lang))
    res = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
    return res

def perturb_sentence(lexicon_df, text, prob_mix=0.5, src_lang="en", trg_lang="zh", seed=0):
    random.seed(seed)
    l_df = lexicon_df.set_index(src_lang)

    words = word_tokenize(text)
    mixed_text = ""
    for word in words:
        # Add space between word
        if mixed_text != "":
            mixed_text += " "
            
        if word.lower() not in l_df.index:
            mixed_text += word
        else:
            rand_prob = random.random()
            if rand_prob < prob_mix:
                plain_word = word.translate(str.maketrans('', '', string.punctuation)).strip().lower()

                if plain_word == "":
                    continue

                if not word[0].isupper(): # lower case
                    perturbed_word = l_df.loc[plain_word, trg_lang]
                else:
                    perturbed_word = l_df.loc[plain_word, trg_lang].capitalize()
                    
                mixed_text += perturbed_word
            else:
                mixed_text += word

    # print(text, mixed_text)
    return mixed_text

class MultilingualLexiconPerturbation(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION
    ]
    supported_languages = [
        'af', 'am', 'ar', 'ast', 'az', 'ba', 'be', 'bg', 'bn', 'br', 'bs', 'ca', 'ceb', 'cs', 'cy',
        'da', 'de', 'el', 'en', 'es', 'et', 'fa', 'ff', 'fi', 'fr', 'fy', 'ga', 'gd', 'gl', 'gu',
        'ha', 'he', 'hi', 'hr', 'ht', 'hu', 'hy', 'id', 'ig', 'ilo', 'is', 'it', 'ja', 'jv', 'ka',
        'kk', 'km', 'kn', 'ko', 'lb', 'lg', 'ln', 'lo', 'lt', 'lv', 'mg', 'mk', 'ml', 'mn', 'mr',
        'ms', 'my', 'ne', 'nl', 'no', 'ns', 'oc', 'or', 'pa', 'pl', 'ps', 'pt', 'ro', 'ru', 'sd',
        'si', 'sk', 'sl', 'so', 'sq', 'sr', 'ss', 'su', 'sv', 'sw', 'ta', 'th', 'tl', 'tn', 'tr', 
        'uk', 'ur', 'uz', 'vi', 'wo', 'xh', 'yi', 'yo', 'zh', 'zu'
    ]    
    heavy = False

    def __init__(self, seed=0, prob_mix=0.5, src_lang="en", trg_lang="zh"):
        super().__init__(seed)
        if src_lang not in self.supported_languages: 
            raise ValueError(f'Invalid `src_lang` value "{src_lang}". Supported languages: {supported_languages}')
            
        if trg_lang not in self.supported_languages:
            raise ValueError(f'Invalid `trg_lang` value "{trg_lang}". Supported languages: {supported_languages}')
            
        self.lexicon_df = pd.read_pickle(f'{FOLDER_PATH}/multilingual_lexicon_uncased.xz')
        
        self.prob_mix=prob_mix
        self.src_lang=src_lang
        self.trg_lang=trg_lang

    def generate(self, sentence: str):
        pertubed_sentence = perturb_sentence(lexicon_df=self.lexicon_df, text=sentence, prob_mix=self.prob_mix, src_lang=self.src_lang, trg_lang=self.trg_lang, seed=self.seed)
        return [pertubed_sentence]
