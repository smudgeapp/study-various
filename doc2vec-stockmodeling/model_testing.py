import gensim
import os
import string
from preprocess import Preprocess
from vec_ops import VectorOperations
from gensim.models import Word2Vec
from gensim.models.doc2vec import Doc2Vec
from gensim.test.test_doc2vec import ConcatenatedDoc2Vec
import logging
import json
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import datetime
import time
import numpy as np

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


##method to transfer corpus to gensim tagged document
def d2vTagData(data):
    itr = 0
    for name, item, date, stock_val in data:
        tokens = gensim.utils.simple_preprocess(item)
        tag = [itr, name, date, stock_val]
        itr += 1
        yield gensim.models.doc2vec.TaggedDocument(tokens, tag)

dirpath = "E:/Projects/word2vec/w2vgit/rssj"
dirpath2 = "C:/Users/HP/Downloads/w2v-wip/rssj"

##price data must be stored in columns, with the tickers matching the names
## in the corpus
##
price_data = os.path.join("price_data_sort1.csv")
price_cols = ['Date', 'ATRL_Avg', 'OGDC_Avg', 'NRL_Avg', 'HUBC_Avg',
                  'KAPCO_Avg', 'PSO_Avg', 'PPL_Avg']


stringops = Preprocess(pricedata=price_data, datacols=price_cols)
vec_ops = VectorOperations()

jsonfile = os.path.join(dirpath2, "final_cor.json")

data = stringops.getJSONData(jsonfile, text_index=1, stock_data=True)


targetname = 'pso'
name_list = ['pso', 'ogdc', 'ppl', 'atrl', 'nrl', 'hubc', 'kapco']

regex_list = [r'\b(pakistanstateoil)', r'\b(oil&gasdevelopmentcompany)',
              r'\b(oilandgasdevelopmentcompany)', r'\b(ogdcl)', 
              r'\b(pakistanpetroleum)',
              r'\b(attockrefinery)', r'\b(nationalrefinery)',
              r'\b(hubpowercompany)', r'\b(hubco)', r'\b(kotaddupower)']
replace_list = [r'pso', r'ogdc', r'ogdc', r'ogdc', r'ppl', r'atrl', r'nrl',
                r'hubc', r'hubc', r'kapco']

regex_dict = []

for i in range(len(regex_list)):
    item = {
        'regex': regex_list[i],
        'replace': replace_list[i]
        }
    regex_dict.append(item)
    

d2vdata = stringops.preprocessDocs(data, target_names=regex_dict,
                                   remove_nnp=True)
d2vcorpus = list(d2vTagData(d2vdata))


d2v_dbow = Doc2Vec.load('d2vmodel.model')
d2v_dm = Doc2Vec.load('d2vmodel_dm.model')
d2v_com = Doc2Vec.load('d2v_test.model')

#custom concatenation of dbow & dm
#this concatenates the paragraph vectors and the word vectors
vec_ops.concatenate_d2v(d2v_com, d2v_dbow, d2v_dm)

#defining text files for storing testing data and results
plain_sents = 'plain_sents.txt'
polar_sents = 'polar_sents.txt'
coed_sents = 'coed_sents.txt'

plain_res = 'plain_res.txt'
polar_res = 'polar_res.txt'
coed_res = 'coed_res.txt'

plain_res_vecs = 'plain_res_vecs.txt'
polar_res_vecs = 'polar_res_vecs.txt'
coed_res_vecs = 'coed_res_vecs.txt'

#define pos taggin filter - this is a positive filter
#it will keep the listed ones and remove the rest
#this input is as a nested list, with two items
#the first will filter words from the sim of target word
#second will filter words from the sim words of the sim word of the target word.

tagfilters = [['N'], ['V', 'J', 'R']]
polscore = 0.05               

sents = vec_ops.plain_sents(d2v_com, 'pso', tag_filters=tagfilters,
                           write_to=plain_sents, topn=25)



polar_sents = vec_ops.polar_sents(d2v_com, 'pso', tag_filters=tagfilters,
                                 write_polar_sents=polar_sents, pol_score=polscore,
                                 topn=25)

coed_sents = vec_ops.coed_polar_sents(d2v_com, 'pso', tag_filters=tagfilters,
                                       write_coed_sents=coed_sents,
                                       pol_score=polscore, vec_len=50, topn=25)

vec_ops.run_test(d2v_com, sents, d2vcorpus, polar_sents=0, epochs=50000,
                 write_to=plain_res)

vec_ops.run_test(d2v_com, polar_sents, d2vcorpus, epochs=50000,
                 write_to=polar_res)

vec_ops.run_test(d2v_com, coed_sents, d2vcorpus, epochs=50000,
                 write_to=coed_res)

##vec_shape = 600
##
##sents_vecs = vec_ops.plain_vecs(d2v_com, 'pso', tag_filters=tagfilters,
##                                topn=25, shape_r=vec_shape)
##
##polar_vecs = vec_ops.polar_vecs(d2v_com, 'pso', tag_filters=tagfilters,
##                               topn=25, shape_r=vec_shape)
##
##coed_vecs = vec_ops.coed_polar_vecs(d2v_com, 'pso', tag_filters=tagfilters,
##                                    topn=25, shape_r=vec_shape)
##
##vec_ops.run_test(d2v_com, sents_vecs, d2vcorpus, vecs=1, polar_sents=0,
##                 epochs=50000, write_to=plain_res_vecs)
##
##vec_ops.run_test(d2v_com, polar_vecs, d2vcorpus, vecs=1, epochs=50000,
##                 write_to=polar_res_vecs)
##
##vec_ops.run_test(d2v_com, coed_vecs, d2vcorpus, vecs=1, epochs=50000,
##                 write_to=coed_res_vecs)
