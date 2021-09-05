def keywords_in_file():
    with open("docs/keywords.md") as kfile:
        keywords = [line.split("`")[1] for line in kfile.readlines() if "  " in line]
        print(keywords)
        return keywords