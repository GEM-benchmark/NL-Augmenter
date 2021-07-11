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

    def loadCountries(self):
        self.countries = {}
        self.countriesName = {}

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
                # 4 = name
                # 5 = capital
                # 7 = population
                # 8 = continent
                # 11 = currency name

                self.countries[line[0]] = {
                    "name": line[4],
                    "capital": line[5],
                    "population": line[7],
                    "continent": line[8],
                    "currency": line[11],
                }

                self.countriesName[line[4]] = {
                    "capital": line[5],
                    "population": line[7],
                    "continent": line[8],
                    "currency": line[11],
                }

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

    def generate(self, sentence: str):
        result = []

        try:
            tokens = nltk.word_tokenize(sentence)
        except LookupError:
            nltk.download("punkt")
            tokens = nltk.word_tokenize(sentence)

        for i in range(len(tokens)):
            for j in reversed(range(1, min(6, len(tokens) - i + 1))):
                s = " ".join(tokens[i : i + j])
                if not s[0].isupper():
                    continue

                if s in self.countriesName:
                    data = self.countriesName[s]
                    start = " ".join(tokens[0 : i + j])
                    final = " ".join(tokens[i + j :]).strip()
                    if len(final) > 0:
                        final = ", " + final

                    new_sent = (
                        start
                        + ", a country in "
                        + self.continents[data["continent"]]
                        + final
                    )
                    result.append(new_sent)

                    new_sent = (
                        start
                        + ", a country in "
                        + self.continents[data["continent"]]
                        + ", with a population of "
                        + "{:,}".format(int(data["population"]))
                        + " inhabitants"
                        + final
                    )
                    result.append(new_sent)

                    new_sent = (
                        start + ", whose capital city is " + data["capital"] + final
                    )
                    result.append(new_sent)

                    new_sent = (
                        start
                        + ", a country in "
                        + self.continents[data["continent"]]
                        + ", with a population of "
                        + "{:,}".format(int(data["population"]))
                        + " inhabitants, with the capital at "
                        + data["capital"]
                        + final
                    )
                    result.append(new_sent)

                    continue

                if s in self.cities:
                    # print("s=[%s]"%(s))
                    data = self.cities[s]
                    start = " ".join(tokens[0 : i + j])
                    final = " ".join(tokens[i + j :]).strip()
                    if len(final) > 0:
                        final = ", " + final

                    new_sent = (
                        start
                        + ", a city in "
                        + self.countries[data["country"]]["name"]
                        + final
                    )
                    result.append(new_sent)

                    new_sent = (
                        start
                        + ", a city with a population of "
                        + "{:,}".format(int(data["population"]))
                        + final
                    )
                    result.append(new_sent)

                    new_sent = (
                        start
                        + ", a city in "
                        + self.countries[data["country"]]["name"]
                        + ", with a population of "
                        + "{:,}".format(int(data["population"]))
                        + " inhabitants"
                        + final
                    )
                    result.append(new_sent)

                    new_sent = (
                        start
                        + ", a city in "
                        + self.continents[self.countries[data["country"]]["continent"]]
                        + final
                    )
                    result.append(new_sent)

                    new_sent = (
                        start
                        + ", a city in "
                        + self.continents[self.countries[data["country"]]["continent"]]
                        + ", with a population of "
                        + "{:,}".format(int(data["population"]))
                        + " inhabitants"
                        + final
                    )
                    result.append(new_sent)

        return result


"""
# Sample code to demonstrate usage. Can also assist in adding test cases.
# You don't need to keep this code in your transformation.
"""
if __name__ == "__main__":
    import json
    from TestRunner import convert_to_snake_case

    tf = GeoNamesTransformation(max_outputs=3)
    # sentence = "Bucharest is the largest city in Romania"
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
