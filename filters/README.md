### The List of Filters

This directory contains filters that are used to create contrast sets. A list of data points are fed through the filter to match the condition (e.g. the input text length should be above certain threshold, the input text should contain some keywords, etc.). Each subdirectory contains a single filter to construct contrast sets. A summary table of these filters follows.

The following describes the list of filters or conditions which split the dataset into contrast sets.

| Filter                             | Description                                                                       
| ------- | -----------                          
| [TextContainsKeywordsFilter](keywords)              | Selects examples which contain a pre-defined set of keywords.                
| [TextLengthFilter](length)     | Selects sentences/paragraphs of a specified length.


### How to Contribute
1. Create a new folder and a new filter file `filter_folder/filter_name.py`. Remember to import the filter class in the `filter_folder/__init__.py` file, otherwise it may cause error when running the test cases.
2. Implement your filter by inheriting one of the operation [interfaces](../interfaces), and re-write the `filter` method with corresponding input. You might need to specify a default value for the arguments for `filter` and `__init__` method of your filter class. For example:
```
class CustomFilter(Interface):
    tasks = []
    locales = []

    def __init__(self, op: str=None, threshold: int=None):
        ...

    def filter(self, sentence: str=None) -> bool:
        ...
```
3. Add a README file and the `test.json` file under your folder. You can specify the filter initialized with different arguments by adding them in the format of key-value pairs, and similar strategy applies to arguments for the filter method. The output should be either true or false.
```
{
    "type": "length",
    "test_cases": [
        {
            "class": "CostumFilter",
            "args": {
                "arg1": ...,
                "arg2": ...
            },
            "inputs": {
                "sentence": ...
            },
            "outputs": true
        }
    ]
}
```
4. Run your test. Make sure there's no error and make a pull request.