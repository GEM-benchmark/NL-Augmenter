import itertools
import random

from typing import List

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

"""
5 way Character Perturbation [ Swap, Delete, Insert, Duplicate, Substitute]
Pass to Operations a list of booleans corresponding to which operations you want to be a part of final perturbation :
1. Swap
2. Delete
3. Insert
4. Duplicate
5. Substitute

Eg : Only Substitution : operation = [0,0,0,0,1]
     Deletion + Substitution : operation = [0,1,0,0,1]

"""



class VariableCharPerturbation(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION, TaskType.TEXT_TAGGING]

    languages = ["en"]

    def __init__(self, seed: int = 0, max_outputs: int = 1, probability: float = 0.2,operations: list = [1,1,1,1,1]) -> None:
        super().__init__(seed=seed, max_outputs=max_outputs)
        self.probability = probability
        self.operations = operations
        assert(sum(self.operations)!=0)


    def swap(self,word,i,j):
        """
          Swap ith and jth position in word 
        """
        word_ = ""
        for x in range(len(word)):
            if x == i:
                word_+=word[j]
            elif x == j:
                word_+=word[i]
            else:  
                word_+=word[x]
        return word_

    def insert(self,word,i,x):
        """
          Insert x at ith position in word 
        """
        return word[:i]+x+word[i:]

    def delete(self,word,i):
        """
          Delete ith position in word 
        """
        return word[:i]+word[i+1:]

    def substitute(self,word,i,x):
        """
          Substitute x at ith position in word
        """
        string_list = list(word)
        string_list[i] = x
        return "".join(string_list)

    def duplicate(self,word,i):
        """
          Duplicate ith position in word
        """
        d = word[i]
        return word[:i]+d+word[i:]

    def generate(self, sentence:str) -> List[str]:
        random.seed(self.seed)
        perturbed_texts = []
        # Perturb the input sentence max_output times
        for _ in itertools.repeat(None, self.max_outputs):
            new = []
            for i in sentence.split():
              if self.probability>random.uniform(0, 1) and len(i)>3 and i.isalpha(): # enter perturbation loop
                ch = []
                for j in range(len(self.operations)):
                    if self.operations[j]:
                        ch.append(j+1)

                choice = random.choice(ch)
                if choice == 1: # swap
                  swap_point = random.randint(0,len(i)-1)
                  if swap_point == 0:
                    swap_target = 1
                  elif swap_point == len(i)-1:
                    swap_target = swap_point - 1
                  else:
                    seqs = [swap_point - 1,swap_point+1]
                    swap_target = random.choice(seqs)
                  swapped_word = self.swap(i,swap_point,swap_target)

                  new.append(swapped_word)

                elif choice == 2: # delete
                  delpoint = random.randint(0,len(i)-1)
                  del_word = self.delete(i,delpoint)
                  new.append(del_word)

                elif choice == 3: #insert
                  ipoint = random.randint(0,len(i)-1)
                  alphabets = "abcdefghijklmnopqrstuvwxyz"
                  alphachoice = random.randint(0,len(alphabets)-1)
                  i_word = self.insert(i,ipoint,alphabets[alphachoice])
                  new.append(i_word)
                
                elif choice == 4: # duplicate
                  dpoint = random.randint(0,len(i)-1)
                  d_word = self.duplicate(i,dpoint)
                  new.append(d_word)

                else: # substitute
                  spoint = random.randint(0,len(i)-1)
                  alphabets = "abcdefghijklmnopqrstuvwxyz"
                  alphachoice = random.randint(0,len(alphabets)-1)
                  s_word = self.substitute(i,spoint,alphabets[alphachoice])
                  new.append(s_word)

                

              else:
                new.append(i)
              
            perturbed_texts.append(" ".join(new))

        return perturbed_texts

# if __name__ == '__main__':
#     import json
#     from TestRunner import convert_to_snake_case
#     tf = CharPerturbation(max_outputs=3)
#     sentence = "Andrew finally returned the French book to Chris that I bought last week"
#     test_cases = []
#     for sentence in ["Andrew finally returned the French book to Chris that I bought last week",
#                      "Sentences with gapping, such as Paul likes coffee and Mary tea, lack an overt predicate to indicate the relation between two or more arguments.",
#                      "Alice in Wonderland is a 2010 American live-action/animated dark fantasy adventure film",
#                      "Ujjal Dev Dosanjh served as 33rd Premier of British Columbia from 2000 to 2001",
#                      "Neuroplasticity is a continuous processing allowing short-term, medium-term, and long-term remodeling of the neuronosynaptic organization."]:
#         test_cases.append({
#             "class": tf.name(),
#             "inputs": {"sentence": sentence}, "outputs": [{"sentence": o} for o in tf.generate(sentence)]}
#         )
#     json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
#     print(json.dumps(json_file))