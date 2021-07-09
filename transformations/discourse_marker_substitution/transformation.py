import random
import re

from collections import defaultdict
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

"""
Substitution of discourse markers with semantically equivalent marker
"""

MARKER_TO_CLASS = {
    "accordingly,": "Contingency.Cause.Result",
    "additionally,": "Expansion.Conjunction",
    "also,": "Expansion.Conjunction",
    "and,": "Expansion.Conjunction",
    "as a result": "Contingency.Cause.Result",
    "at the same time": "Temporal.Synchrony",
    "at the time": "Temporal.Synchrony",
    "because": "Contingency.Cause.Reason",
    "besides": "Expansion.Conjunction",
    "but,": "Comparison.Contrast",
    "consequently": "Contingency.Cause.Result",
    "earlier": "Temporal.Asynchronous.Succession",
    "finally": "Temporal.Asynchronous.Precedence",
    "for example": "Expansion.Instantiation",
    "for instance": "Expansion.Instantiation",
    "further": "Expansion.Conjunction",
    "furthermore": "Expansion.Conjunction",
    "hence": "Contingency.Cause.Result",
    "however,": "Comparison.Contrast",
    "in addition,": "Expansion.Conjunction",
    "in fact,": "Expansion.Conjunction",
    "in particular": "Expansion.Restatement.Specification",
    "in turn,": "Expansion.Conjunction",
    "inasmuch as": "Contingency.Cause.Reason",
    "later": "Temporal.Asynchronous.Precedence",
    "likewise": "Expansion.Conjunction",
    "meanwhile": "Expansion.Conjunction",
    "moreover": "Expansion.Conjunction",
    "on the contrary": "Comparison.Contrast",
    "previously": "Temporal.Asynchronous.Succession",
    "similarly": "Expansion.Conjunction",
    "since": "Contingency.Cause.Reason",
    "so,": "Contingency.Cause.Result",
    "specifically": "Expansion.Restatement.Specification",
    "subsequently": "Temporal.Asynchronous.Precedence",
    "then,": "Temporal.Asynchronous.Precedence",
    "therefore": "Contingency.Cause.Result",
    "thus": "Contingency.Cause.Result",
}

CLASS_TO_MARKERS = defaultdict(list)
for (k, v) in MARKER_TO_CLASS.items():
    CLASS_TO_MARKERS[v].append(k)
CLASS_TO_MARKERS = dict(CLASS_TO_MARKERS)


def discourse_marker_substitution(text, seed=0, max_output=1):
    """Performs a ubstitution of discourse markers with semantically equivalent marker
    in the input text
    """
    random.seed(seed)
    perturbed_texts = []
    for _ in range(max_output):
        present_markers = [m for m in MARKER_TO_CLASS if m in text.lower().split()]

        if not present_markers:
            return [text]
        original = random.choice(present_markers)
        same_class_markers = CLASS_TO_MARKERS[MARKER_TO_CLASS[original]]
        possible_substitutions = [m for m in same_class_markers if m not in original]
        if not possible_substitutions:
            return [text]
        new = random.choice(possible_substitutions)
        matched_markers = list(re.finditer("(?i)" + re.escape(original), text))
        if matched_markers:
            m = random.choice(matched_markers)
            # keep the same case type
            if m[0].isupper():
                new_with_matching_case_type = new.upper()
            elif m[0][0].isupper() and len(m[0]) > 1:
                new_with_matching_case_type = f"{new[0].upper()}{new[1:]}"
            else:
                new_with_matching_case_type = new
            if original.endswith(","):
                new_with_matching_case_type += ","
            perturbed_text = (
                text[: m.start()] + new_with_matching_case_type + text[m.end() :]
            )
            perturbed_texts.append(perturbed_text)
    return list(set(perturbed_texts))


class DiscourseMarkerSubstitution(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
    ]
    languages = ["en"]

    def __init__(self, seed=0, max_output=1):
        super().__init__(seed)
        self.max_output = max_output

    def generate(self, sentence: str):
        perturbed_texts = discourse_marker_substitution(
            text=sentence, seed=self.seed, max_output=self.max_output
        )
        return perturbed_texts
