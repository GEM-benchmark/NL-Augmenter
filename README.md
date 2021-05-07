# GEM-special-test-sets
Special Test Sets for the Generation Evaluation Benchmark. Contains data-sets for evaluating the robustness of (1) data-to-text and (2) text-to-text generative models.  


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