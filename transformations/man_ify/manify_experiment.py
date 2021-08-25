
import io
import re
import string
import tqdm

import numpy as np

import tensorflow as tf
from tensorflow.keras import layers

import gensim 
from gensim import downloader 

'''
vocab_size  = 10000
embedding_dim = 300 
W = tf.Variable(tf.constant(0.0, shape=[vocab_size, embedding_dim]),
                trainable=False, name="W")

embedding_placeholder = tf.placeholder(tf.float32, [vocab_size, embedding_dim])
embedding_init = W.assign(embedding_placeholder)

# ...
sess = tf.Session()

sess.run(embedding_init, feed_dict={embedding_placeholder: embedding})
'''
# taken from https://radimrehurek.com/gensim/auto_examples/tutorials/run_word2vec.html#sphx-glr-auto-examples-tutorials-run-word2vec-py
import gensim.downloader as api
wv = api.load('word2vec-google-news-300')
wv_man = wv['man']
wv_woman = wv['woman']
wv_king= wv['king']
wv_queen = wv['queen']

wv.similar_by_vector( wv_king + wv_woman,  topn = 4)

### Now need to figure out SVO
## https://stackoverflow.com/questions/39763091/how-to-extract-subjects-in-a-sentence-and-their-respective-dependent-phrases

