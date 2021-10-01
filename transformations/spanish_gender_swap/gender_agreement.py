import json
import os

gazeteer_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "gazeteer"
)

with open(os.path.join(gazeteer_dir, "auxiliary.json"), "r") as fd:
    auxiliary = json.load(fd)

auxiliary_subject_agreement = (
    auxiliary["ser"] + auxiliary["estar"] + auxiliary["seguir"]
)

with open(
    os.path.join(gazeteer_dir, "gender_country", "male2country.json"), "r"
) as fd:
    male2country = json.load(fd)

with open(
    os.path.join(gazeteer_dir, "gender_country", "country_gender_names.json"),
    "r",
) as fd:
    country_gender_names = json.load(fd)

noun_files = [
    "inflections-fixed.txt",
    "inflections-wiktionary.txt",
    "gentilicios.txt",
    "comunes.txt",
    "anglicismos.txt",
    "inflections-fixed_p.txt",
    "inflections-wiktionary_p.txt",
    "gentilicios_p.txt",
    "comunes_p.txt",
    "anglicismos_p.txt",
]

nouns = []
for f in noun_files:
    with open(os.path.join(gazeteer_dir, f)) as fd:
        m_f = fd.readlines()
        m_f = [tuple(i.strip().split("\t")) for i in m_f]
        nouns.extend(m_f)

m2f_nouns = dict(nouns)

adjective_files = ["adjectives.txt", "adjectives_p.txt"]
adjectives = []
for f in adjective_files:
    with open(os.path.join(gazeteer_dir, f)) as fd:
        m_f = fd.readlines()
        m_f = [tuple(i.strip().split("\t")) for i in m_f]
        adjectives.extend(m_f)
m2f_adjectives_animate_only = dict(adjectives)

# It helps to use these explicitly in case the POS tagger makes mistakes.
# (e.g., "tuyo" in "Ese jugador es un primo tuyo.")
unambiguous_pronouns = [
    "tuyo",
    "mío",
    "tuyos",
    "míos",
    "nuestros",
    "nuestro",
    "vuestro",
    "vuestros",
    "suyo",
    "suyos",
]

# TODO clitic pronouns lo, le, la, les, las, etc -- deal with these separately.
function_m2f = {
    "del": "de la",
    "al": "a la",
    "este": "esta",
    "estos": "estas",
    "ese": "esa",
    "esos": "esas",
    "aquel": "aquella",
    "aquellos": "aquellas",
    "el": "la",
    "los": "las",
    "un": "una",
    "unos": "unas",
    "uno": "una",
    "mi": "mi",
    "mis": "mis",
    "tu": "tu",
    "tus": "tus",
    "su": "su",
    "sus": "sus",
    "nuestro": "nuestra",
    "nuestros": "nuestras",
    "vuestro": "vuestra",
    "vuestros": "vuestras",
    "suyo": "suya",
    "suyos": "suyas",
    "mío": "mía",
    "míos": "mías",
    "tuyos": "tuyas",
    "tuyo": "tuya",
    "vosotros": "vosotras",
    "nosotros": "nosotras",
    "ellos": "ellas",
    "él": "ella",
    "muchos": "muchas",
    "muchísimos": "muchísimas",
    "muchisimos": "muchisimas",
    "pocos": "pocas",
    "cierto": "cierta",
    "ciertos": "ciertas",
    "algunos": "algunas",
    "algún": "alguna",
    "ningún": "ninguna",
    "ninguno": "ninguna",
    "ningunos": "ningunas",
    "todo": "toda",
    "todos": "todas",
    "tanto": "tanta",
    "tantos": "tantas",
    "cuantos": "cuantas",
    "cuántos": "cuántas",
    "cuánto": "cuánta",
    "otro": "otra",
    "otros": "otras",
    "varios": "varias",
    "demasiados": "demasiadas",
    "diversos": "diversas",
    "escaso": "escasa",
    "escasos": "escasas",
    "propios": "propias",
    "cuyo": "cuya",
    "cuyos": "cuyas",
    "mismo": "misma",
    "mismos": "mismas",
    "mismísimo": "mismísimo",
    "mismísimos": "mismísimas",
    "ningún": "ninguna",
    "ninguno": "ninguna",
    "medio": "media",
    "medios": "medias",
    "ambos": "ambas",
    "que": "que",
    "qué": "qué",
}


def path_to_word_exists(
    token,
    replacements,
    dep_relation_list=["det", "conj", "amod", "nmod", "nsubj"],
):

    """Returns True if there is a path in the dependency tree from the
    token to any word in the list of existing replacements, but only following
    paths with labels in the list `dep_relation_list`.
    """

    connected_list = []
    while token.dep_ in dep_relation_list:
        A = token.head.i in replacements and token.dep_ in dep_relation_list
        connected_list.append(A)
        token = token.head
    return any(connected_list)


def change_participle(verb):
    if verb[-1] == "o":
        return verb[:-1] + "a"
    elif verb[-2:] == "os":
        return verb[:-2] + "as"
    else:
        print("What kind of verb is this: ", verb)
        return verb


def check_change_verb(token, doc, replacements):
    """Check to see if the participle should be changed. Note this is
    sometimes tagged as an adjective.

    """
    is_participle = token.pos_ in ["VERB", "ADJ"] and token.morph.get(
        "VerbForm"
    ) == ["Part"]
    # Note we can only change the gender when the participle forms part
    # of a passive periphrastic construction (like [ser/estar] + participle); see
    # https://www.rae.es/dpd/ayuda/terminos-linguisticos or
    # and Castillo Peña, C. (2016). La concordancia en las primeras gramáticas del español para italianos.
    # and Luque, R. (2015). La traducción de las perífrasis de infinitivo del español al italiano.
    if token.i < 2:
        return False  # Don't change the verb in this silly case.
    else:
        prev_token = doc[token.i - 1]
        prev_token_auxsubj = (
            prev_token.pos_ in ["AUX"]
            and prev_token.text in auxiliary_subject_agreement
        )

        is_subject = [
            x
            for x in token.children
            if x.i in replacements
            and x.pos_ in ["NOUN", "PROPN", "PRON"]
            and x.dep_ == "nsubj"
        ]

        return is_participle and prev_token_auxsubj and len(is_subject) != 0


# NOTE: it would be harder to swap from female to male, since many adjectives
# that agree with male nouns also end in "a", e.g., "belga".
def adjective_male_to_female(adjective):
    """Changes the gender of an adjective from male to female using some
    simple rules.
    """

    # Many color adjectives have fixed gender; some that don't are
    # morado, cerúleo, rojo, amarillo, castaño, pardo, negro, blanco.
    invariables = [
        "cortés",
        "corteses",
        "descortés",
        "descorteses" "exjuez",
        "mayor",
        "mayores",
        "menor",
        "menores",
        "mejor",
        "mejores",
        "peor",
        "peores",
        "inferior",
        "inferiores",
        "superior",
        "superiores",
        "exterior",
        "exteriores",
        "anterior",
        "anteriores",
        "posterior",
        "posteriores",
        "gran",
        "marrón",
        "índigo",
        "amaranto",
        "carmín",
        "burdeos",
        "bermellón",
        "verdeceledón",
        "salmón",
        "limón",
        "ámbar",
        "topacio",
        "sésamo",
        "durazno",
        "marengo",
        "hueso",
        "marfil",
        "oro",
    ]

    # NOTE: strictly speaking, "andaluz" and "marfuz" are not exceptions, but
    # there aren't any other gendered adjectives ending in "uz".
    exceptions = {
        "buen": "buena",
        "primer": "primera",
        "mal": "mala",
        "tercer": "tercera",
        "andaluz": "andaluza",
        "marfuz": "marfuza",
        "andaluces": "andaluzas",
    }

    if adjective in invariables:
        return adjective
    elif adjective in exceptions:
        return exceptions[adjective]
    else:
        if adjective.endswith(("or", "ol")):  # fumador, mongol
            return adjective + "a"
        elif adjective.endswith("ón"):  # llorón
            return adjective[:-2] + "ona"
        elif adjective.endswith("án"):  # charlatán
            return adjective[:-2] + "ana"
        elif adjective.endswith("ín"):  # malandrín, pequeñín
            return adjective[:-2] + "ina"
        elif adjective.endswith("és"):  # inglés
            return adjective[:-2] + "esa"
        elif adjective.endswith(("ete", "ote")):  # regordete, grandote
            return adjective[:-1] + "a"
        elif adjective.endswith(("etes", "otes")):  # regordetes, grandotes
            return adjective[:-2] + "as"
        elif adjective.endswith(
            ("ores", "oles", "ones", "anes", "ines", "eses")
        ):
            return adjective[:-2] + "as"
        elif adjective.endswith("ces"):  # felices, veloces
            return adjective
        elif adjective.endswith("os"):  # ambiciosos
            return adjective[:-2] + "as"
        elif adjective.endswith("o"):  # ambicioso
            return adjective[:-1] + "a"
        else:
            return adjective
