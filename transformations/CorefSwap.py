import spacy
import neuralcoref
import random
from transformations.SentenceTransformation import SentenceTransformation

class CorefSwap(SentenceTransformation):

    def __init__(self):
        random.seed(42)
        self.nlp = init_components()
        self.mention_replacers = None

    def generate(self, sentence: str):
        perturbed, mention_replacers = swap_coref(sentence,self.nlp)
        print(f"Perturbed Input from {self.name()} : {perturbed}")
        print(f"Metadata from {self.name()} : {mention_replacers}")
        self.mention_replacers = mention_replacers
        return perturbed

def init_components():
    nlp = spacy.load('en')
    coref = neuralcoref.NeuralCoref(nlp.vocab)
    nlp.add_pipe(coref,name='neuralcoref')
    return nlp

def swap_coref(sent,nlp,verbose=False,how_likely=3):
    doc = nlp(sent)


    mention_replacers = []
    if verbose: print(doc._.coref_clusters)
    for cluster_id,coref_cluster in enumerate(doc._.coref_clusters):
       
        if verbose: print(coref_cluster.mentions)
        swap_pairs = []
        for i in range(1,len(coref_cluster.mentions)):
            for j in range(i+1,len(coref_cluster.mentions)):
                if sum([random.randint(0,2) for trial in range(5)])<=how_likely:
                    swap_pairs.append((i,j))
        if verbose: print(swap_pairs)
        
        for i,j in swap_pairs:
            
            mention_i, mention_j  = coref_cluster.mentions[i], coref_cluster.mentions[j]

            mention_i_text_full = sent[doc[mention_i.start].idx:doc[mention_i.end-1].idx+len(doc[mention_i.end-1].text)] 
            mention_j_text_full = sent[doc[mention_j.start].idx:doc[mention_j.end-1].idx+len(doc[mention_j.end-1].text)] 
           
            mention_i_replacer = {"start": doc[mention_i.start].idx, "end": doc[mention_i.end-1].idx+len(doc[mention_i.end-1].text), "repn": mention_j_text_full, "start_replacer": doc[mention_j.start].idx, "end_replacer": doc[mention_j.end-1].idx+len(doc[mention_j.end-1].text) }
            mention_replacers.append(mention_i_replacer)
    
    mention_replacers.sort(key = lambda x:x["start"])

    new_string = ""
    if len(mention_replacers) > 0:
        new_string = sent[:mention_replacers[0]["start"]]
    for mention_replacer_id in range(len(mention_replacers)-1):
        new_string += mention_replacers[mention_replacer_id]["repn"]
        new_string += sent[mention_replacers[mention_replacer_id]["end"]:mention_replacers[mention_replacer_id+1]["start"]]
    if len(mention_replacers)>0:
        new_string += mention_replacers[-1]["repn"]
        new_string += sent[mention_replacers[-1]["end"]:len(sent)]

    if len(mention_replacers) == 0:
        new_string = sent

    if verbose: print(new_string)
    if verbose: print(mention_replacers)
    if verbose: print(cluster_repn_heads)
    if verbose: print(sent)
    
    return new_string, mention_replacers



if __name__ == "__main__":
    """
    random.seed(42)
    nlp = init_components()
    #sent = 'My sister has a dog. She loves him. Being a firefighter, she often uses that dog at work.' 
    sent = "Einstein's future wife, a 20-year-old Serbian named Mileva Marić, also enrolled at the polytechnic school that year. She was the only woman among the six students in the mathematics and physics section of the teaching diploma course. Over the next few years, Einstein's and Marić's friendship developed into romance, and they spent countless hours debating and reading books together on extra-curricular physics in which they were both interested. Einstein wrote in his letters to Marić that he preferred studying alongside her."

    print("Before Perturbation:",sent)
    new_string = swap_coref(sent,nlp)
    print("After Perturbation:",new_string)
    
    doc = nlp(sent)
    #print([x.text for x in list(doc.sents)])
    """
    sent = "Einstein's future wife, a 20-year-old Serbian named Mileva Marić, also enrolled at the polytechnic school that year. She was the only woman among the six students in the mathematics and physics section of the teaching diploma course. Over the next few years, Einstein's and Marić's friendship developed into romance, and they spent countless hours debating and reading books together on extra-curricular physics in which they were both interested. Einstein wrote in his letters to Marić that he preferred studying alongside her."
    coref_swap = CorefSwap()
    coref_swap.generate(sent)
