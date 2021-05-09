### Supported Interfaces

The following is a list of supported interfaces. 

| Interface                             | Description                                                                                       | Tasks                               |
| ----------                            | -----------                                                                                       | -----                               |
| `SentenceTransformation`              | Interface which expects a text as input and return of a transformed piece of text.                | Text Classification, T2T Generation |
| `SentenceAndTargetTransformation`     | Interface which expects a source and a target text as inputs and return of their transformations. | Text-to-Text Generation             |
| `DataTransformation`                  | Interface which expects an RDF triplet as input and returns a piece of RDF triplet as output.     | RDF-to-Text Generation              |

We welcome pull-requests of newer interfaces.   