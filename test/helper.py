import json

from nlaugmenter.evaluation.TestRunner import convert_to_snake_case


def generate_test_cases(
    transformation, src_sentences=[], print_result=False, output_path=""
):
    """
    Sample code to demonstrate usage that can also assist in adding test cases.

    :param transformation: a transformation object.
    :param src_sentences: a list of input sentences (if empty, the default sentences are used).
    :param print_results: indicates whether to print the content of the output file to stdout.
    :param output_path: the path to the output JSON file used to store the generated test cases.
    """

    test_cases = []

    if len(src_sentences) == 0:
        src_sentences = [
            "Manmohan Singh served as the PM of India.",
            "Neil Alden Armstrong was an American astronaut.",
            "Katheryn Elizabeth Hudson is an American singer.",
            "The owner of the mall is Anthony Gonsalves.",
            "Roger Michael Humphrey Binny (born 19 July 1955) is an Indian "
            + "former cricketer.",
        ]

    for idx, sent in enumerate(src_sentences):
        outputs = transformation.generate(sent)
        test_cases.append(
            {
                "class": transformation.name(),
                "inputs": {"sentence": sent},
                "outputs": [],
            }
        )
        for out in outputs:
            test_cases[idx]["outputs"].append({"sentence": out})

    json_file = {
        "type": convert_to_snake_case(transformation.name()),
        "test_cases": test_cases,
    }

    if print_result:
        print(json.dumps(json_file, ensure_ascii=False))

    if len(output_path) > 0:
        with open(output_path, "w") as f:
            json.dump(json_file, f, indent=2, ensure_ascii=False)
