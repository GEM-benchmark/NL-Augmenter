import enum


class TaskType(enum.Enum):
    TEXT_CLASSIFICATION = (1,) # This would include all - sentiment, emotion, etc.
    TEXT_TO_TEXT_GENERATION = (2,)
    TEXT_TAGGING = (3,)  # This would require the inputs to be in ConnLL like format
    DIALOGUE_ACT_TO_TEXT = (4,)
    TABLE_TO_TEXT = (5,)
    RDF_TO_TEXT = (6,)
    RDF_TO_RDF = (7,)
    QUESTION_ANSWERING = (8,)
    QUESTION_GENERATION = (9,)
    AMR_TO_TEXT = (10,)
    E2E_TASK = (11,)
    SENTIMENT_ANALYSIS = (12,) # This is a specific type of text classification with unique properties
