!python -m spacy download en_core_web_sm
from interfaces.SentenceOperation import SentenceOperation
from evaluation.evaluation_engine import evaluate, execute_model
from tasks.TaskTypes import TaskType
import spacy
import string
from spacy.lang.en.examples import sentences 
nlp = spacy.load("en_core_web_sm")

# A dict containing offensive words and their alternatives
disability_names =  {"blind":"person or people with a visual impairment", 
                           "deformed": "person or people with a physical disability", 
                           "handicapped":"person or people with a physical disability", 
                           "cripple":"person with a physical disability", 
                           "crippled":"person or people with a physical disability", 
                           "paraplegic":"person or people with paraplegia", 
                           "psychotic":"person or people with a psychotic condition", 
                           "psycho":"person with a psychotic condition", 
                           "psychopath":"person with a psychotic condition", 
                           "quadriplegic":"person or people with quadriplegia", 
                           "schizophrenic":"person or people with schizophrenia", 
                           "vegetable":"person in a vegetative state", 
                           "bonkers":"person or people with a mental disability", 
                           "senile":"person or people with dementia", 
                           "gimp":"person with a physical disability", 
                           "spastic":"person with a physical disability", 
                           "spaz":"person with a physical disability", 
                           "lame":"person with a physical disability", 
                           "lunatic":"person with a mental disability", 
                           "lunatics":"people with a mental disability", 
                           "looney":"person with a mental disability", 
                           "manic":"person with a psychological disability", 
                           "mutant":"person with an uncommon genetic mutation", 
                           "mutants": "people with an uncommon genetic mutation", 
                           "wheelchairbound":"wheelchair user", 
                           "subnormal":"person or people with learning difficulties or a developmental disorder", 
                           "dwarf":"short-statured person", 
                           "midget":"short-statured person", 
                           "deaf":"person or people with a hearing disability", 
                           "mute":"person or people with a listening disability", 
                           "dumb":"person or people with a mental and/or speech impairment", 
                           "demented":"person or people with dementia", 
                           "dotard":"old person with impaired intellect or physical disability", 
                           "dotards":"old people with impaired intellect or physical disability", 
                           "derp":"person with intellectual disabilities", 
                           "imbecile":"person with intellectual disabilities", 
                           "imbeciles":"people with intellectual disabilities", 
                           "crazy":"person or people with a mental impairment", 
                           "insane ":"person or people with a mental impairment", 
                           "wacko":"person with a mental impairment", 
                           "nuts":"person or people with a mental impairment", 
                           "retard":"person with an intellectual disability", 
                           "retards":"people with an intellectual disability", 
                           "retarded":"person or people with an intellectual disability", 
                           }
def postag(text):
    doc = nlp(text)
    pos_list = []
    word_list = []
    for token in doc:
        pos_list.append(token.pos_)
        word_list.append(token.text)
    print(pos_list, word_list)
    return word_list, pos_list

def cleanup(text):
    st = text
    l = len(st)
    indices = [i for i, x in enumerate(st) if x in string.punctuation]
    new_str = ""
    if len(indices) != 0:
        if indices[-1] == l-1:
            j = 0
            for i in indices:
                new_str += st[j:i-1]
                j = i
            new_str += st[j:]
            return new_str  
        elif indices[-1] < l-1:
            j = 0
            for i in indices:
                new_str += st[j:i-1]
                j = i
            notlast = indices[-1]
            new_str += st[notlast:]
            return new_str      
    elif len(indices) == 0:
        return st
    else:
        return st
      
def preserve_capitalization(original, transformed):
    if original[0].isupper():
        transformed = transformed.capitalize()
    else:
        return original
    return transformed

def get_index(wl, n):
    indices = [i for i, x in enumerate(wl) if x == n]
    return indices

def placement(index_of_dis, wl, pl, input, disability_names, name):
    text = input.lower()
    wl,pl = postag(text)
    index_of_dis = get_index(wl,name)
    max_len = len(wl)

    for i in index_of_dis: 
        print("For Occurence", i)
        print("For Words Less than Maximum Length:")
        if i < (max_len-1):
          print("Words in between")
          if pl[i+1] == 'NOUN': 
              s = ' '.join(wl)
              text = s
          elif pl[i+1]!='NOUN':
              s = ' '.join(wl) 
              namew = wl[i]
              wl[i] = disability_names[namew]
              text = ' '.join(wl)      
        elif i >= (max_len-1):
            print("For Words At Maximum Length:") 
            namew = wl[i]
            wl[i] = disability_names[namew]
            text = ' '.join(wl)
        else:
            s = ' '.join(wl)
            text = s
        text = preserve_capitalization(input, text)
    return text    
  
def different_ability(input, disability_names):
    text = input.lower()
    for name in disability_names.keys():
        if name in text:
            wl, pl = postag(text)
            max_len = len(wl)
            indices = get_index(wl, name)
            textp = placement(indices, wl, pl, input, disability_names, name) 
            text = cleanup(textp)
    return text

class DifferentAbilityTransformation(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION
    ]
    languages = ["en"]

    def __init__(self, seed=0, max_outputs=1):
        super().__init__(seed, max_outputs = max_outputs)
        self.disability_names = disability_names

    def generate(self, sentence: str):
      return [different_ability(sentence, self.disability_names)]
