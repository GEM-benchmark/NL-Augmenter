from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
import random


class CharacterToNumber(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en", "es"]
    heavy = False

    def __init__(self, seed=0, max_outputs=1, probability=1):
        super().__init__(seed, max_outputs=max_outputs)
        self.substitution_dictionary = {'O': '0', 'I': '1', 'Z':'2', 'E':'3', 'A':'4', 'S': '5', 'G': '6', 'T': '7', 'B': '8', 'P': '9'}
        self.probability = probability
        if self.verbose:
            for item in self.substitution_dictionary.items():
                print(item)
            print('Probability of substitution fixed to ', probability)

    def transform(self, string: str):
        try:
            final_string = ''
            new_string = string.upper()
            for character in new_string:
                if character in self.substitution_dictionary.keys() and random.random()< self.probability:
                    final_string = final_string + self.substitution_dictionary[character]
                else: final_string = final_string + character        
        except Exception:
            print("Returning Default due to Run Time Exception")
            final_string = string
        return final_string

    def generate(self, sentence: str):
        perturbs = [self.transform(sentence)]
        return perturbs


'''
if __name__ == '__main__':
    import json
    from TestRunner import convert_to_snake_case

    tf = CharacterToNumber()
    sentence = "Andrew finally returned the French book to Chris that I bought last week"
    test_cases = []
    src = ["Andrew finally returned the French book to Chris that I bought last week",
        "Sentences with gapping, such as Paul likes coffee and Mary tea, lack an overt predicate to indicate the relation between two or more arguments."]
    tgt = ["4NDR3W F1N4LLY R37URN3D 7H3 FR3NCH 800K 70 CHR15 7H47 1 80U6H7 L457 W33K",
        "53N73NC35 W17H 64991N6, 5UCH 45 94UL L1K35 C0FF33 4ND M4RY 734, L4CK 4N 0V3R7 9R3D1C473 70 1ND1C473 7H3 R3L4710N 837W33N 7W0 0R M0R3 4R6UM3N75.", ]
    for idx, (sentence, target) in enumerate(zip(src, tgt)):
        converted_sentence = tf.generate(sentence)
        print('sentence', sentence)
        print('converted sentence', converted_sentence)
        print('target', target)
        assert(target == converted_sentence)
'''