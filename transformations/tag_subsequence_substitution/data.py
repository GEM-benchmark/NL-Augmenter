from datasets import load_dataset

conll03_dataset = load_dataset("conll2003")
id2name = conll03_dataset["train"].features["pos_tags"].feature.names
example_dataset = [
    (x, [id2name[z] for z in y])
    for x, y in zip(
        conll03_dataset["train"]["tokens"],
        conll03_dataset["train"]["pos_tags"],
    )
]
