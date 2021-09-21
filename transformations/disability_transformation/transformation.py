

disability_names= {"blind":"person with a visual impairment ",
                           "deformed": " person with a physical disability ",
                           "handicapped":" person with a physical disability ",
                           "cripple":" person with a physical disability ",
                           "crippled":" person with a physical disability ",
                           "paraplegic":" person with paraplegia ",
                           "psychotic":" person with a psychotic condition ",
                           "psycho":" person with a psychotic condition ",
                           "quadriplegic":" person with quadriplegia ",
                           "schizophrenic":" person with schizophrenia ",
                           "vegetable":"  person in a vegetative state ",
                           "mentally retarded":" person with a mental  disablity ",
                           "senile ":" person with dementia ",
                           "gimp":" person with a physical disability ",
                           "spastic":"person with a physical disability ",
                           "spaz":" person with a physical disability ",
                           "lame ":" person with a physical disability ",
                           "lunatic":" person with a mental disability ",
                           "lunatics":" person with a mental disability ",
                           "looney":" person with a mental disability ",
                           "looney bin":" person with a mental disability ",
                           "manic":" person with a psychological disability ",
                           "mongoloid":" person with Down syndrome ",
                           "mutant":" person with an uncommon genetic mutation ",
                           "mutants": " people with an uncommon genetic mutation ",
                           "wheelchairbound":" wheelchair user ",
                           "dwarf":" short-statured person ",
                           "midget":" short-statured person ",
                           "deaf":" person with a hearing disability ",
                           "mute":" person with a listening disability ",
                           "dumb":" person with a mental and/or speech impairments ",
                           "demented":" person with dementia ",
                           "dotard":" old person with impaired intellect or physical disability ",
                           "dotards":"old people with impaired intellect or physical disability ",
                           "derp":" person with intellectual disabilities ",
                           "imbecile":" person with intellectual disabilities ",
                           "imbeciles":" people with intellectual disabilities ",
                           "crazy":" person with a mental impairment ",
                           "insane ":" person with a mental impairment ",
                           "wacko":" person with a mental impairment ",
                           "nuts":" person with a mental impairment ",
                           "retard":" person with an intellectual  disablity ",
                           "retards":" people with an intellectual  disablity ",
                           "retarded":" person with an intellectual  disablity "
                           }
!python -m spacy download en_core_web_sm
# POS TAGGER
import spacy
from spacy.lang.en.examples import sentences 
nlp = spacy.load("en_core_web_sm")
def postag(text):
  doc = nlp(text)
  pos_list=[]
  word_list=[]
  for token in doc:
   pos_list.append(token.pos_)
   word_list.append(token.text)
  print(pos_list,word_list)
  return word_list,pos_list
#CAPITALIZATION
def preserve_capitalization(original, transformed):
  if original[0].isupper():
    transformed = transformed.capitalize()
  else:
    return original
  return transformed

  #PUNC
def remove_punc(my_str):
  punctuations = '''!()-[]{};:\,<>./?@#$%^&*_~'''
  no_punct = ""
  for char in my_str:
   if char not in punctuations:
       no_punct = no_punct + char
  return no_punct    
def get_index(wl,n):
  indices = [i for i, x in enumerate(wl) if x == n]
  return indices

#ASSUMING FOR NAME IN TEXT

def placement(index_of_dis, wl,pl,input,disability_names,name):
  inp=input
  print(inp)
  text=input.lower()
  text=remove_punc(text)
  text = ''.join(' ' if c in '.!' else c for c in text) #for last word case
  wl,pl=postag(text)
  index_of_dis=get_index(wl,name)
  max_len=len(wl)
  #FOR EACH VALUE OF INDEX
  for i in index_of_dis: 
    print("For Occurence", i)
    print("For Words Less than Maximum Length:")
    
    if i<(max_len-1): #1<10 
      print("Words in between")
      if pl[i+1]=='NOUN': 
        #print("NOUN",i)
        #print(pl[i+1])
        s=' '.join(wl)
        text=s
        #print(1)
      elif pl[i+1]!='NOUN':
        s=' '.join(wl) #convert to a string and replace with disability name
        namew=wl[i]
        wl[i]=disability_names[namew]
        text=' '.join(wl)
        #text=replaces(s,name,input)
        #print(2)
    #last word    
    elif i>=(max_len-1):
      print("For Words At Maximum Length:") 
      namew=wl[i]
      wl[i]=disability_names[namew]
      text=' '.join(wl)
      #print(3)
    else:
      s=' '.join(wl)
    text=preserve_capitalization(input, text)
  return text    
                          
def preserve_capitalization(original, transformed):
  if original[0].isupper():
    transformed = transformed.capitalize()
  else:
    return original
  return transformed

def different_ability(input, disability_names):
  #lowercase, remove puncuations
  text=input.lower()
  text=remove_punc(text)
  text = ''.join(' ' if c in '.!' else c for c in text) #for last word case

  for name in disability_names.keys():
    if name in text:
      n=name #store name
      print(n)
      #GET POS TAGS
      wl,pl=postag(text)
      #MAX LENGTH OF LIST
      max_len=len(wl)
      #GET ALL OCCURENCES OF NAME
      indices=get_index(wl,name)
      #PLACEMENT
      text=placement(indices, wl,pl,input,disability_names,name) 

  return text


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
    for sentence in ["He is blind.",             
                     "John is deaf.",
                     "He's probably a retard.",
                     "Only a psycho will be admitted to a mental hospital.",
                     "She became a cripple after the accident."]:
        test_cases.append({
            "class": tf.name(),
            "inputs": {"sentence": sentence}, 
            "outputs": [{"sentence": o} for o in tf.generate(sentence)],
            }
        )
    json_file = {"type": convert_to_snake_case(tf.name()),
                 "test_cases": test_cases}
    print(json.dumps(json_file, indent=2))
