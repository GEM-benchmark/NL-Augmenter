def perturb_text(s: str, sentence: str):
    perturbed_texts = []
    desc = sentence

    # case1:
    if desc.__contains__("[ARGM-COM:") and desc.__contains__("[ARGM-TMP:"):
        start = desc.find("ARGM-TMP:") + 10
        end = desc.find("]", start)
        s1 = desc[start:end]

        start = desc.find("ARGM-COM:") + 10
        end = desc.find("]", start)
        s2 = desc[start:end]

        t = s.replace(s2, "xxxx")
        u = t.replace(s1, s2)
        s = u.replace("xxxx", s1)
        perturbed_texts.append(s)

    # case2:
    if (
        desc.__contains__("[ARG0:")
        and desc.__contains__("[ARGM-TMP:")
        and desc.find("ARGM-TMP:") > desc.find("ARG0:")
    ):
        start = desc.find("ARG0:") + 6
        end = desc.find("]", start)
        s1 = desc[start:end]

        start = desc.find("ARGM-TMP:") + 10
        end = desc.find("]", start)
        s2 = desc[start:end]

        # s1 -> s2 + s1
        # s2 -> ""
        t = s.replace(s2, "xxxx")
        u = t.replace(s1, s2 + " " + s1)
        s = u.replace("xxxx", "")
        perturbed_texts.append(s)

    # case3:
    if (
        desc.__contains__("[ARG0:")
        and desc.__contains__("[ARGM-LOC:")
        and desc.find("ARGM-LOC:") > desc.find("ARG0:")
    ):
        start = desc.find("ARG0:") + 6
        end = desc.find("]", start)
        s1 = desc[start:end]

        start = desc.find("ARGM-LOC:") + 10
        end = desc.find("]", start)
        s2 = desc[start:end]

        # s1 -> s2 + s1
        # s2 -> ""
        t = s.replace(s2, "xxxx")
        u = t.replace(s1, s2 + " " + s1)
        s = u.replace("xxxx", "")
        perturbed_texts.append(s)

    # case4:
    if (
        desc.__contains__("[ARG1:")
        and desc.__contains__("[ARGM-LOC:")
        and desc.find("ARGM-LOC:") > desc.find("ARG1:")
    ):
        start = desc.find("ARG1:") + 6
        end = desc.find("]", start)
        s1 = desc[start:end]

        start = desc.find("ARGM-LOC:") + 10
        end = desc.find("]", start)
        s2 = desc[start:end]

        # s1 -> s2 + s1
        # s2 -> ""
        t = s.replace(s2, "xxxx")
        u = t.replace(s1, s2 + " " + s1)
        s = u.replace("xxxx", "")
        perturbed_texts.append(s)

    # case5:
    if (
        desc.__contains__("[ARG1:")
        and desc.__contains__("[ARGM-TMP:")
        and desc.find("ARGM-TMP:") > desc.find("ARG1:")
    ):
        start = desc.find("ARG1:") + 6
        end = desc.find("]", start)
        s1 = desc[start:end]

        start = desc.find("ARGM-TMP:") + 10
        end = desc.find("]", start)
        s2 = desc[start:end]

        # s1 -> s2 + s1
        # s2 -> ""
        t = s.replace(s2, "xxxx")
        u = t.replace(s1, s2 + " " + s1)
        s = u.replace("xxxx", "")
        perturbed_texts.append(s)

    return perturbed_texts
