import gensim
import os
import string
from preprocess import Preprocess
import vec_ops1, vec_ops
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

dirpath = "[local disk directory path to files]"


##price data must be stored in columns, with the tickers matching the names
## in the corpus
##
price_data = os.path.join("[path to price data in csv format]")
price_cols = ['Date', 'ATRL_Avg', 'OGDC_Avg', 'NRL_Avg', 'HUBC_Avg',
                  'KAPCO_Avg', 'PSO_Avg', 'PPL_Avg']


stringops = Preprocess(pricedata=price_data, datacols=price_cols)
vecOps = vec_ops.VectorOperations()
vecOpsSeq = vec_ops1.VectorOperations()

jsonfile = os.path.join(dirpath, "final_cor.json")

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

#models are not included in the repo

d2v_dbow = Doc2Vec.load('d2vmodel.model')
d2v_dm = Doc2Vec.load('d2vmodel_dm.model')
d2v_com = Doc2Vec.load('d2v_test.model')


#custom concatenation of dbow & dm
#this concatenates the paragraph vectors and the word vectors
vecOps.concatenate_d2v(d2v_com, d2v_dbow, d2v_dm)


#defining text files for storing testing data and results
plain_sents_t1 = 'plain_sents_t1m1.txt'
polar_sents_t1 = 'polar_sents_t1m2.txt'
coed_sents_t1 = 'coed_sents_t1m3.txt'

plain_sents_t3 = 'plain_sents_t3m1.txt'
polar_sents_t3 = 'polar_sents_t3m2.txt'
coed_sents_t3 = 'coed_sents_t3m3.txt'

plain_res_t1 = 'plain_res_t1m1.txt'
polar_res_t1 = 'polar_res_t1m2.txt'
coed_res_t1 = 'coed_res_t1m3.txt'

plain_res_vecs = 'plain_res_t2m1.txt'
polar_res_vecs = 'polar_res_t2m2.txt'
coed_res_vecs = 'coed_res_t2m3.txt'

plain_res_t3 = 'plain_res_t3m1.txt'
polar_res_t3 = 'polar_res_t3m2.txt'
coed_res_t3 = 'coed_res_t3m3.txt'

#define pos taggin filter - this is a positive filter
#it will keep the listed ones and remove the rest
#this input is as a nested list, with two items
#the first will filter words from the sim of target word
#second will filter words from the sim words of the sim word of the target word.

tagfilters = [['N'], ['V', 'J', 'R']]
polscore = 0.05

#T1

print("Running T1")

plain_sents = vecOps.plain_sents(d2v_com, 'pso', tag_filters=tagfilters,
                           write_to=plain_sents_t1, topn=25)


polar_sents = vecOps.polar_sents(d2v_com, 'pso', tag_filters=tagfilters,
                                 write_polar_sents=polar_sents_t1, pol_score=polscore,
                                 topn=25)

coed_sents = vecOps.coed_polar_sents(d2v_com, 'pso', tag_filters=tagfilters,
                                       write_coed_sents=coed_sents_t1,
                                       pol_score=polscore, vec_len=50, topn=25)

vecOps.run_sent_test(d2v_com, [d2v_dbow, d2v_dm], plain_sents, d2vcorpus, polar_sents=0, epochs=80000,
                 write_to=plain_res_t1)

vecOps.run_sent_test(d2v_com, [d2v_dbow, d2v_dm], polar_sents, d2vcorpus, epochs=80000,
                 write_to=polar_res_t1)

vecOps.run_sent_test(d2v_com, [d2v_dbow, d2v_dm], coed_sents, d2vcorpus, epochs=80000,
                 write_to=coed_res_t1)


#T2

print("Running T2")

vec_shape = 600

sents_vecs = vecOps.plain_vecs(d2v_com, 'pso', tag_filters=tagfilters,
                                topn=25, shape_r=vec_shape)

polar_vecs = vecOps.polar_vecs(d2v_com, 'pso', tag_filters=tagfilters,
                               topn=25, shape_r=vec_shape)

coed_vecs = vecOps.coed_polar_vecs(d2v_com, 'pso', tag_filters=tagfilters,
                                    topn=25, shape_r=vec_shape)

vecOps.run_vec_test(d2v_com, sents_vecs, d2vcorpus, polar_sents=0,
                    write_to=plain_res_vecs)

vecOps.run_vec_test(d2v_com, polar_vecs, d2vcorpus, write_to=polar_res_vecs)

vecOps.run_vec_test(d2v_com, coed_vecs, d2vcorpus, write_to=coed_res_vecs)

#T3

print("Running T3")

plain_sents_seq = vecOpsSeq.plain_sents(d2v_com, 'pso', tag_filters=tagfilters,
                           write_to=plain_sents_t3, topn=25)


polar_sents_seq = vecOpsSeq.polar_sents(d2v_com, 'pso', tag_filters=tagfilters,
                                 write_polar_sents=polar_sents_t3, pol_score=polscore,
                                 topn=25)

coed_sents_seq = vecOpsSeq.coed_polar_sents(d2v_com, 'pso', tag_filters=tagfilters,
                                       write_coed_sents=coed_sents_t3,
                                       pol_score=polscore, vec_len=50, topn=25)

vecOpsSeq.run_sent_test(d2v_com, [d2v_dbow, d2v_dm], plain_sents_seq, d2vcorpus, polar_sents=0, epochs=80000,
                 write_to=plain_res_t3)

vecOpsSeq.run_sent_test(d2v_com, [d2v_dbow, d2v_dm], polar_sents_seq, d2vcorpus, epochs=80000,
                 write_to=polar_res_t3)

vecOpsSeq.run_sent_test(d2v_com, [d2v_dbow, d2v_dm], coed_sents_seq, d2vcorpus, epochs=80000,
                 write_to=coed_res_t3)


plain_res_t1_h = 'plain_res_t1m1_h.txt'
polar_res_t1_h = 'polar_res_t1m2_h.txt'
coed_res_t1_h = 'coed_res_t1m3_h.txt'


plain_res_t3_h = 'plain_res_t3m1_h.txt'
polar_res_t3_h = 'polar_res_t3m2_h.txt'
coed_res_t3_h = 'coed_res_t3m3_h.txt'


print("Running T1-H")

vecOps.run_sent_test(d2v_com, [d2v_dbow, d2v_dm], plain_sents, d2vcorpus, use_holder=True,
                     polar_sents=0, epochs=80000, write_to=plain_res_t1_h)

vecOps.run_sent_test(d2v_com, [d2v_dbow, d2v_dm], polar_sents, d2vcorpus, use_holder=True,
                     epochs=80000, write_to=polar_res_t1_h)

vecOps.run_sent_test(d2v_com, [d2v_dbow, d2v_dm], coed_sents, d2vcorpus, use_holder=True,
                     epochs=80000, write_to=coed_res_t1_h)

print("Running T3-H")

vecOpsSeq.run_sent_test(d2v_com, [d2v_dbow, d2v_dm], plain_sents_seq, d2vcorpus,
                        use_holder=True, polar_sents=0, epochs=80000, write_to=plain_res_t3_h)

vecOpsSeq.run_sent_test(d2v_com, [d2v_dbow, d2v_dm], polar_sents_seq, d2vcorpus, use_holder=True,
                        epochs=80000, write_to=polar_res_t3_h)

vecOpsSeq.run_sent_test(d2v_com, [d2v_dbow, d2v_dm], coed_sents_seq, d2vcorpus, use_holder=True,
                        epochs=80000, write_to=coed_res_t3_h)

print("DONE")
