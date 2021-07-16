import re
import json
import os
import numpy as np
from scipy.sparse import issparse
try:
    from transformations.mix_transliteration.utils import viterbi, one_hot_encoder, wx
except:
    os.system('python3 setup.py build_ext --inplace')
    from transformations.mix_transliteration.utils import viterbi, one_hot_encoder, wx
    
import string


def ngram_context(letters, n=4):
    feats = []
    dummies = ["_"] * n
    context = dummies + letters + dummies
    for i in range(n, len(context) - n):
        unigrams = context[i - n: i] +\
            [context[i]] +\
            context[i + 1: i + (n + 1)]
        ngrams = ['|'.join(ng) for k in range(2, n + 1) for ng in zip(*[unigrams[j:] for j in range(k)])]
        feats.append(unigrams + ngrams)
    return feats

class Transliterator:
    """
    Transliterator to convert Indic scripts to english.
    """

    def __init__(self, source):
        if source in ('mar', 'nep', 'kok', 'bod'):
            source = 'hin'
        elif source == 'asm':
            source = 'ben'
        self.source = source
        self.target = 'eng'
        self.lookup = dict()
        self.decoder = viterbi
        self.tab = '\x01\x03'  # mask tabs
        self.space = '\x02\x04'  # mask spaces
        self.esc_ch = '\x00'  # escape-sequence for Roman in WX
        self.dist_dir = os.path.dirname(os.path.abspath(__file__))
        self.base_fit()
        self.letters = set(string.ascii_letters)
        self.non_alpha = re.compile(r"([^a-zA-Z%s]+)" % (self.esc_ch))
        # initialize WX back-convertor for Indic to Indic transliteration
        self._to_indic = False

    def case_trans(self, word):
        oword = word
        if not word:
            return ''
        if word[0] == self.esc_ch:
            return word[1:]
        if word[0] not in self.letters:
            return word
        if oword in self.lookup:
            return self.lookup[oword]
        word = ' '.join(word)
        word = re.sub(r' ([VYZ])', r'\1', word)
        if not self._to_indic:
            word = word.replace(' a', 'a')
        word_feats = ngram_context(word.split())
        t_word = self.predict(word_feats)
        if self._to_indic:
            t_word = self._to_utf(t_word)
        self.lookup[oword] = t_word
        return t_word

    def load_models(self):
        self.vectorizer_ = one_hot_encoder.OneHotEncoder()
        model = '{}-{}'.format(self.source, self.target)
        with open('{}/models/{}/sparse.vec'.format(self.dist_dir, model)) as jfp:
            self.vectorizer_.unique_feats = json.load(jfp)
        self.classes_ = np.load(
            '{}/models/{}/classes.npy'.format(self.dist_dir, model),
            encoding='latin1',
            allow_pickle=True)[0]
        self.coef_ = np.load(
            '{}/models/{}/coef.npy'.format(self.dist_dir, model),
            encoding='latin1',
            allow_pickle=True)[0].astype(np.float64)
        self.intercept_init_ = np.load(
            '{}/models/{}/intercept_init.npy'.format(self.dist_dir, model),
            encoding='latin1',
            allow_pickle=True).astype(np.float64)
        self.intercept_trans_ = np.load(
            '{}/models/{}/intercept_trans.npy'.format(self.dist_dir, model),
            encoding='latin1',
            allow_pickle=True).astype(np.float64)
        self.intercept_final_ = np.load(
            '{}/models/{}/intercept_final.npy'.format(self.dist_dir, model),
            encoding='latin1',
            allow_pickle=True).astype(np.float64)
        # convert numpy.bytes_/numpy.string_ to numpy.unicode_
        if not isinstance(self.classes_[0], np.unicode_):
            self.classes_ = {k: v.decode('utf-8') for k, v in self.classes_.items()}

    def base_fit(self):
        # load models
        self.load_models()
        # initialize wx-converter and character-maps
        wxp = wx.WX(order='utf2wx', lang=self.source)
        self.wx_process = wxp.utf2wx
        self.mask_roman = re.compile(r'([a-zA-Z]+)')

    def predict(self, word):
        X = self.vectorizer_.transform(word)
        if issparse(X):
            scores = X.dot(self.coef_.T).toarray()
        else:
            scores = self.coef_.dot(X.T).T
        y = self.decoder.decode(
            scores,
            self.intercept_trans_,
            self.intercept_init_,
            self.intercept_final_
        )
        y = [self.classes_[pid] for pid in y]
        y = ''.join(y).replace('_', '')
        return y

    def convert_to_wx(self, text):
        if self.source == 'eng':
            return text.lower()
        if self.source == 'ben':
            # Assamese `ra` to Bengali `ra`
            text = text.replace('\u09f0', '\u09b0')
            # Assamese `va` to Bengali `va`
            text = text.replace('\u09f1', '\u09ac')
        text = self.mask_roman.sub(r'%s\1' % (self.esc_ch), text)
        text = self.wx_process(text)
        return text

    def transliterate(self, text, k_best=None):
        trans_list = []
        text = self.convert_to_wx(text)
        text = text.replace('\t', self.tab)
        text = text.replace(' ', self.space)
        lines = text.split("\n")
        for line in lines:
            if not line.strip():
                trans_list.append(line)
                continue
            trans_line = str()
            line = self.non_alpha.split(line)
            for word in line:
                trans_line += self.case_trans(word)
            trans_list.append(trans_line)
        trans_line = '\n'.join(trans_list)
        trans_line = trans_line.replace(self.space, ' ')
        trans_line = trans_line.replace(self.tab, '\t')
        return trans_line