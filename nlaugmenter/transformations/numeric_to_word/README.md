# Numeric to Word 🦎  + ⌨️ → 🐍
This transformation translates numbers in numeric form form written amongst the texts for:
- General numbers
    - general number (commas, thousands)
    - sticky numbers (2x, 5th, 8pm, 10%)
    - negatives (-0.5)
    - percentage
    - natural log (e(9))
    - fraction
    - long number
    - long number with stripes
    - sticky ranges ( (1-2) )
    - range not sticky ( ( 1-2 ) )
    - math formula equality
    - mathematical power of ten (10-4)
    - numeric in begin end bracket ( (34) )
    - numeric beside end bracket ( 34) )
    - numeric in math_bracket
    - special numbers (911)
    - currency (with the currency symbols and cents)
    - and more ..
- Datetime
    - incomplete_date
        - '01/2020'
        - '2020/01'
        - '20/01'
        - '01/20'
    - complete date
    - year
    - yime
    - date time
- Phone Number
    - general phone number
    - special phone number ('*#')

This transformation also translates the cases existed in test samples taken from:
- [SemEval 2019 Task 10: Math Question Answering](https://www.aclweb.org/anthology/S19-2153.pdf)
- [ChemistryQA](https://openreview.net/pdf?id=oeHTRAehiFF)
- [PubmedQA](https://www.aclweb.org/anthology/D19-1259.pdf)
- [SMD / KVRET](https://www.aclweb.org/anthology/2020.findings-emnlp.215/)
- [Mathematics Dataset](https://openreview.net/pdf?id=H1gR5iR5FX)
- [PubMed 200k RCT](https://www.aclweb.org/anthology/I17-2052.pdf)
- [BBC News](https://www.kaggle.com/c/learn-ai-bbc)

The 80 tested cases are listed in `test.json`, the transformation will return the text (no transformation), whenever the numeric cases is not recognized.

Author names: Bryan Wilie (bryanwilie92@gmail.com), Genta Indra Winata (giwinata@connect.ust.hk), Samuel Cahyawijaya (scahyawijaya@connect.ust.hk)

## What type of a transformation is this?
This transformation acts as a perturbation to test robustness in numbers understanding and generation when they are presented in the text form.

## What tasks does it intend to benefit?
This perturbation would benefit all tasks with a sentence/paragraph/document as input like text classification, text generation, etc.

## What are the limitations of this transformation?
The transformation does not transform numbers in numeric form that could be catered but , e.g.:
- "N2"
- "USD300!@#!"
- "(\$12,235)"
- "My phone number is 628782" -> considered defaultly as general numbers, will be read as six hundred and twenty-eight...
- "5.05" -> considered defaultly as a decimal, not an hour and minutes
- Only cater 1 prev and 1 next words, e.g.
    input: the sequel took $44.7m (£23.2m) between 24 and 26 december  according to studio estimates
    output: the sequel took forty-four point seven m dollar (twenty-three point two m pound) between twenty-four and twenty-sixth of december according to studio estimates
    remark: notice the difference of cardinality on twenty-four and twenty-sixth

Other cases that hasn't yet transformed, but maybe catered in near future:
- "HD5A"
- "C8H18"
- "NH4NO3"
- "231321412A2312BDSA"
- "ACTRN12613000290796"

Other cases that were not listed in the above cases, imaginable, but hasn't yet seen in any of the dataset samples:
- "(-0.5"
- "+17.5%"
- "5:05:30"
- "01 Sep. 11"
- "Jan 28 \'09"