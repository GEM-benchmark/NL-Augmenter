if __name__ == "__main__":
    import json
    from transformations.spellchecker_perturbation import SpellCheckerPerturbation

    tf = SpellCheckerPerturbation()
    # sentence = "Andrew finally returned the French book to Chris that I bought last week"
    test_cases = []
    for sentence in [
        "This is one of the sample test cases for the task",
        "Andrew finally returned the French book to Chris that I bought last week",
        "Sentences with gapping, such as Paul likes coffee and Mary tea, lack an overt predicate to indicate the relation between two or more arguments.",
        "Alice in Wonderland is a 2010 American live-action/animated dark fantasy adventure film",
        "Ujjal Dev Dosanjh served as 33rd Premier of British Columbia from 2000 to 2001",
        "Neuroplasticity is a continuous processing allowing short-term, medium-term, and long-term remodeling of the neuronosynaptic organization.",
    ]:
        test_cases.append(
            {
                "class": tf.name(),
                "inputs": {"sentence": sentence},
                "outputs": {"sentence": tf.generate(sentence)},
            }
        )
    json_file = {"type": tf.name(), "test_cases": test_cases}
    print(json.dumps(json_file))
