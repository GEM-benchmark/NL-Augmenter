from initialize import spacy_nlp
import spacy

from interfaces.SentencePairOperation import SentencePairOperation
from tasks.TaskTypes import TaskType

"""
Auxiliary Negation Removal.
    Remove auxiliary negations generating a sentence with oposite meaning.
    Can be applyed to both sentences, the first, or the second in a set of paired sentences.
"""


class AuxiliaryNegationRemoval(SentencePairOperation):
    tasks = [TaskType.PARAPHRASE_DETECTION]
    languages = ['en']

    def __init__(self, seed=0, max_outputs=3, pos_label="1", neg_label="0"):
        super().__init__(seed, max_outputs=max_outputs)
        self.nlp = spacy_nlp if spacy_nlp else spacy.load('en_core_web_sm')
        self.pos_label = pos_label
        self.neg_label = neg_label

    def generate(self, sentence1: str, sentence2: str, target: str):

        # Initialize Variables
        output_sentences = []
        changed_sentences = {}
        
        # Only process equivalent pairs
        if target == self.pos_label:

            for n, sentence in enumerate([sentence1, sentence2]):
                # Tokenize Sentence
                doc = self.nlp(sentence)

                # Initialize Variables
                new_sentence = []
                changed = False

                # Evaluate Tokens
                for token in doc:
                    # Add Token to Output Sentence
                    new_sentence.append(token)

                    # Process Negations
                    if  token.lemma_.lower() == 'not':
                        # Get not position
                        not_index = token.i

                        # Process Auxiliaries
                        if not_index > 0:

                            # Get Previous Token
                            previous_index = not_index - 1
                            previous_surface = doc[previous_index].text
                            previous_lowercase_surface = previous_surface.lower()

                            # Remove Negation
                            if previous_lowercase_surface in ['am',
                                                              'are',
                                                              'can',
                                                              'could',
                                                              'had',
                                                              'has',
                                                              'have',
                                                              'is',
                                                              'may',
                                                              'might',
                                                              'must',
                                                              'shall',
                                                              'should',
                                                              'was',
                                                              'were',
                                                              'will',
                                                              'would']:
                                new_sentence = new_sentence[:-1]
                                changed = True
                            
                                # Handle Spacing
                                if token.text == "n't":
                                    new_sentence[-1] = self.nlp(previous_surface + ' ')[0]

                            elif previous_lowercase_surface in ['do']:
                                new_sentence = new_sentence[:-2]
                                changed = True

                if changed:
                    # Rebuild Sentence
                    new_sentence = [t.text + t.whitespace_ for t in new_sentence]
                    new_sentence = ''.join(new_sentence)
                    changed_sentences[n] = new_sentence
        
        if 0 in changed_sentences.keys():
            output_sentences.append((changed_sentences[0], sentence2, self.neg_label))
        
        if 1 in changed_sentences.keys():
            output_sentences.append((sentence1, changed_sentences[1], self.neg_label))
        
        if 0 in changed_sentences.keys() and 1 in changed_sentences.keys():
            output_sentences.append((changed_sentences[0], changed_sentences[1], self.pos_label))
        
        if not output_sentences:
            output_sentences = [(sentence1, sentence2, target)]

        return output_sentences

"""
# Sample code to demonstrate usage. Can also assist in adding test cases.
# You don't need to keep this code in your transformation.
if __name__ == '__main__':
    import json
    from TestRunner import convert_to_snake_case
    tf = AuxiliaryNegationRemoval(max_outputs=3)
    test_cases = []
    for sentence1, sentence2, target in zip(["Andrew has not returned the French book to the library.",
                                     "Sentences with gapping, such as Paul likes coffee and Mary tea, do not have an overt predicate.",
                                     "Alice in Wonderland isn't a 1997 American live-action/animated dark fantasy adventure film.",
                                     "Ujjal Dev Dosanjh was not the 1st Premier of British Columbia from 1871 to 1872.",
                                     "The fighters would not give up."],
                                    ["He hasn't brought back the library's books.",
                                     "Gapping sentences, such as Paul likes coffee and Mary tea, lack an overt predicate.",
                                     "Alice in Wonderland is not an American animated, dark fantasy adventure film from 1997.",
                                     "U.D. Dosanjh wasn't the 1st Premier of British Columbia for a year from 1871.",
                                     "The warriors wouldn't leave the battlefield."],
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
