# Double Context Perturbation 🦎  +   → 🐍
This perturbation acts as an example perturbation for question answering transformations. It adds redundant context to a question answering input.

## What type of a transformation is this?
This transformation acts like a perturbation to test robustness. The context is doubled and the question and the answer are kept unchanged. 
Generated transformations would be highly accurate.

## What tasks does it intend to benefit?
This perturbation would benefit question answering, question generation, etc.

The accuracy of a TinyBert model fine-tuned on SQUAD has exact match accuracy = 60.31
The accuracy of the perturbed set = 58.27
```python
dataset = load_dataset("squad", split='validation[:20%]')
```

## What are the limitations of this transformation?
The transformation is too simple. Also, it might be possible that some event based question answering problems 
might not benefit from this transformation where the role of entities changes over time.