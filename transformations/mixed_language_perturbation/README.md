# Mixed Language Perturbation 🦎  + ⌨️ → 🐍
This perturbation translates randomly picked words in the text from English to other languages (e.g., German). It can be used to test the robustness of a model in a multilingual setting.

Author names: 
- Genta Indra Winata (giwinata@connect.ust.hk, The Hong Kong University of Science and Technology), 
- Samuel Cahyawijaya (scahyawijaya@connect.ust.hk, The Hong Kong University of Science and Technology)
- Bryan Wilie (bryanwilie92@gmail.com, Institut Teknologi Bandung).

## What type of a transformation is this?
This transformation acts as a perturbation to test robustness. Few words were picked at random with a probability and translated to the target language.

## What tasks does it intend to benefit?
This perturbation would benefit all tasks with a sentence/paragraph/document as input like text classification, text generation, etc.

## Previous Work
(1) Mixed-Language Training (Published in AAAI 2020)
```bibtex
@inproceedings{liu2020attention,
  title={Attention-informed mixed-language training for zero-shot cross-lingual task-oriented dialogue systems},
  author={Liu, Zihan and Winata, Genta Indra and Lin, Zhaojiang and Xu, Peng and Fung, Pascale},
  booktitle={Proceedings of the AAAI Conference on Artificial Intelligence},
  volume={34},
  number={05},
  pages={8433--8440},
  year={2020}
}
```
(2) Continual Mixed-Language Pre-Training (Accepted in ACL Findings 2021)
```
@article{liu2021continual,
  title={Continual Mixed-Language Pre-Training for Extremely Low-Resource Neural Machine Translation},
  author={Liu, Zihan and Winata, Genta Indra and Fung, Pascale},
  journal={arXiv preprint arXiv:2105.03953},
  year={2021}
}
```

## What are the limitations of this transformation?
The transformation's outputs are dependent on the accuracy of the individual translation models and generally would generate simpler text or more popularly used text.
