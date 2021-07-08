### Supported Interfaces

The following is a list of currently supported interfaces along-with sample transformations. (Note that the same interfaces can be used for creating new filters by implementing ".filter()" instead of ".generate()")

| Interface                             | Description                                                                       | Tasks                               | Example Transformation | Default Evaluation Models & Datasets
| ----------                            | -----------                                                                       | -----                               | -----   | -----
| [`SentenceOperation`](../interfaces/SentenceOperation.py)              | Expects a text as input and return of a transformed piece of text.                | Text Classification, T2T Generation | [`BackTranslation`](../transformations/back_translation)| ("aychang/roberta-base-imdb", "imdb")
| [`SentenceAndTargetOperation`](../interfaces/SentenceOperation.py)      | Expects a source and a target text as inputs and return of their transformations. | Text Classification, T2T Generation             | [`ChangeTwoWayNamedEntities`](../transformations/change_two_way_ne) | ("sshleifer/distilbart-xsum-12-6", "xsum")     
| `KeyValuePairsOperation`          | Expects key-value pairs as input and returns a piece of text as output.           | AMR-to-Text, E2E Task               | -----|
| `RDFOperation`                    | Expects an RDF triplet as input and returns a piece of RDF triplet as output.     | RDF-to-Text Generation              | -----|
| [`QuestionAnswerOperation`](../interfaces/QuestionAnswerOperation.py)         | Expects a question answering example as input and returns its transformation.     | QA, QG                              | [`RedundantContextForQa`](../transformations/redundant_context_for_qa)| ("mrm8488/bert-tiny-5-finetuned-squadv2", "squad")
| [`TaggingOperation`](../interfaces/TaggingOperation.py)         | Expects a list of tokena and a list of tags as input and returns its transformation.     | Tagging                              | [`LongerNamesNer`](../transformations/longer_names_ner)| ("dslim/bert-base-NER", "conll2003")


We also welcome pull-requests of newer interfaces. To add a new interface, follow the below steps:
1) Create a new python file - "YourInterface.py" in the interfaces folder
2) Inside this python file, define a class with the appropriate inputs for the generate and the filter functions.
    ```python
   from interfaces.Operation import Operation
   
   class YourInterface(Operation):
    ``` 
    A good idea would be to look at existing interfaces like [`SentenceOperation`](../interfaces/SentenceOperation.py) and [`QuestionAnswerOperation`](../interfaces/QuestionAnswerOperation.py)
3) [Optional] Now, you can create a transformation and a filter corresponding to `YourInterface` with the usual steps mentioned [on the main page](../README.md)
4) [Optional] To gauge the effectiveness of your transformation, you can call a HuggingFace model and [evaluate](../evaluation) it over a HuggingFace dataset with the following command
    ```bash
    python evaluate.py -t NameOfTransformationClass
    ```
   That's it! You can now measure your transformation with this simple command!
