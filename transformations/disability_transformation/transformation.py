import itertools
import random

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

"""
Base Class for implementing the different input transformations a generation should be robust against.
"""


def different_ability(input, disability_names):
    text=input.lower()
    for name in disability_names.keys():
        if name in text:
            text = text.replace(name, disability_names[name])
    return text 


"""
Butter Finger implementation borrowed from https://github.com/alexyorke/butter-fingers.
"""
disability_names= {"blind": "visually impaired",
                           "deformed": "person with physical disability",
                           "handicapped":"person with physical disability",
                           "cripple":"person with physical disability",
                           "gimp":"person with physical disability",
                           "spastic":"person with physical disability",
                           "spaz":"person with physical disability",
                           "wheelchairbound":"wheelchair user",
                           "dwarf":"short-statured person",
                           "midget":"short-statured person",
                           "deaf":"hard-of-hearing",
                           "dumb":"person with hearing and/or speech impairments",
                           "derp":"person with intellectual disabilities",
                           "imbecile":"person with intellectual disabilities",
                           "crazy":"mentally impaired",
                           "insane":"mentally impaired",
                           "wacko":"mentally impaired",
                           "nuts":"mentally impaired",
                           "retard":"person with a learning disablity"
                           }

class DifferentAbilityTransformation(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION
    ]
    languages = ["en"]
    


    def __init__(self, seed=0, max_outputs=1):
        super().__init__(seed, max_outputs=max_outputs)
        
       
        self.disability_names = disability_names


    def generate(self, sentence: str):
        return [different_ability(sentence, self.disability_names)]


# Sample code to demonstrate usage. Can also assist in adding test cases.
# You don't need to keep this code in your transformation.
if __name__ == '__main__':
    import json
    from TestRunner import convert_to_snake_case

    tf = DifferentAbilityTransformation()
    test_cases = []
    for sentence in ["He is blind.",             
                     "John is deaf.",
                     "That kid is so slow he's probably a retard.",
                     "Alice is a wacko."]:
        test_cases.append({
            "class": tf.name(),
            "inputs": {"sentence": sentence}, "outputs": [{"sentence": o} for o in tf.generate(sentence)]}
        )
    json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
    print(json.dumps(json_file, indent=2))

