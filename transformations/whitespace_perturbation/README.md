# Whitespace Perturbation 🦎  + ⌨️ → 🐍
This perturbation adds noise to text by randomly removing or adding whitespaces.

Author name: Xinyi Wu (xinyiwu.nlp@gmail.com)

## What type of a transformation is this?
The transformation removes (with a probability of `remove_prob`) or adds (with a probability of `add_prob`) a whitespace at random positions.

## What tasks does it intend to benefit?
This perturbation would benefit all tasks that require whitespace-dependent tokenizers. Such tokenizers include not only traditianal whitespace tokenzers (e.g., nltk `WhitespaceTokenizer`), but also BPE-based tokenizers, which are widely used in recent pretrained language models (e.g., `BERT`, `RoBERTa`, `GPT`). By removing or adding whitespaces, we could find the same tokenizer results in different sequences of tokens. For example, 
```
>>> from transformers import RobertaTokenizer
>>> tokenizer = RobertaTokenizer.from_pretrained("roberta-base")
>>> tokenizer.tokenize('a whitespace') # original
['a', 'Ġwhites', 'pace']
>>> tokenizer.tokenize('awhitespace') # remove a whitespace
['aw', 'h', 'ites', 'pace']
>>> tokenizer.tokenize('a whi tespace') # add a whitespace
['a', 'Ġwh', 'i', 'Ġt', 'esp', 'ace']
```

**Evaluation**
```python evaluate.py -t WhitespacePerturbation -task TEXT_CLASSIFICATION```
```model_name = "aychang/roberta-base-imdb"```
The accuracy of a RoBERTa model (fine-tuned on IMDB) (model: "aychang/roberta-base-imdb") 
on a subset of IMDB sentiment dataset = 95.74
The accuracy of the same model on the perturbed set (`remove_prob=0.1`, `add_prob=0.05`) = 89.78

## What are the limitations of this transformation?
Some languages do not separate words with whitespaces (e.g., Chinese, Japanese, Thai, etc.). Therefore, we will not be able to remove any whitespaces from proper text in those languages. Adding whitespaces to those languages, however, may or may not change the tokens depending on the specific tokenizer. For example, `一个空格` (`a whitespace` in Chinese) and the perturbed `一个空 格` share the same tokens (`['一', '个', '空', '格']`) after applying the `bert-base-multilingual-cased` tokenizer (character-level BPE), but have slightly different tokens(`['▁', '一个', '空', '格']` vs. `['▁', '一个', '空', '▁', '格']`) after applying the `xlm-roberta-base` tokenizer (byte-level BPE).
