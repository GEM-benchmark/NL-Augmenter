import io
import os
import nltk

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


class GeoNamesTransformation(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
    ]
    languages = ["en"]

    def loadCities(self):
        self.cities = {}

        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__))
        )

        with io.open(
            os.path.join(__location__, "cities5000.txt"), mode="r", encoding="utf8"
        ) as file:
            while True:
                data = file.readline()
                if not data:
                    break

                line = data.split("\t")

                # 1 = name
                # 2 = asciiname
                # 3 = alternatenames
                # 8 = country code
                # 14 = population

                # print(line)
                alternates = {}
                alternates[line[1]] = True
                alternates[line[2]] = True
                if len(line[3]) > 0:
                    for alt in line[3].split(","):
                        alternates[alt] = True
                current = {
                    "country": line[8],
                    "population": line[14],
                    "alternates": list(alternates.keys()),
                }
                for c in alternates:
                    self.cities[c] = current

        # print("Loaded %d cities"%(len(self.cities)))

    def loadLocales(self):
        self.locales = {}

        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__))
        )

        with io.open(
            os.path.join(__location__, "locales.txt"), mode="r", encoding="utf8"
        ) as file:
            first = True
            while True:
                data = file.readline()
                if not data:
                    break

                line = data.split("\t")

                if first:
                    first = False
                    continue

                # 0 = locale name
                # 1 = language code
                # 2 = LCID code

                language = line[0].split("-")[0].strip()
                basicCode = line[2].split("-")[0].strip()

                self.locales[line[2]] = {
                    "language": language,
                }

                self.locales[basicCode] = {
                    "language": language,
                }
        # print("Loaded %d locales"%(len(self.locales)))

    def loadCountries(self):
        self.countries = {}
        self.countriesName = {}
        self.capitals = {}

        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__))
        )

        with io.open(
            os.path.join(__location__, "countryInfo.txt"), mode="r", encoding="utf8"
        ) as file:
            while True:
                data = file.readline()
                if not data:
                    break

                if data.startswith("#"):
                    continue

                line = data.split("\t")

                # 0 = ISO
                # 1 = ISO3
                # 4 = name
                # 5 = capital
                # 7 = population
                # 8 = continent
                # 11 = currency name
                # 15 = languages
                # 17 = neighbours

                neighbours = []
                if len(line[17]) > 0:
                    neighbours = line[17].split(",")

                self.countries[line[0]] = {
                    "name": line[4],
                    "capital": line[5],
                    "population": line[7],
                    "continent": line[8],
                    "currency": line[11],
                }

                self.countriesName[line[4]] = {
                    "iso": line[0],
                    "iso3": line[1],
                    "capital": line[5],
                    "population": line[7],
                    "continent": line[8],
                    "currency": line[11],
                    "neighbours": neighbours,
                    "languages": line[15].split(","),
                }

                self.capitals[line[5]] = {"countryName": line[4]}

        # print("Loaded %d countries"%(len(self.countries)))

    def loadContinents(self):
        self.continents = {
            "AF": "Africa",
            "AS": "Asia",
            "EU": "Europe",
            "NA": "North America",
            "OC": "Oceania",
            "SA": "South America",
            "AN": "Antarctica",
        }

    def __init__(self, seed=0, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)

        self.loadContinents()
        self.loadCountries()
        self.loadCities()
        self.loadLocales()

    def pattern_countryInContinent(self, start, final, data, textFeatures):
        continent = self.continents[data["continent"]]
        if continent in textFeatures:
            return []
        return [(start + ", a country in " + continent + final)]

    def pattern_countryInContinentWithPopulation(
        self, start, final, data, textFeatures
    ):
        continent = self.continents[data["continent"]]
        population = "{:,}".format(int(data["population"]))
        if continent in textFeatures:
            return []
        return [
            (
                start
                + ", a country in "
                + continent
                + ", with a population of "
                + population
                + " inhabitants"
                + final
            )
        ]

    def pattern_countryWithCapital(self, start, final, data, textFeatures):
        capital = data["capital"]
        if capital in textFeatures:
            return []
        return [(start + ", whose capital city is " + capital + final)]

    def pattern_countryInContinentWithPopulationAndCapital(
        self, start, final, data, textFeatures
    ):
        continent = self.continents[data["continent"]]
        population = "{:,}".format(int(data["population"]))
        capital = data["capital"]
        if continent in textFeatures or capital in textFeatures:
            return []
        return [
            (
                start
                + ", a country in "
                + continent
                + ", with a population of "
                + population
                + " inhabitants, with the capital at "
                + capital
                + final
            )
        ]

    def pattern_countryWithISO(self, start, final, data, textFeatures):
        iso = data["iso"]
        if iso in textFeatures:
            return []
        return [(start + " (" + iso + ")" + final)]

    def pattern_countryWithISO3(self, start, final, data, textFeatures):
        iso3 = data["iso3"]
        if iso3 in textFeatures:
            return []
        return [(start + " (" + iso3 + ")" + final)]

    def pattern_countryWithISOAndISO3(self, start, final, data, textFeatures):
        iso = data["iso"]
        iso3 = data["iso3"]
        if iso in textFeatures or iso3 in textFeatures:
            return []
        return [(start + " (" + iso + "/" + iso3 + ")" + final)]

    def pattern_countryWithNeighbours(self, start, final, data, textFeatures):
        neighbours = data["neighbours"]
        if len(neighbours) == 0:
            return []

        actual = []
        for n in neighbours:
            name = self.countries[n]["name"]
            if name not in textFeatures:
                actual.append(name)

        if len(actual) == 0:
            return []

        n1 = ", ".join(actual[: len(actual) - 1])
        n2 = actual[len(actual) - 1]
        if len(n1) > 0:
            n2 = " and " + n2
        return [(start + ", a country neighbouring " + n1 + n2 + final)]

    def pattern_countryWithPrimaryLanguage(self, start, final, data, textFeatures):
        if len(data["languages"]) == 0:
            return []
        lang = data["languages"][0]
        if lang not in self.locales:
            lang = lang.split("-")[0].strip()
        if lang not in self.locales:
            return []

        lang = self.locales[lang]["language"]
        return [
            (start + ", a country speaking primarily the " + lang + " language" + final)
        ]

    def pattern_countryWithNumberOfLanguages(self, start, final, data, textFeatures):
        num_languages = len(data["languages"])
        if num_languages == 0:
            return []
        s = ""
        if num_languages > 1:
            s = "s"
        return [
            (
                start
                + ", a country with "
                + str(num_languages)
                + " spoken language"
                + s
                + final
            )
        ]

    def pattern_countryWithSpokenLanguages(self, start, final, data, textFeatures):
        num_languages = len(data["languages"])
        if num_languages == 0:
            return []

        actual = []
        for lang in data["languages"]:
            if lang not in self.locales:
                lang = lang.split("-")[0].strip()
            if lang in self.locales:
                actual.append(self.locales[lang]["language"])

        if len(actual) == 0:
            return []

        n1 = ", ".join(actual[: len(actual) - 1])
        n2 = actual[len(actual) - 1]
        if len(n1) > 0:
            n2 = " and " + n2

        num_languages = len(actual)
        # if there is only 1 language this will be the primary language => no need to write it again
        if num_languages < 2:
            return []

        s = ""
        if num_languages > 1:
            s = "s"

        return [
            (
                start
                + ", a country with the "
                + str(num_languages)
                + " most spoken language"
                + s
                + " being "
                + n1
                + n2
                + final
            )
        ]

    def generateCountry(self, feature, start, final, data, textFeatures):
        result = []

        result += self.pattern_countryInContinent(start, final, data, textFeatures)
        result += self.pattern_countryInContinentWithPopulation(
            start, final, data, textFeatures
        )
        result += self.pattern_countryWithCapital(start, final, data, textFeatures)
        result += self.pattern_countryInContinentWithPopulationAndCapital(
            start, final, data, textFeatures
        )
        result += self.pattern_countryWithISO(start, final, data, textFeatures)
        result += self.pattern_countryWithISO3(start, final, data, textFeatures)
        result += self.pattern_countryWithISOAndISO3(start, final, data, textFeatures)
        result += self.pattern_countryWithNeighbours(start, final, data, textFeatures)
        result += self.pattern_countryWithPrimaryLanguage(
            start, final, data, textFeatures
        )
        result += self.pattern_countryWithNumberOfLanguages(
            start, final, data, textFeatures
        )
        result += self.pattern_countryWithSpokenLanguages(
            start, final, data, textFeatures
        )

        return result

    def pattern_cityInCountry(self, start, final, data, textFeatures):
        country = self.countries[data["country"]]["name"]
        if country in textFeatures:
            return []
        return [(start + ", a city in " + country + final)]

    def pattern_cityWithPopulation(self, start, final, data, textFeatures):
        population = "{:,}".format(int(data["population"]))
        # if country in textFeatures: return []
        return [(start + ", a city with a population of " + population + final)]

    def pattern_cityInCountryWithPopulation(self, start, final, data, textFeatures):
        country = self.countries[data["country"]]["name"]
        population = "{:,}".format(int(data["population"]))
        if country in textFeatures:
            return []
        return [
            (
                start
                + ", a city in "
                + country
                + ", with a population of "
                + population
                + " inhabitants"
                + final
            )
        ]

    def pattern_cityInContinent(self, start, final, data, textFeatures):
        continent = self.continents[self.countries[data["country"]]["continent"]]
        if continent in textFeatures:
            return []
        return [(start + ", a city in " + continent + final)]

    def pattern_cityInContinentWithPopulation(self, start, final, data, textFeatures):
        continent = self.continents[self.countries[data["country"]]["continent"]]
        population = "{:,}".format(int(data["population"]))
        if continent in textFeatures:
            return []
        return [
            (
                start
                + ", a city in "
                + continent
                + ", with a population of "
                + population
                + " inhabitants"
                + final
            )
        ]

    def pattern_cityCapitalOfCountry(self, city, start, final, data, textFeatures):
        if city not in self.capitals:
            return []
        country = self.capitals[city]["countryName"]
        if country in textFeatures:
            return []
        return [(start + ", the capital of " + country + final)]

    def generateCity(self, feature, start, final, data, textFeatures):
        result = []

        result += self.pattern_cityInCountry(start, final, data, textFeatures)
        result += self.pattern_cityWithPopulation(start, final, data, textFeatures)
        result += self.pattern_cityInCountryWithPopulation(
            start, final, data, textFeatures
        )
        result += self.pattern_cityInContinent(start, final, data, textFeatures)
        result += self.pattern_cityInContinentWithPopulation(
            start, final, data, textFeatures
        )
        result += self.pattern_cityCapitalOfCountry(
            feature, start, final, data, textFeatures
        )

        return result

    def generate(self, sentence: str):
        result = []

        try:
            tokens = nltk.word_tokenize(sentence)
        except LookupError:
            nltk.download("punkt")
            tokens = nltk.word_tokenize(sentence)

        textFeatures = {}

        # First extract the GeoNames features existing in text
        # This will be used both for enhancing the text and for preventing inserting duplicates
        for i in range(len(tokens)):
            for j in reversed(range(1, min(6, len(tokens) - i + 1))):
                s = " ".join(tokens[i : i + j])
                if not s[0].isupper():
                    continue

                if s in self.countriesName:
                    textFeatures[s] = {"from": i, "to": i + j, "type": "country"}
                    break
                elif s in self.cities:
                    textFeatures[s] = {"from": i, "to": i + j, "type": "city"}
                    break
                elif s in self.continents:
                    textFeatures[s] = {"from": i, "to": i + j, "type": "continent"}
                    break
                elif len(s) == 2 and s.isupper():
                    textFeatures[s] = {"type": "iso"}
                    break
                elif len(s) == 3 and s.isupper():
                    textFeatures[s] = {"type": "iso3"}
                    break

        # Iterate through all identified features and perform text augmentation
        for feature, featureData in textFeatures.items():
            # Augment countries
            if featureData["type"] == "country":
                data = self.countriesName[feature]
                start = " ".join(tokens[0 : featureData["to"]])
                final = " ".join(tokens[featureData["to"] :]).strip()
                if len(final) > 0:
                    final = ", " + final

                result += self.generateCountry(
                    feature, start, final, data, textFeatures
                )

                continue

            # Augment cities
            if featureData["type"] == "city":
                data = self.cities[feature]
                start = " ".join(tokens[0 : featureData["to"]])
                final = " ".join(tokens[featureData["to"] :]).strip()
                if len(final) > 0:
                    final = ", " + final

                result += self.generateCity(feature, start, final, data, textFeatures)

        return result


"""
# Sample code to demonstrate usage. Can also assist in adding test cases.
# You don't need to keep this code in your transformation.
"""
if __name__ == "__main__":
    import json
    from TestRunner import convert_to_snake_case

    tf = GeoNamesTransformation(max_outputs=3)
    # sentence = "Bucharest is the largest city in Romania" # Antigua and Barbuda"
    # sentence = "Klaus Iohannis is the current president of Romania"

    # for x in tf.generate(sentence):
    #    print(x)

    # exit(-1)

    test_cases = []
    for sentence in [
        "Bucharest is a large city",
        "Klaus Iohannis is the current president of Romania",
        "Romania and the United States have trade agreements",
        "Mangalia is situated on the shores of the Black Sea",
        "Egypt has many pyramids",
    ]:
        test_cases.append(
            {
                "class": tf.name(),
                "inputs": {"sentence": sentence},
                "outputs": [{"sentence": o} for o in tf.generate(sentence)],
            }
        )
    json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
    print(json.dumps(json_file))
"""
"""
