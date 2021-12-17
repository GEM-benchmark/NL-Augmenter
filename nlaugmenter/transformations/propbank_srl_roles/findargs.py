def perturb_text(s: str, sentence: str):
    perturbed_texts = []
    desc = sentence

    # case1:
    if desc.__contains__("ARGM-COM") and desc.__contains__("ARGM-TMP"):
        perturbed_texts.append(exchange_args(s, desc, "ARGM-COM", "ARGM-TMP"))

    # case2:
    if (
        desc.__contains__("ARG0")
        and desc.__contains__("ARGM-TMP")
        and desc.find("ARGM-TMP") > desc.find("ARG0")
    ):
        perturbed_texts.append(agr2_before_arg1(s, desc, "ARG0", "ARGM-TMP"))

    # case3:
    if (
        desc.__contains__("ARG0")
        and desc.__contains__("ARGM-LOC")
        and desc.find("ARGM-LOC") > desc.find("ARG0")
    ):
        perturbed_texts.append(agr2_before_arg1(s, desc, "ARG0", "ARGM-LOC"))

    # case4:
    if (
        desc.__contains__("ARG1")
        and desc.__contains__("ARGM-LOC")
        and desc.find("ARGM-LOC") > desc.find("ARG1")
    ):
        perturbed_texts.append(agr2_before_arg1(s, desc, "ARG1", "ARGM-LOC"))

    # case5:
    if (
        desc.__contains__("ARG1")
        and desc.__contains__("ARGM-TMP")
        and desc.find("ARGM-TMP") > desc.find("ARG1")
    ):
        perturbed_texts.append(agr2_before_arg1(s, desc, "ARG1", "ARGM-TMP"))

    # case6:
    if (
        desc.__contains__("ARG0")
        and desc.__contains__("ARGM-PRP")
        and desc.find("ARGM-PRP") > desc.find("ARG0")
    ):
        perturbed_texts.append(agr2_before_arg1(s, desc, "ARG1", "ARGM-TMP"))

    # case7:
    if (
        desc.__contains__("ARG0")
        and desc.__contains__("ARGM-CAU")
        and desc.find("ARGM-CAU") > desc.find("ARG0")
    ):
        perturbed_texts.append(agr2_before_arg1(s, desc, "ARG1", "ARGM-CAU"))

    # case8:
    if (
        desc.__contains__("ARG0")
        and desc.__contains__("ARGM-GOL")
        and desc.find("ARGM-GOL") > desc.find("ARG0")
    ):
        perturbed_texts.append(agr2_before_arg1(s, desc, "ARG1", "ARGM-GOL"))

    # case9:
    if desc.__contains__("ARGM-TMP") and desc.__contains__("ARGM-PRP"):
        perturbed_texts.append(exchange_args(s, desc, "ARGM-TMP", "ARGM-PRP"))

    # case10:
    if desc.__contains__("ARGM-TMP") and desc.__contains__("ARGM-CAU"):
        perturbed_texts.append(exchange_args(s, desc, "ARGM-TMP", "ARGM-CAU"))

    return perturbed_texts


def exchange_args(s, desc, arg1, arg2):
    start = desc.find(arg1) + len(arg1) + 2
    end = desc.find("]", start)
    s1 = desc[start:end]

    start = desc.find(arg2) + len(arg2) + 2
    end = desc.find("]", start)
    s2 = desc[start:end]

    # s1 <--> s2
    t = s.replace(s2, "xxxx")
    u = t.replace(s1, s2)
    s = u.replace("xxxx", s1)

    s = s[0].upper() + s[1:]

    return s


def agr2_before_arg1(s, desc, arg1, arg2):
    start = desc.find(arg1) + len(arg1) + 2
    end = desc.find("]", start)
    s1 = desc[start:end]

    start = desc.find(arg2) + len(arg2) + 2
    end = desc.find("]", start)
    s2 = desc[start:end]

    # s1 -> s2 + s1
    # s2 -> ""
    t = s.replace(s2, "xxxx")
    u = t.replace(s1, s2 + " " + s1)

    wordlist = u.split()
    newtext = [x for x in wordlist if x not in ["xxxx", "xxxx.", "xxxx,"]]
    s = " ".join(newtext)

    s = s[0].upper() + s[1:]

    return s
