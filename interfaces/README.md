### Supported Interfaces

The following is a list of currently supported interfaces. 

| Interface                             | Description                                                                       | Tasks                               | Default Evaluation Models & Datasets
| ----------                            | -----------                                                                       | -----                               | -----
| `SentenceTransformation`              | Expects a text as input and return of a transformed piece of text.                | Text Classification, T2T Generation | ("aychang/roberta-base-imdb", "imdb")
| `SentenceAndTargetTransformation`     | Expects a source and a target text as inputs and return of their transformations. | Text-to-Text Generation             |
| `KeyValuePairsTransformation`         | Expects key-value pairs as input and returns a piece of text as output.           | AMR-to-Text, E2E Task               |
| `RDFTransformation`                   | Expects an RDF triplet as input and returns a piece of RDF triplet as output.     | RDF-to-Text Generation              |
| `QuestionAnswerTransformation`        | Expects a question answering example as input and returns its transformation.     | QA, QG                              | ("mrm8488/bert-tiny-5-finetuned-squadv2", "squad")

We welcome pull-requests of newer interfaces. To add a new interface, follow the below steps:
1) Create a new module like "YourInterface.py" in the interfaces folder
2) Inside this python module (or python file), define your interface with the appropriate inputs for the generate function.
    ```python
    class YourInterface(abc.ABC):
    ``` 
    A good idea would be to look at existing interfaces like 'SentenceTransformation'
3) [Optional] Now, you can create a transformation corresponding to this interface with the usual steps mentioned [on the main page](../README.md)
4) [Optional] To gauge the effectiveness of your transformation, you can call a HuggingFace model and evaluate it over a HuggingFace dataset
by writing your own function `def evaluate_my_task` in the file `evaluation_engine.py` and calling that function from the function `execute_model`.
Hurrah! That's it! You can now measure your transformation with the simple command
    ```bash
    python evaluate.py -t my_transformation
    ```