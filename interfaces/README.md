### Supported Interfaces

The following is a list of currently supported interfaces. 

| Interface                             | Description                                                                       | Tasks                               |
| ----------                            | -----------                                                                       | -----                               |
| `SentenceTransformation`              | Expects a text as input and return of a transformed piece of text.                | Text Classification, T2T Generation |
| `SentenceAndTargetTransformation`     | Expects a source and a target text as inputs and return of their transformations. | Text-to-Text Generation             |
| `DataTransformation`                  | Expects an RDF triplet as input and returns a piece of RDF triplet as output.     | RDF-to-Text Generation              |
| `QuestionAnswerTransformation`        | Expects a question answering example as input and returns its transformation.     | QA, QG                              |

We welcome pull-requests of newer interfaces.   