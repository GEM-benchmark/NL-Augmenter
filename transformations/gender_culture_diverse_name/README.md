# gender culture diverse name transformantion 👨 ️→ 🐍🧔🏾
This transformation changes a name with another, considering gender and cultural diversity.
Example: Rachel --> Salome, Phoebe --> Rihab, Joey --> Clarinda, Chandler --> Deon, Monica --> Lamya

Contributor: Xudong Shen, National University of Singapore (xudong.shen@u.nus.edu)

## What does this transformation do?
For a recognized name, this transformation randomly samples a (country, gender) pair, and samples a new name from that (country, gender).
This transformation also allows sampling new names from the same sex, country, or both.

## Why is this transformation important?
1. What invariance are we trying to achieve by introducing name transformation? Besides invariance to the literal sence of name, invariance to the gender and cultural implications behind the name is also desirable. This could help mitigate many of the representation biases in the corpora, e.g., the glass ceiling effect that disadvantaged women in high ranks of management, the association between Muslim names and violence, and stereotypes about Asians.

2. The existing "Change Person Named Entities" transformation provides a poor coverage on non-English orign names. The statistics of the intersection between CheckList's and our dataset shows that 34.0%, 33.5%, 31.9%, 30.8% of the names therein are popular names in the US, Canada, Australia, and UK, respectively (note that a name can be popular in multiple countries). On the other hand, 0.4%, 0.4%, 0.5%, 2.1% of the names therein are popular names in India, Korea, China, and Kazakhstan. Using the existing name transformation fails to fairly represent the non-English origin names.

Thus, we are motivated to create a name transformation with gender and cultural diversity.

## What tasks does it intend to benefit?
(1) enhance the existing name transformation, which has a poor coverage on non-English origin names.
(2) help mitigate representation biases in the corpora.

could benefit (but not limited to): text classification, text-to-text generation

## data curation
Popular male and female names from 141 countries are collected from different sources.
42812 distinct names are included and, on average, 778 names are included for each (country,gender) pair.
Note that a name can be popular in multiple countries.

The names are from several sources, primarily the World Gender Name Dictionary (WGND) 2.0 [1]. Other sources include BIG-bench project [2], wikipedia [3,4].

We use country or territory code with the the ISO 3166-1 alpha-2 standard. The complete list of countries that are covered in this transformation: AU, CA, BE, GB, CN, AE, BH, CH, DZ, EG, ER, IQ, JO, KM, KW, LB, LY, MA, MR, OM, QA, SA, SD, SO, SY, TN, YE, IE, IN, US, ES, NL, FI, SE, EE, LV, DE, DK, NO, IS, NZ, AF, AZ, IR, AG, BB, BD, BI, BW, BZ, CB, CM, CY, DM, FJ, GD, GH, GY, JM, KE, KI, KN, LC, LR, LS, ME, MH, MT, MU, MW, NG, NR, PG, PH, PW, RS, RW, SB, SC, SL, SZ, TO, TT, TV, UG, VC, VU, WS, ZA, ZM, ZW, AT, BF, BJ, CD, CF, CG, CI, DJ, FR, GA, GN, HT, IL, LI, LU, MC, MG, ML, NE, PL, SN, TD, TG, LK, CZ, KZ, UZ, AL, BA, KS, TR, IT, MK, HR, HU, PT, SM, LT, AM, BY, MD, RU, RO, GR, SK, UA, BG, SI, KP, JP.

## What are the limitations of this transformation?
(1) the quality of non-English origin names might be limited because we rely on external sources and are unable to manually verify.

## Previous Work and References
[1] World Gender Name Dictionary (WGND) 2.0 
```bibtex
@data{DVN/MSEGSJ_2021,
author = {Raffo, Julio},
publisher = {Harvard Dataverse},
title = {{WGND 2.0}},
UNF = {UNF:6:5rI3h1mXzd6zkVhHurelLw==},
year = {2021},
version = {V1},
doi = {10.7910/DVN/MSEGSJ},
url = {https://doi.org/10.7910/DVN/MSEGSJ}
}
```
[2] https://github.com/google/BIG-bench/tree/main/bigbench/benchmark_tasks/gender_sensitivity_English
[3] https://en.wikipedia.org/wiki/List_of_most_popular_given_names
[4] https://en.wikipedia.org/wiki/List_of_the_most_popular_given_names_in_South_Korea
