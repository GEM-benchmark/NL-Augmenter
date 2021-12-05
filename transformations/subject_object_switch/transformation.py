from initialize import initialize_models, spacy_nlp
from interfaces.SentenceOperation import SentenceOperation
from interfaces.SentencePairOperation import SentencePairOperation
from tasks.TaskTypes import TaskType

"""
Subject Object Switch.
    Switches with each other the subject and object of English sentences.
"""


def subject_object_switch(sentence, nlp):

    # Tokenize Sentence
    doc = nlp(sentence)

    # Initialize Variables
    changed = False
    chunks = {}
    new_sentence = []
    root_token = list(doc.sents)[0].root

    # Evaluate Tokens
    for token in doc:

        # Evaluate subjects and objects
        if "subj" in token.dep_ or "obj" in token.dep_:

            # Initialize Variables
            current_chunk = []
            check = [token]

            # Evaluate pending tokens
            while check:
                current_token = check.pop(0)
                current_chunk.append(current_token)

                # Get token children
                for child in current_token.children:
                    check.append(child)

            # Sort by token index
            current_chunk.sort(key=lambda x: x.i)

            # Get chunk position
            index = current_chunk[0].i

            # Add chunk to list
            chunks[index] = current_chunk

    # Naively select candidate objects and subjects
    candidate_subjects = [k for k in chunks.keys() if k < root_token.i]
    candidate_objects = [k for k in chunks.keys() if k > root_token.i]

    # If there are both, naively select a subject and an object
    if candidate_subjects and candidate_objects:
        subject_chunk = chunks[max(candidate_subjects)]
        object_chunk = chunks[min(candidate_objects)]
        changed = True

        # Add tokens in the right order
        new_sentence.extend(doc[i] for i in range(0, subject_chunk[0].i))
        new_sentence.extend(
            doc[i] for i in range(object_chunk[0].i, object_chunk[-1].i)
        )
        new_sentence.extend(
            nlp(object_chunk[-1].text + subject_chunk[-1].whitespace_)
        )
        new_sentence.extend(
            doc[i] for i in range(subject_chunk[-1].i + 1, object_chunk[0].i)
        )
        new_sentence.extend(
            doc[i] for i in range(subject_chunk[0].i, subject_chunk[-1].i)
        )
        new_sentence.extend(
            nlp(subject_chunk[-1].text + object_chunk[-1].whitespace_)
        )
        new_sentence.extend(
            doc[i] for i in range(object_chunk[-1].i + 1, len(doc))
        )

        # Rebuild Sentence
        new_sentence = [t.text + t.whitespace_ for t in new_sentence]
        new_sentence = "".join(new_sentence)

        # Naively handle basic capitalization
        if (
            sentence[0] == sentence[0].upper()
            and new_sentence[0] != new_sentence[0].upper()
        ):
            new_sentence = new_sentence[0].upper() + new_sentence[1:]

    return new_sentence, changed


class SentenceSubjectObjectSwitch(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]
    keywords = [
        "lexical",
        "syntactic",
        "word-order",
        "rule-based",
        "tokenizer-required",
        "chunker-required",
        "meaning-alteration",
        "high-precision",
        "low-coverage",
        "low-generations",
    ]

    def __init__(self, seed=0, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)
        # Initialize the spacy model
        self.nlp = (
            spacy_nlp if spacy_nlp else initialize_models()
        )  # loads en_core_web_sm by default

    def generate(self, sentence: str):

        # Initialize Variables
        output_sentence = sentence

        new_sentence, changed = subject_object_switch(sentence, self.nlp)

        if changed:
            output_sentence = new_sentence

        return [output_sentence]


class PairSubjectObjectSwitch(SentencePairOperation):
    tasks = [TaskType.PARAPHRASE_DETECTION]
    languages = ["en"]
    keywords = [
        "lexical",
        "syntactic",
        "word-order",
        "rule-based",
        "tokenizer-required",
        "chunker-required",
        "meaning-alteration",
        "high-precision",
        "low-coverage",
        "low-generations",
    ]

    def __init__(self, seed=0, max_outputs=3, pos_label="1", neg_label="0"):
        super().__init__(seed, max_outputs=max_outputs)
        # Initialize the spacy model
        self.nlp = (
            spacy_nlp if spacy_nlp else initialize_models()
        )  # loads en_core_web_sm by default

        self.pos_label = pos_label
        self.neg_label = neg_label

    def generate(self, sentence1: str, sentence2: str, target: str):

        # Initialize Variables
        output_sentences = []
        changed_sentences = {}

        # Only process equivalent pairs
        if target == self.pos_label:

            for n, sentence in enumerate([sentence1, sentence2]):
                new_sentence, changed = subject_object_switch(
                    sentence, self.nlp
                )
                if changed:
                    changed_sentences[n] = new_sentence

        if 0 in changed_sentences.keys():
            output_sentences.append(
                (changed_sentences[0], sentence2, self.neg_label)
            )

        if 1 in changed_sentences.keys():
            output_sentences.append(
                (sentence1, changed_sentences[1], self.neg_label)
            )

        if 0 in changed_sentences.keys() and 1 in changed_sentences.keys():
            output_sentences.append(
                (changed_sentences[0], changed_sentences[1], self.pos_label)
            )

        if not output_sentences:
            output_sentences = [(sentence1, sentence2, target)]

        return output_sentences


"""
# Sample code to demonstrate usage. Can also assist in adding test cases.
# You don't need to keep this code in your transformation.
if __name__ == '__main__':
    import json
    from TestRunner import convert_to_snake_case
    tf = SentenceSubjectObjectSwitch()
    test_cases = []
    for sentence in ["Andrew has not returned the French book to the library.",
                     "John Locke and Adam Smith were born before Karl Marx and Friedrich Engels.",
                     "John loves Mary.",
                     "Ujjal Dev Dosanjh was not the 1st Premier of British Columbia from 1871 to 1872.",
                     "The fighters would not give up the fight."]:
        test_cases.append({
            "class": tf.name(),
            "inputs": {"sentence": sentence},
            "outputs": [{"sentence": o[0]} for o in tf.generate(sentence)]}
        )
    json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
    print(json.dumps(json_file))
    tf = PairSubjectObjectSwitch(max_outputs=3)
    test_cases = []
    for sentence1, sentence2, target in zip(["Andrew has not returned the French book to the library.",
                                     "John Locke and Adam Smith were born before Karl Marx and Friedrich Engels.",
                                     "John loves Mary.",
                                     "Ujjal Dev Dosanjh was not the 1st Premier of British Columbia from 1871 to 1872.",
                                     "The fighters would not give up the fight."],
                                    ["He hasn't brought back the library's books.",
                                     "Karl Marx and Friedrich Engels were born after John Locke and Adam Smith.",
                                     "John really likes Mary.",
                                     "U.D. Dosanjh wasn't the 1st Premier of British Columbia for a year from 1871.",
                                     "The warriors would stay in the battle"],
                                     ["1",
                                      "1",
                                      "1",
                                      "1",
                                      "1"
                                     ]
                                    ):
        test_cases.append({
            "class": tf.name(),
            "inputs": {"sentence1": sentence1, "sentence2": sentence2, "target": target},
            "outputs": [{"sentence1": o[0], "sentence2": o[1], "target": o[2]} for o in tf.generate(sentence1, sentence2, target)]}
        )
    json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
    print(json.dumps(json_file))
"""
