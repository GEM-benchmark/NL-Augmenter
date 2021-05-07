import enum


class TaskType(enum.Enum):
    TEXT_CLASSIFICATION = 1,
    TEXT_TO_TEXT_GENERATION = 2,
    TEXT_TAGGING = 3,  # This would require the inputs to be in ConnLL like format
    DIALOGUE_TO_TEXT = 4,
    TABLE_TO_TEXT = 5,
    RDF_TO_TEXT = 6,
    RDF_TO_RDF = 7
