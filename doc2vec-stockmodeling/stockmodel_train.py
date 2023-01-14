import gensim
import os
import string
from gensim.models import Word2Vec
from gensim.models.doc2vec import Doc2Vec
from w2vcallback import w2vcallback
from nltk import word_tokenize, sent_tokenize, pos_tag
import re
import logging
import json
from preprocess import Preprocess
from sklearn.decomposition import PCA
from matplotlib import pyplot
import threading

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


dirpath = "[local disk directory path to files]"


jsonfile = os.path.join(dirpath, "final_cor.json")

stringops = Preprocess()

data = stringops.getJSONData(jsonfile)

sent_count, word_count, para_len = stringops.getCorpusStats()

minct = word_count / sent_count


regex_list = [r'\b(pakistanstateoil)', r'\b(oil&gasdevelopmentcompany)',
              r'\b(oilandgasdevelopmentcompany)', r'\b(ogdcl)',
              r'\b(pakistanpetroleum)',
              r'\b(attockrefinery)', r'\b(nationalrefinery)',
              r'\b(hubpowercompany)', r'\b(hubco)', r'\b(kotaddupower)']
replace_list = [r'pso', r'ogdc', r'ogdc', r'ogdc', r'ppl', r'atrl',
                r'nrl', r'hubc', r'hubc',
                r'kapco']

regex_dict = []

for i in range(len(regex_list)):
    item = {
        'regex': regex_list[i],
        'replace': replace_list[i]
        }
    regex_dict.append(item)

def trimrule(word, count, min_count):
    if len(word) < 3:
        return gensim.utils.RULE_DISCARD

    if count < min_count:
        return gensim.utils.RULE_DISCARD

    
m_epochs = 50000


def d2vTagData(corpus):
    itr = 0
    for date, stockval, name, item in corpus:
        tokens = gensim.utils.simple_preprocess(item)
        #tag = [date, itr]
        itr += 1
        yield gensim.models.doc2vec.TaggedDocument(tokens, [itr])
        
        
        
d2v_vecsize = 300

d2vdata = stringops.preprocessDocs(data, tags=sgonetags,
                                   target_names=regex_dict,
                                     remove_nnp=True)

d2vcorpus = list(d2vTagData(d2vdata))


d2vmodel = Doc2Vec(min_count=minct, epochs=m_epochs, dbow_words=1,
                   vector_size=d2v_vecsize, window=minct / 2)

d2vmodel.build_vocab(d2vcorpus, trim_rule=trimrule)


d2vmodel_dm = Doc2Vec(min_count=minct, epochs=m_epochs, dbow_words=1,
                     dm=1, dm_mean=1, vector_size=d2v_vecsize, window=minct / 2)

d2vmodel_dm.build_vocab(d2vcorpus, trim_rule=trimrule)


d2vmodel_test = Doc2Vec(min_count=minct, epochs=m_epochs, dbow_words=1,
                   vector_size=600, window=minct / 2)

d2vmodel_test.build_vocab(d2vcorpus, trim_rule=trimrule)


def wrapper(name, model, corpus, epochs):
    model.train(d2vcorpus, total_examples=len(corpus), epochs=model.epochs)
    model.save(name)

t1 = threading.Thread(target=wrapper, args=("d2vmodel.model", d2vmodel, d2vcorpus, m_epochs3))
t2 = threading.Thread(target=wrapper, args=("d2vmodel_dm.model", d2vmodel_dm, d2vcorpus, m_epochs3))
t3 = threading.Thread(target=wrapper, args=("d2v_test.model", d2vmodel_test, d2vcorpus, m_epochs3))

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()

print("DONE")
