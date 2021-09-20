
import itertools
import random
import string

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

"""
Base Class for implementing the different input transformations a generation should be robust against.
"""
disability_names= {"blind ":" visually impaired ",
                           "deformed ": " person with a physical disability ",
                           "handicapped ":" person with a physical disability ",
                           "cripple ":" person with a physical disability ",
                           "crippled ":" person with a physical disability ",
                           "paraplegic ":" person with paraplegia ",
                           "psychotic ":" person with a psychotic condition ",
                           "psycho ":" person with a psychotic condition ",
                           "quadriplegic ":" person with quadriplegia ",
                           "schizophrenic ":" person with schizophrenia ",
                           "vegetable ":"  person in a vegetative state ",
                           "mentally retarded ":" person with a mental  disablity ",
                           "senile ":" person with dementia ",
                           "gimp ":" person with a physical disability ",
                           "spastic ":"person with a physical disability ",
                           "spaz ":" person with a physically disability ",
                           "lame ":" person with a physically disability ",
                           "lunatic ":" person with a mental disability ",
                           "lunatics ":" person with a mental disability ",
                           "looney":" person with a mental disability ",
                           "looney bin ":" person with a mental disability ",
                           "manic ":" person with a psychological disability ",
                           "mongoloid ":" person with Down syndrome ",
                           "mutant ":" person with an uncommon genetic mutation ",
                           "mutants ": " people with an uncommon genetic mutation ",
                           "wheelchair bound ":" wheelchair user ",
                           "dwarf ":" short-statured person ",
                           "midget ":" short-statured person ",
                           "deaf ":" person with a hearing disability ",
                           "mute ":" person with a listening disability ",
                           "dumb ":" person with a mental and/or speech impairments ",
                           "demented ":" person with dementia ",
                           "dotard ":" old person with impaired intellect or physical disability ",
                           "dotards ":"old people with impaired intellect or physical disability ",
                           "derp ":" person with intellectual disabilities ",
                           "imbecile ":" person with intellectual disabilities ",
                           "imbeciles ":" people with intellectual disabilities ",
                           "crazy ":" person with a mental impairment ",
                           "insane ":" person with a mental impairment ",
                           "wacko ":" person with a mental impairment ",
                           "nuts ":" person with a mental impairment ",
                           "retard ":" person with an intellectual  disability ",
                           "retards ":" people with an intellectual  disability ",
                           "retarded ":" person with an intellectual  disablity "
                           }
def preserve_capitalization(original, transformed):
  if original[0].isupper():
    transformed = transformed.capitalize()
  else:
    return original
  return transformed

def last_character(orig,trans):
  global end_var,final
  end_var=orig[-1]
  if trans[:-1]==" ":
    final = trans[:-1]+end_var
  elif trans[:-1]!=" ":
    final = trans+end_var
  else:
    return final
  return final


def different_ability(input, list):
    text=input.lower()
    text = ''.join(' ' if c in '.!' else c for c in text) #for last word case

    for name in disability_names.keys():
        if name in text: #if name of disability is present
            text = text.replace(name, disability_names[name])
        text=preserve_capitalization(input,text)
    text=last_character(input,text)    
    return text 


"""

"""


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

if __name__ == '__main__':
    import json
    from TestRunner import convert_to_snake_case

    tf = DifferentAbilityTransformation()
    #sentence = "Andrew finally returned the French book to Chris that I bought last week"
    test_cases = []
    #WARNING: Some sentences may be offensive 
    for sentence in ["He became a cripple.",             
                     "John is deaf.",
                     "He's probably a retard.",
                     "A psycho was admitted to a mental hospital."]:
        test_cases.append({
            "class": tf.name(),
            "inputs": {"sentence": sentence}, 
            "outputs": [{"sentence": o} for o in tf.generate(sentence)],
            }
        )
    json_file = {"type": convert_to_snake_case(tf.name()),
                 "test_cases": test_cases}
    print(json.dumps(json_file, indent=2))
