import random

from interfaces.SentenceOperation import SentenceAndTargetOperation
import spacy
from tasks.TaskTypes import TaskType

"""
Motivation: Causal relations are sensitive to negations and strength, and 
misinterpretation could lead to drastic conclusions. Models trained on corpus 
without minimally augmented negated sentences mistakenly categorize a sentence
as causal even though the sentence is negated (E.g. He did not cause her to fall.).

Source: This transformation is targetted at augmenting Causal Relations in text and 
adapts the code from paper 'Causal Augmentation for Causal Sentence Classification' 
at https://openreview.net/pdf/17eafef9e25b48eb90a9a7f32c4f52e21177cc73.pdf.

Test: Original test sentences are based on corpus AltLex (Hidey et al, 2016) 
(https://github.com/chridey/altlex) and PubMed by (Yu et al, 2019)
(https://github.com/junwang4/causal-language-use-in-science). More expected examples 
and output grouped by grammar method is available in the Appendix of the code paper.

Note: This augment may work for general relations too. 
E.g. "She is related to John" --> "She is not related to John."
"""

class NegateStrengthen(SentenceAndTargetOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.SENTIMENT_ANALYSIS]
    languages = ["en"]
    tgt_languages = ["en"]

    def __init__(self, seed=0):
        super().__init__(seed)
        self.nlp = spacy.load("en_core_web_sm")
        self.seed = seed
        random.seed(self.seed)

    def generate(self, sentence: str, target: str):

        print('>>>>>>> sentence: ',sentence)
        print('>>>>>>> target: ',target)

        # perturbed_sentences = []
        # perturbed_targets = []


        # perturbed_sentences.append(sentence) 
        # perturbed_targets.append(target)

        # if self.verbose:
        #     print(
        #         f"Perturbed Input from {self.name()} : \nSource: {perturbed_sentences}\nLabel: {perturbed_targets}"
        #     )
        
        perturbed_items  = [(sentence, target)]

        return perturbed_items


"""
# Sample code to demonstrate adding test cases.
if __name__ == '__main__':
    tf = SentimentEmojiAugmenter()
    test_cases = []
    src = ["The dog was happily wagging its tail.", "Ram und Sita waren glücklich verheiratet.",
                                                    "Le film était bien meilleur que les 100 derniers que j'ai regardés !",
           "這部電影比我最近看的 100 部要好得多！",
           "भारत आणि कॅनडा चांगले मित्र आहेत.", "Tujuh orang terluka!",
           "அது மிக மோசமான படம், அதற்கு நான் மீண்டும் பணம் கொடுக்கவில்லை."]
    tgt = ["pos", "pos", "pos", "pos", "pos", "neg", "neg"]
    for sentence, target in zip(src, tgt):
        sentence_o, target_o = tf.generate(sentence, target)
        test_cases.append({
            "class": tf.name(),
            "inputs": {"sentence": sentence, "target": target},
            "outputs": {"sentence": sentence_o, "target": target_o}}
        )
    json_file = {"type": tf.name(), "test_cases": test_cases}
    print(str(json_file))
""" 