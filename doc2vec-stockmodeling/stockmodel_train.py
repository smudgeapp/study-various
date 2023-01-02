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

##TODO run training again with smaller window size 6 in w2v and 12 in d2v
##TODO very short window on nouns, double in nouns+verbs+adj+etc.
##TODO increase epochs
##TODO combine 2 versions of d2v

dirpath = "E:/Projects/word2vec/w2vgit/rssj"
dirpath2 = "C:/Users/HP/Downloads/w2v-wip/rssj"


jsonfile = os.path.join(dirpath, "final_cor.json")

stringops = Preprocess()

data = stringops.getJSONData(jsonfile)
#print(data[140:150])

sent_count, word_count, para_len = stringops.getCorpusStats()

minct = word_count / sent_count

##FIRST SG -- ONLY NOUNS

targetname = 'atrl'
company = r'pso'
repl_regex = r'\b(pakistanstateoil)'
target = {
    'replace_regex': repl_regex,
    'replace_with': company
    }

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

    
m_epochs1 = 70000
m_epochs2 = 50000
m_epochs3 = 50000
sg_vecsize = 300


sgonetags = (0, ['N', 'J', 'V', 'R'])
'''
sgonedata = stringops.preprocessSG(data, tags=sgonetags, target_names=regex_dict,
                                   remove_nnp=True, corpus_name="sg1cor.txt")

                                 
sgonemodel = Word2Vec(sg=1, min_count=6, epochs=m_epochs1, window=3,
                      vector_size=sg_vecsize)

sgonemodel.build_vocab(corpus_file=sgonedata, trim_rule=trimrule)

sgonemodel.train(corpus_file=sgonedata, total_examples=stringops.sent_count,
                 total_words=sgonemodel.corpus_total_words,
                 epochs=sgonemodel.epochs, compute_loss=True,
                 callbacks=[w2vcallback("SG1MODEL")])

sgonemodel.save("sgonemodel.model")

sgtwotags = (1, ["NN", "NNS", "JJ", "JJR", "JJS",
                 "RB", "RBR", "RBS", "VB", "VBP", "VBZ"])
##TODO give full tags and remove all nnps

sgtwodata = stringops.preprocessSG(data, tags=sgtwotags, target_names=regex_dict,
                                 remove_nnp=True, corpus_name="sg2cor.txt")

sgtwomodel = Word2Vec(sg=1, min_count=6, epochs=m_epochs2, window=6,
                      vector_size=sg_vecsize)

sgtwomodel.build_vocab(corpus_file=sgtwodata, trim_rule=trimrule)

sgtwomodel.train(corpus_file=sgtwodata, total_examples=stringops.sent_count,
                 total_words=sgtwomodel.corpus_total_words,
                 epochs=sgtwomodel.epochs,
                 compute_loss=True,
                 callbacks=[w2vcallback("SG2MODEL")])

sgtwomodel.save("sgtwomodel.model")


target_sim = list(sgonemodel.wv.most_similar(targetname))

class_vecs = []

tag_filter = ["J", "V", "R"]

checkingvecs = "checkvecs.txt"
for i in target_sim:
    vec = []
    vec.append(targetname.upper())
    vec.append(i[0].upper())
    class_sims = sgtwomodel.wv.most_similar(i[0])
    for j in class_sims:
        if stringops.tagFilter(tag_filter, j[0]):
            vec.append(j[0])
    with open(checkingvecs, 'a') as f:
        f.write(' '.join(vec) + '\n')
        f.close()

'''

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


d2vmodel = Doc2Vec(min_count=minct, epochs=m_epochs3, dbow_words=1,
                   vector_size=d2v_vecsize, window=minct / 2)

d2vmodel.build_vocab(d2vcorpus, trim_rule=trimrule)

##d2vmodel.train(d2vcorpus, total_examples=len(d2vcorpus),
##               epochs=d2vmodel.epochs)
##
##d2vmodel.save("d2vmodel.model")


d2vmodel_dm = Doc2Vec(min_count=minct, epochs=m_epochs3, dbow_words=1,
                     dm=1, dm_mean=1, vector_size=d2v_vecsize, window=minct)

d2vmodel_dm.build_vocab(d2vcorpus, trim_rule=trimrule)

##d2vmodel_dm.train(d2vcorpus, total_examples=len(d2vcorpus),
##                  epochs=d2vmodel_dm.epochs)
##
##d2vmodel_dm.save("d2vmodel_dm.model")



d2vmodel_test = Doc2Vec(min_count=minct, epochs=m_epochs3, dbow_words=1,
                   vector_size=600, window=minct / 2)

d2vmodel_test.build_vocab(d2vcorpus, trim_rule=trimrule)

##d2vmodel_test.train(d2vcorpus, total_examples=len(d2vcorpus),
##               epochs=d2vmodel_test.epochs)
##
##d2vmodel_test.save("d2vmodel_com.model")

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
