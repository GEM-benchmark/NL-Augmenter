# Chinese Pinyin Butter Fingers Perturbation 🦎  + ⌨️ → 🐍
This perturbation adds noise to all types of text sources containing Chinese words and characters (sentence, paragraph, etc.) proportional to noise erupting 
from keyboard typos making errors resulting from Chinese words and characters that have similiar Pinyin (with or without tones). 

Author name: Timothy Sum Hon Mun
Author email: timothy22000@gmail.com

## What type of a transformation is this?
This transformation perturbes Chinese input text to test robustness. Few Chinese words and characters that are picked at random will be replaced with words and characters 
that have similar pinyin (based on the default Pinyin keyboards in Windows and Mac OS) where the user may accidentally select the wrong word or character from the returned results. 

It uses a database of 16142 Chinese characters （单字库）and its associated pinyins to generate the perturbations for Chinese characters. 
A smaller database of 3500 more frequently seen Chinese characters are also used in the perturbations with a higher probability of being used compared to less frequently seen Chinese characters.

It also uses a database of 575173 words (词库) that are combined from several sources in order to generate perturbations for Chinese words.

## What tasks does it intend to benefit?
This perturbation would benefit all tasks which have a sentence/paragraph/document with Chinese words and characters as input like text classification, 
text generation, etc.

## Previous Work

1) Xinhua Dictionary Database for Chinese characters: https://github.com/pwxcoo/chinese-xinhua
2) 清华大学开放中文词库 THUOCL: http://thuocl.thunlp.org/
3) 中文数据预处理材料: https://github.com/fighting41love/Chinese_from_dongxiexidian
4) 3500常用汉字: https://github.com/elephantnose/characters

## What are the limitations of this transformation?
There could be Chinese characters that are not within the database of 16142 characters since there are over 50000 Chinese characters.
However, the commonly utilized characters in modern Chinese are around 7000 - 8000 characters and most modern Chinese dictionaries will list around 16000 - 20000 characters so the database should cover most cases.

There also could be Chinese words that are not within the database of 575173 words.

A more comprehensive database for Chinese words and characters can be used. This will be left as future work for the project.

