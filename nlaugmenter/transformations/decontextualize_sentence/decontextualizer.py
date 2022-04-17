KEEPARG = [
    "ARG0",
    "ARG1",
    "ARG2",
    "ARG3",
    "ARG4",
    "ARG5",
    "ARG6",
    "ARG7",
    "ARG8",
    "MOD",
    "V",
    "O",
]
punc = """!()-[]{};:'"\,<>./?@#$%^&*_~"""


def decontextualize_text(pred_arg_pair: dict, words: list):
    """
    Given the predicate-argument pair this function removes all the contextual arguments except AM-MOD
    :param pred_arg_pair: Dictionary containing srl tags for each token
    :param words: List of tokenized words
    :return: String
    """
    tags = pred_arg_pair["tags"]
    new_sen = []
    for tokid, tag in enumerate(tags):
        if tag.split("-")[-1] in KEEPARG:
            new_sen.append(words[tokid])
    new_sen = " ".join(new_sen)
    if new_sen[0] in punc:
        new_sen = new_sen[1:]
    new_sen = new_sen.strip()
    return new_sen
