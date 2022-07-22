import os


def keywords_in_file():
    """
    Loads all the keywords from the keywords.md file. Mainly loads all the words which have an indentation.
    """
    # Set the path of keywords.md
    if "test" in os.getcwd():  # if pytest is executed within test folder
        key_file = os.path.join(
            os.path.dirname(os.getcwd()), "docs/keywords.md"
        )
    else:  # if pytest is executed at nlaugmenter folder (for github actions)
        key_file = os.path.join(os.getcwd(), "docs/keywords.md")

    with open(key_file) as kfile:
        keywords = [
            line.split("`")[1] for line in kfile.readlines() if "  " in line
        ]
        return keywords
