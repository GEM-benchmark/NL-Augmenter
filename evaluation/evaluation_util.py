def get_task_type(implementation, task_type):
    if task_type is None:
        print(
            "Undefined task type, switching to default task %s",
            implementation.tasks[0].name,
        )
        return str(implementation.tasks[0]).split(".")[1]
    return task_type


def convert_ner_ids_to_tags(ner_tags):
    # convert list of ner ids [0,1,2,0] to list of ner tags ['0', 'B-PER', 'I-PER', '0']
    ner_tag_sequence = []
    ner_tag_dict = {
        1: "B-PER",
        2: "I-PER",
        3: "B-ORG",
        4: "I-ORG",
        5: "B-LOC",
        6: "I-LOC",
        7: "B-MISC",
        8: "I-MISC",
    }
    for tag in ner_tags:
        ner_tag_sequence.append(ner_tag_dict.get(tag, "0"))  # '0', tag for no ner token
    return ner_tag_sequence


def create_prediction_seq(prediction, expected_seq_length):
    # create model output into ner tag sequence
    # input : model output in the form [[], [{ner-info}], [{ner-info}], []]
    # output : ['0', 'B-PER', 'I-PER', '0']
    if prediction == []:
        # corner case where model prediction is [] and gold label is not []. ex: example["tokens"] = [',']
        return ["0"] * expected_seq_length
    seq = []
    tag = ""
    for item in prediction:
        if len(item) == 0:
            seq.append("0")
        else:
            if isinstance(item, list):
                tag = item[0]["entity"]
            elif isinstance(item, dict):  # to handle a corner case
                tag = item["entity"]
            seq.append(tag)
    return seq
