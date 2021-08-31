#!/usr/bin/env python
# coding: utf-8

# In[ ]:


"""
ref: https://medium.com/coinmonks/remaking-of-shortened-sms-tweet-post-slangs-and-word-contraction-into-sentences-nlp-7bd1bbc6fcff
"""

from bs4 import BeautifulSoup
import urllib3
import json

http = urllib3.PoolManager()
phrase_abbr_dict = {}
word_abbr_dict = {}
def getAbbr(alpha):
    global phrase_abbr_dict
    global word_abbr_dict
    r = http.request('GET','https://www.noslang.com/dictionary/'+alpha)
    soup = BeautifulSoup(r.data,'html.parser')
    
    for i in soup.findAll('div',{'class':'dictionary-word'}): 

        full = i.find('abbr')['title']
        abbr = i.find('span').text[:-2]
        #abbr_dict[i.find('span').text[:-2]] = abbr
        
        if " " not in full:
            word_abbr_dict[full] = abbr
        else:
            phrase_abbr_dict[full] = abbr
        
linkDict = []

#Generating a-z
for one in range(97,123):
    linkDict.append(chr(one))

    #Creating Links for https://www.noslang.com/dictionary/a...https://www.noslang.com/dictionary/b....etc
for i in linkDict:
    getAbbr(i)

#abbr_dict = {v: k for k, v in abbr_dict.items()}
    
# finally writing into a json file
with open('phrase_abbrev_dict.json','w') as file:
    jsonDict = json.dump(phrase_abbr_dict,file)
with open('word_abbrev_dict.json', 'w') as file:
    jsonDict = json.dump(word_abbr_dict, file)