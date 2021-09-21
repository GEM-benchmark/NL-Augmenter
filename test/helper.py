
import json, os
from TestRunner import convert_to_snake_case


def generate_test_cases(transformation, src_sentences=[], print_result=False, output_filename=""):
    """
    Sample code to demonstrate usage that can also assist in adding test cases.
    """

    test_cases = []

    if len(src_sentences) == 0:
        src_sentences = ["Manmohan Singh served as the PM of India.",
                         "Neil Alden Armstrong was an American astronaut.",
                         "Katheryn Elizabeth Hudson is an American singer.",
                         "The owner of the mall is Anthony Gonsalves.",
                         "Roger Michael Humphrey Binny (born 19 July 1955) is an Indian " +
                         "former cricketer."]

    for idx, sent in enumerate(src_sentences):
        outputs = transformation.generate(sent)
        test_cases.append({
            "class": transformation.name(),
            "inputs": {"sentence": sent},
            "outputs": []}
        )
        for out in outputs:
            test_cases[idx]["outputs"].append({"sentence": out})

    json_file = {"type": convert_to_snake_case(transformation.name()),
        "test_cases": test_cases}

    if print_result:
        print(json.dumps(json_file, ensure_ascii=False))

    dir_path = os.path.dirname(os.path.realpath(__file__))

    if len(output_filename) > 0:
        with open(os.path.join(dir_path, output_filename), "w") as f:
            json.dump(json_file, f, indent=2, ensure_ascii=False)

