# GeoNames Transformation
This transformation augments the input sentence with information based on location entities available in GeoNames (currently only cities and countries are supported).

Author name: Vasile Pais
Author email: vasile@racai.ro
Author Affiliation: Research Institute for Artificial Intelligence "Mihai Drăgănescu", Romanian Academy

## What type of a transformation is this?
This transformation identifies cities and countries present in GeoNames and augment the sentence with additional information.

For countries, the following information is used: continent, capital, population, neighbours, languages.

For cities, the following information is used: continent, country, population.


## What tasks does it intend to benefit?
This data augmentation would benefit all tasks which have a sentence/paragraph/document as input like text classification, 
text generation, etc., as long as the text contains city/country names.

Example sentence:

```Mangalia is situated on the shores of the Black Sea```

Generated sentences:

```Mangalia, a city in Romania, is situated on the shores of the Black Sea```

```Mangalia, a city with a population of 39,619, is situated on the shores of the Black Sea```

```Mangalia, a city in Romania, with a population of 39,619 inhabitants, is situated on the shores of the Black Sea```

```Mangalia, a city in Europe, is situated on the shores of the Black Sea```

```Mangalia, a city in Europe, with a population of 39,619 inhabitants, is situated on the shores of the Black Sea```


## Data and code provenance
This transformation makes use of city and country information obtained from GeoNames ( http://download.geonames.org/export/dump/ ).
Additionally, locale codes were used for obtaining the language names. This information was obtained from ( https://www.science.co.il/language/Locale-codes.php ).

The code was written from scratch by the author for this project. An initial idea was explored for the purposes of my PhD thesis:
```Vasile Păiș. Contributions to semantic processing of texts; Identification of entities and relations between textual units; Case study on Romanian language. PhD thesis, Romanian Academy, 2019.```

## What are the limitations of this transformation?
If the identified name corresponds to both a city and a country, only the country enhancements will be applied. The transformation does not perform disambiguation to understand if it is a city or a country.