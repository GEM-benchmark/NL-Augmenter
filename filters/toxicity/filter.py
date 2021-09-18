import enum
import operator

from detoxify import Detoxify

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


class ToxicityTypes(str, enum.Enum):
    TOXICITY = "toxicity"
    SEVERE_TOXICITY = "severe_toxicity"
    OBSCENE = "obscene"
    IDENTITY_ATTACK = "identity_attack"
    INSULT = "insult"
    THREAT = "threat"
    SEXUAL_EXPLICIT = "sexual_explicit"


class ToxicityFilter(SentenceOperation):
    tasks = [TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]
    heavy = True

    def __init__(
        self,
        toxicity_type: ToxicityTypes,
        op: str = ">",
        threshold: float = 0.5,
    ):
        super().__init__()

        self.check_threshold_value(threshold)

        self.type = toxicity_type
        self.operator = self.parse_operator(op)
        self.threshold = threshold
        self.unbiased_model = Detoxify("unbiased")

    @staticmethod
    def parse_operator(op):
        ops = {
            ">": operator.gt,
            "<": operator.lt,
            ">=": operator.ge,
            "<=": operator.le,
            "==": operator.eq,
        }
        return ops[op]

    @staticmethod
    def check_threshold_value(threshold):
        if threshold < 0 or threshold > 1:
            raise ValueError(
                f"Threshold must be in the range [0, 1]. {threshold} provided."
            )

    def filter(self, sentence: str = None) -> bool:
        predictions = self.unbiased_model.predict(sentence)
        toxicity_value = predictions[self.type]
        return self.operator(toxicity_value, self.threshold)
