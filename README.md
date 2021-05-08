# A Repository of Perturbations and Adversaries 🦎 → 🐍

The Perturbation Repository is a collaborative effort intended to accumulate all transformations operating over tasks dealing with natural language. We invite submissions of perturbations and transformations via pull requests to this GitHub repository. 
Every contribution of a perturbation should either add noise to the input or paraphrase or transform the input. 

# Tasks
```python
class TaskType(enum.Enum):
    TEXT_CLASSIFICATION = 1,
    TEXT_TO_TEXT_GENERATION = 2,
    TEXT_TAGGING = 3,
    DIALOGUE_TO_TEXT = 4,
    TABLE_TO_TEXT = 5,
    RDF_TO_TEXT = 6,
    RDF_TO_RDF = 7
```

#### Install and Generate the Test Sets
```bash
pip install -r requirements.txt
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.2.0/en_core_web_sm-2.2.0.tar.gz
```

```bash
python main.py
```
Running it for the first time will take a while (depending on your internet speed) since the translation models need to be downloaded.

After you make any change, run test_main.py once to ensure that your changes don't regress anything.

```bash
python test_main.py
```
 
And for any new logic, add the appropriate test case so that no one else breaks the changes. 
