def keywords_in_file():
    """
    Loads all the keywords from the keywords.md file. Mainly loads all the words which have an indentation.
    """
    with open("docs/keywords.md") as kfile:
        keywords = [line.split("`")[1] for line in kfile.readlines() if "  " in line]
        return keywords