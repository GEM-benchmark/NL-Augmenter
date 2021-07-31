from gender_pairs import SINGULAR_GENDER_PAIRS


def extract_names_genders():
    male_name_file = open("./resources/gender.male.names", "r")
    male_names  = []
    for line in male_name_file:
        male_names.append(line.strip())
    female_name_file = open("./resources/gender.female.names", "r")
    female_names = []
    for line in female_name_file:
        female_names.append(line.strip())

    male_names.extend(SINGULAR_GENDER_PAIRS.keys()) # adding male title, profession and relation
    female_names.extend(SINGULAR_GENDER_PAIRS.values()) # adding female title, profession and relation

    return male_names, female_names






