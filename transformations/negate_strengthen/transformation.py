import random
from initialize import spacy_nlp
from interfaces.SentenceOperation import SentenceAndTargetOperation
from tasks.TaskTypes import TaskType

import re
import spacy
from spacy.tokenizer import Tokenizer
import pandas as pd
import nltk
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.metrics import edit_distance
from nltk import pos_tag
from pattern.en import conjugate as conjugate_en
from typing import Union

# defaults
_RE_COMBINE_WHITESPACE = re.compile(r"\s+")
MODAL_TYPE_LEMMA = ['be', 'to', 'have', 'get', 'do']
MODAL_STRENGTHEN_DICT = {
    'could': 'would',
    'should': 'would',
    'would': 'would',
    'can': 'will',
    'may': 'will',
    'might': 'will',
    'will': 'will'
}

# intialize
try:
    conjugate_en(verb='testing',tense='present',number='singular')
except:
    pass


class NegateStrengthen(SentenceAndTargetOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.SENTIMENT_ANALYSIS]
    languages = ["en"]
    tgt_languages = ["en"]

    def __init__(self, max_outputs=1, seed=0, verbose=False):
        super().__init__(seed)

        # downloads
        nltk.download('wordnet')
        nltk.download('averaged_perceptron_tagger')

        # initialise
        self.verbose = verbose
        self.nlp = spacy.load("en_core_web_sm")
        self.nlp.tokenizer = Tokenizer(
            self.nlp.vocab, 
            prefix_search=re.compile('''^\\$[a-zA-Z0-9]''').search
            )
        self.wnl = WordNetLemmatizer()
        self.max_outputs = max_outputs
        self.num_tries = 2 # fixed number of max recursion tries
        self.seed = seed
        random.seed(self.seed)


    def text_to_spacy_table_info(self, _text):

        doc = self.nlp(_text)

        table = []
        letters2word = {}
        
        # future to do: keep only relevant items
        for idx, token in enumerate(doc):
            letters2word[token.idx] = idx
            table.append([token.text, token.lemma_, token.pos_, token.tag_, 
                        token.dep_, token.head.text, token.head.idx, token.head.pos_])

        table = pd.DataFrame(table)
        table.columns = ['text', 'lemma', 'pos', 'pos_tag', 'dep', 'head_text', 'head_id', 'head_pos']
        # convert idx from letter idx to word idx level
        table['head_id'] = [letters2word[i] for i in table['head_id']]
        if self.verbose:
            print(table)

        return table


    def negation_rules(self, tgx, text, pos, method=[], curr_try=0):

        curr_try += 1
        edit_id = tgx

        if self.verbose:
            print('before {}, actual {}, after {}'.format(pos[tgx-2], pos[tgx-1], pos[tgx]))
        if curr_try > self.num_tries:
            if self.verbose:
                print('Max {} tries hit...'.format(self.num_tries))
            method.append(None)
            edit_id = None
            text = None
        elif pos[tgx-1][0:2] =='VB':
            # if actual word is a modal type
            if self.wnl.lemmatize(text[tgx-1],'v') in MODAL_TYPE_LEMMA \
            or (pos[tgx-1] in ['MD']):
                # if word is last word
                if tgx>=len(text):
                    method.append('VB_1_1')
                    text[tgx-1] =  "<edit>not</edit> " + text[tgx-1]
                # if word after is determiner of sorts
                elif pos[tgx][0:2] in ['CD', 'DT']:
                    method.append('VB_1_2')
                    text[tgx] = "<edit>no</edit>"
                # if word after is noun or description of a noun
                elif pos[tgx][0:2] in ['JJ', 'NN', 'PR', 'WP', 'WD', 'DT']:
                    method.append('VB_1_3')
                    text[tgx-1] = text[tgx-1] + " <edit>not</edit>"
                # if word after is VB
                elif pos[tgx][0:2] =='VB':
                    method.append('VB_1_4')
                    text[tgx-1] = text[tgx-1] + " <edit>no</edit>"
            # if word is the first word
            elif tgx-1==0:
                method.append('VB_2_1')
                text[tgx-1] = "<edit>Not</edit> " + text[tgx-1].lower()
            # if word before target is noun type
            elif pos[tgx-2][0:2] in ['NN', 'PR', 'WP', 'WD', 'DT']:
                method.append('VB_3_1')
                text[tgx-1] = "<edit>did not</edit> " + self.wnl.lemmatize(text[tgx-1],'v')
            # if word is last word
            elif tgx>=len(text):
                method.append('VB_4_1')
                text[tgx-1] =  "<edit>not</edit> " + text[tgx-1]
            # if word before target is AUX | if word after target is IN/TO
            elif self.wnl.lemmatize(text[tgx-2],'v') in MODAL_TYPE_LEMMA \
            or (pos[tgx-2] in ['MD'])\
            or (pos[tgx] in ['IN', 'TO']):
                method.append('VB_5_1')
                text[tgx-1] = "<edit>not</edit> " + text[tgx-1]
            else:
                if self.verbose:
                    print('Unable to find VB_X_X rule...')
                method.append(None)
                edit_id = None
                text = None
        # if target is noun (e.g. as a result of)
        elif pos[tgx-1][0:2] =='NN':
            method.append('NN_1_1')
            loc_id = tgx-1
            doc = self.nlp(' '.join(text))
            dep_dict = {}
            for ix, token in enumerate(doc):
                dep_dict[token.idx] = [ix, token.text, token.head.text, token.head.idx]
                if ix==loc_id:
                    spacy_loc_id = token.idx
            assert(dep_dict[spacy_loc_id][1]==text[tgx-1])
            edit_id = 1 + dep_dict[dep_dict[spacy_loc_id][3]][0]
            text, method, edit_id = self.negation_rules(
                edit_id, text, pos, method=method, curr_try=curr_try)
        # if actual word is an adjective
        elif pos[tgx-1][0:2] =='JJ':
            # if adjective is last word
            if tgx>=len(text):
                method.append('JJ_1_1')
                text[tgx-1] = "<edit>not</edit> " + text[tgx-1]
            # if word after is positive conjunctions
            elif text[tgx] in ['and', 'or']:
                method.append('JJ_1_2')
                text[tgx-1] = "<edit>not</edit> " + text[tgx-1]
                text[tgx] = "<edit>nor</edit>"
            else:
                method.append('JJ_1_3')
                text[tgx-1] = "<edit>not</edit> " + text[tgx-1]
        # if actual word is an subornating conjunction (E.g. because, before, of)
        elif pos[tgx-1][0:2] =='IN':
            method.append('IN_1_1')
            text[tgx-1] = "<edit>not</edit> " + text[tgx-1]
        else:
            if self.verbose:
                print('Unable to find rule...')
            method.append(None)
            edit_id = None
            text = None
        
        return text, method, edit_id


    def get_synonyms_antonyms(self, word):

        # include self dictionary
        cause_terms = ['cause', 'induce', 'trigger', 'affect', 'spark', 'incite', 'set']
        opp_cause_terms = ['deter', 'defuse', 'impede', 'block']

        # use wordnet dictionary
        synonyms = [] 
        antonyms = [] 

        for syn in wordnet.synsets(word): 
            for l in syn.lemmas():
                synonyms.append(l.name()) 
                if l.antonyms(): 
                    antonyms.append(l.antonyms()[0].name()) 
        
        syn, ant = list(set(synonyms)), list(set(antonyms))

        if (self.wnl.lemmatize(word,'v').lower() in cause_terms):
            if (len(ant)==0):
                ant = opp_cause_terms
            if (len(syn)==0):
                syn = cause_terms

        return syn, ant


    def fuzzy_match(self, s1, s2, min_prop=0.7):
        if (s2 is None) or (s1 is None):
            return False
        elif s1 in s2:
            return True
        else:
            max_dist = round(max(len(s1),len(s2))*(1-min_prop),0)
            return edit_distance(s1,s2) <= max_dist


    def improve_negation_flow(self, text, edit_id, edit_method):
        """
        current problems: 
        might be using too many packages (can consider streamlining spacy, nltk, pattern)
        """
        tense = None
        word = text[edit_id-1]
        # check grammar of word
        if conjugate_en(verb=word,tense='past',number='singular')==word:
            tense = 'past'
        elif conjugate_en(verb=word,tense='present',number='singular')==word:
            tense = 'present'
        elif conjugate_en(verb=word,tense='participle',number='singular')==word:
            tense = 'participle'

        syn, ant = self.get_synonyms_antonyms(word)
        if len(ant)>0:
            edit_word = random.choice(ant)
            if tense is not None:
                edit_word = conjugate_en(verb=edit_word,tense=tense,number='singular')
            else:
                if self.verbose:
                    print('Caution: Unsure of tense of "{}" to "{}"...'.format(word, edit_word))
            text[edit_id-1] = "" + edit_word + ""
        else:
            if self.verbose:
                print('Unable to find an antonym...')
            text = None
            edit_word = None
        return text, edit_word


    def select_edit(self, edits_dict):

        edit_id = edits_dict['edit_id']

        if edits_dict['alt_text'] is not None:
            alt_word = edits_dict['alt_text'][edit_id-1]
            alt_word = self.wnl.lemmatize(re.sub('(\\<(\\/)*edit\\>)', '', alt_word))
        else:
            alt_word = None
        not_word = edits_dict['edit_text'][edit_id-1]
        orig_word = self.wnl.lemmatize(re.sub('(\\<(\\/)*edit\\>)', '', not_word))
        not_word = re.sub('(\\<(\\/)*edit\\>)', '', not_word)

        if self.verbose:
            print('orig_word: {} | not_word: {} | alt_word: {}'.format(orig_word, not_word, alt_word))

        if self.fuzzy_match(orig_word, alt_word, min_prop=0.7):
            return edits_dict['alt_text']
        else:
            return edits_dict['edit_text']


    def format_text(self, _text):
        return re.sub(' +', ' ', re.sub('(\\<(\\/)*edit\\>)', '', ' '.join(_text)))


    def text_to_negated_edits(self, _text, get_roots=None):
        # clean multiple whitespaces
        _text = _RE_COMBINE_WHITESPACE.sub(" ", _text).strip()
        text = _text.split(' ')
        pos = [p[1] for p in pos_tag(text)]

        # get roots based on dep info from spacy
        table = self.text_to_spacy_table_info(_text)
        if get_roots is None:
            get_roots = table[([True if t[0:2] =='VB' else False for t in table['pos_tag']]) & (table['dep'] == 'ROOT')].index
        if self.verbose:
            print(">>>>> get_roots: ", get_roots)

        t_dict = {}
        for jx, root in enumerate(get_roots):
            # check if root has acomp, adjust root
            if table.loc[root,'lemma'] in MODAL_TYPE_LEMMA or (table.loc[root,'pos_tag'] in ['MD']):
                if len(table[(table['dep'].isin(['acomp','attr'])) & (table['head_id']==root)])>0:
                    root = table[(table['dep'].isin(['acomp','attr'])) & (table['head_id']==root)].index[0]
                    if self.verbose:
                        print('new root: {}'.format(table.loc[root, 'text']))
            
            # using root loc, negate
            edit_text, method, edit_id = self.negation_rules(root+1, text, pos, method=[])

            if self.verbose:
                print(">>>>> edit_text: ", edit_text)

            # improve text flow
            if None not in method and len(method)>0:
                alt_text, alt_word = self.improve_negation_flow(_text.split(' '), edit_id, method)
                # if method is nor format
                if alt_text is not None:
                    if method[-1]=='JJ_1_2':
                        alt_text, alt_word_2 = self.improve_negation_flow(alt_text.copy(), edit_id+2, method)
                        alt_word = [alt_word, alt_word_2]
            else:
                alt_word = None
                alt_text = None

            # keep only successful edits
            if None not in method:
                t_dict[jx] = {
                    'edit_text': edit_text,
                    'edit_id': edit_id,
                    'edit_method': method,
                    'alt_word': alt_word,
                    'alt_text': alt_text
                }

        return t_dict


    def text_to_stronger_edits(self, _text):
        # clean multiple whitespaces
        _text = _RE_COMBINE_WHITESPACE.sub(" ", _text).strip()
        text = _text.split(' ')

        # get weaker words for converting
        table = self.text_to_spacy_table_info(_text)
        get_roots = table[table['lemma'].isin(MODAL_STRENGTHEN_DICT.keys())].index

        t_dict = {}
        for jx, root in enumerate(get_roots):
            
            if table.loc[root+1,'lemma']=='be':
                text[root] = "<edit>was</edit>"
                text[root+1] = ""
                method = ['MOD_2_1']
            elif  table.loc[root+1,'lemma']=='have':
                if table.loc[root+2,'lemma']=='be':
                    text[root] = "<edit>was</edit>"
                    text[root+1] = ""
                    text[root+2] = ""
                    method = ['MOD_3_2']
                else:
                    text[root] = "<edit>had</edit>"
                    text[root+1] = ""
                    method = ['MOD_3_1'] 
            elif (table.loc[root,'pos_tag']=='MD') and (table.loc[root+1,'pos_tag']=='RB'):
                text[root] = '<edit>'+ MODAL_STRENGTHEN_DICT[text[root]] + '</edit>'
                text[root+1] = ""
                method = ['MOD_4_1']
            else:
                text[root] = '<edit>'+ MODAL_STRENGTHEN_DICT[text[root]] + '</edit>'
                method = ['MOD_1_1']
            
            edit_text = text
            edit_id = root

            # keep only successful edits
            if None not in method:
                t_dict[jx] = {
                    'edit_text': edit_text,
                    'edit_id': edit_id,
                    'edit_method': method,
                    'alt_word': None,
                    'alt_text': None
                }

        return t_dict


    def generate(self, sentence: Union[dict, str], target: str):
        """
        The current available transformation of targets are :
            * "Direct Causal" -> "No Relationship"
            * "Conditional Causal" -> "Direct Causal"
            * "Direct Relation" -> "No Relationship"
        """

        if isinstance(sentence, dict):
            # You can indicate specific word location with var "get_roots" as a list of index
            # especially if you already know the root word you wish to negate/strengthen upon. 
            # E.g. AltLex dataset has "signal_id" info
            get_roots = [sentence['signal_id']]
            sentence = sentence['sentence']
        else:
            # If unspecified, we revert to Root Verbs based on spacy dependency parser.
            get_roots = None

        if self.verbose:
            print('>>>>>>> sentence: ',sentence)
            print('>>>>>>> target: ',target)

        perturbed_sentences = ["NA"]
        perturbed_target = "NA"
        
        if target in ['Direct Causal', 'Direct Relation']:
            # Negation: Direct Causal -> No Relationship
            t_dict = self.text_to_negated_edits(sentence, get_roots=get_roots)
            if self.verbose:
                print(">>>>>> t_dict: ", t_dict)

            if len(t_dict)>0:
                # Found available negation
                perturbed_sentences = []
                for k, v in t_dict.items():
                    # Select edit or alt edit
                    perturbed_sentence = self.format_text(self.select_edit(v))
                    # Store output
                    perturbed_sentences.append(perturbed_sentence)
                perturbed_target = 'No Relationship'

        elif target == 'Conditional Causal':
            # Strengthen: Conditional Causal -> Direct Causal
            t_dict = self.text_to_stronger_edits(sentence)
            if self.verbose:
                print(">>>>>> t_dict: ", t_dict)

            if len(t_dict)>0:
                # Found available strengthening
                perturbed_sentences = []
                for k, v in t_dict.items():
                    # Format sentence
                    perturbed_sentence = self.format_text(v['edit_text'])
                    # Store output
                    perturbed_sentences.append(perturbed_sentence)
                perturbed_target = 'Direct Causal'
        else:
            # Any future conversion implementations
            pass
        
        perturbed_items  = [(perturbed_sentences[i], perturbed_target) for i in range(self.max_outputs)]

        if self.verbose:
            print(">>>>>> perturbed_items: ", perturbed_items)

        return perturbed_items