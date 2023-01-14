import string
from preprocess import Preprocess
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from nltk.sentiment import SentimentIntensityAnalyzer
import numpy as np
from numpy.linalg import norm
import datetime
import time

#CREATES VECTORS AS SEQUENCE TARGET-WHAT-HOW-TARGET-WHAT-HOW AND SO ON.

class VectorOperations:



    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
        self.stringops = Preprocess()


    def concatenate_d2v(self, target_model, dbow_model, dm_model, only_docs=False):
        for i in range(len(target_model.dv)):
            new_arr = np.concatenate([dbow_model.dv[i], dm_model.dv[i]])
            target_model.dv[i] = new_arr

        if not only_docs:
            for i in range(len(target_model.wv)):
                key = target_model.wv.index_to_key[i]
                dbow_ind = dbow_model.wv.key_to_index[key]
                dm_ind = dm_model.wv.key_to_index[key]
                n_vec = np.concatenate([dbow_model.wv[dbow_ind], dm_model.wv[dm_ind]])
                target_model.wv[i] = n_vec

    def nested_words(self, model, in_word, tag_filter, short_filter=True,
                     topn=10):
        sims = model.wv.most_similar(in_word, topn=topn)
        ot_vec = []
        for k in sims:
            vec = [in_word]
            if self.stringops.tagFilter(tag_filter, k[0], short_filter):
                vec.append(k[0])
            else:
                continue
            ot_vec.append(vec)
        return ot_vec
        

    ##Develops the sentences around the target word.
    ##It first gets the similarity output for the target word, applies the 1st
    ## filter to get the word that is in the target's context.
    ##Then applies a second filter to get the words in the similarity words
    ## filtered for the target word.
    ##Ultimately, this forms a group of words that are in the target's context
    ## and the words that are in the context of the target's context.
    ##This becomes a document vector for testing with the doc2vec model.

    ##model = the doc2vec/word2vec model to be used - gensim model
    ##target = target word in string
    ##tag_filters = nested list of filters in order of application
    #short_filter = if True, it filters by the first letter of nltk pos
    ##              tagging. Otherwise, uses the full-form tag.
    ##topn = number of context words to use for the target similarities only.
    ##write_to = file name in string format for saving the sentences. Only text
    ##              format is supported.
    def plain_sents(self, model, target, tag_filters=[["N"],["V", "J", "R"]],
                    short_filter=True, topn=10, write_to=None):
        
        target_sim = model.wv.most_similar(target, topn=topn)
        class_vecs = []
        if write_to:
            with open(write_to, 'w') as f:
                pass
        for i, item in enumerate(target_sim):
            vec = []
            #vec.append(target)
            tag_word = ''
            if tag_filters:
                if self.stringops.tagFilter(tag_filters[0], item[0], short_filter):
                    #vec.append(item[0])
                    tag_word = item[0]
                else:
                    continue
            else:
                #vec.append(item[0])
                tag_word = item[0]
            class_sims = model.wv.most_similar(item[0], topn=model.corpus_count)
            tag_filter2 = None
            if tag_filters:
                tag_filter2 = tag_filters[1]
            for j in class_sims:
                if tag_filter2:
                    if self.stringops.tagFilter(tag_filter2, j[0], short_filter):
                        vec.append(target)
                        vec.append(tag_word)
                        vec.append(j[0])
                    else:
                        continue
                else:
                    vec.append(j[0])
            class_vecs.append(vec)
            if write_to:
                with open(write_to, 'a') as f:
                    f.write('#' + str(i) + '\n' + ' '.join(vec) + ' \n')
        return class_vecs


    def plain_vecs(self, model, target, tag_filters=[["N"],["V", "J", "R"]],
                    short_filter=True, topn=10, write_to=None, shape_r=300,
                   avg=1):
        sents = self.plain_sents(model, target, tag_filters, short_filter, topn,
                                 write_to)
        vecs = []
        item_len = 0
        for i, item in enumerate(sents):
            item_len = len(item)
            vec = np.zeros(shape=(shape_r,))
            for i, word in enumerate(item):
                vc = model.wv[word]
                vec = np.add(vec, vc)
            vec = vec / item_len if avg > 0 else vec
            vecs.append(vec)

        return vecs
        

    ##Develop polar sentences based on word-by-word polarity from nltk sentiment
    ## analyzer. Places the results in a dictionary with key 'pos_vec' for
    ## positive and 'neg_vec' vice versa.

    ##write_polar_sents = file name in string format for saving the sentences. Only text
    ##              format is supported
    ##pol_score = range of polarity score for filtering words.
    ##include_neuts = if True, it will include the neutral words, that is words,
    ##                  within the score range -pol_score < x < pol_score
    ##                  where x is the word's compound polarity score
    def polar_sents(self, model, target, tag_filters=[["N"], ["V", "J", "R"]],
                    short_filter=True, topn=10, write_plain_sents=None,
                    write_polar_sents=None, pol_score=0.0,
                    include_neuts=False):
        class_vecs = self.plain_sents(model, target, tag_filters,
                                      short_filter, topn, write_plain_sents)
        if write_polar_sents:
            with open(write_polar_sents, 'w') as f:
                pass
        polar_sents = []
        for i, text_m in enumerate(class_vecs):
            base_vec = [text_m[0], text_m[1]]
            sent = {
                'pos_vec': [],
                'neg_vec': []
                }
            itr = 0
            for k, text in enumerate(text_m):
                if k == itr + 2:
                    itr += 3
                    score = self.sia.polarity_scores(text)['compound']
                    if score > pol_score:
                        sent['pos_vec'] = sent['pos_vec'] + base_vec + [text]
                    elif score < -pol_score:
                        sent['neg_vec'] = sent['neg_vec'] + base_vec + [text]
                    else:
                        if include_neuts:
                            sent['pos_vec'] = sent['pos_vec'] + base_vec + [text]
                            sent['neg_vec'] = sent['neg_vec'] + base_vec + [text]
            polar_sents.append(sent)    
            if write_polar_sents:
                with open(write_polar_sents, 'a') as f:
                    f.write(u'Positive Sent: #: %s, Sent: %s\n\n' %
                            (str(i), ' '.join(sent['pos_vec'])))
                    f.write(u'Negative Sent: #: %s, Sent: %s\n\n' %
                            (str(i), ' '.join(sent['neg_vec'])))
        return polar_sents

    def polar_vecs(self, model, target, tag_filters=[["N"], ["V", "J", "R"]],
                    short_filter=True, topn=10, write_plain_sents=None,
                    write_polar_sents=None, pol_score=0.0,
                    include_neuts=False, shape_r=300, avg=1):
        sents = self.polar_sents(model, target, tag_filters,
                                      short_filter, topn, write_plain_sents,
                                      write_polar_sents, pol_score,
                                      include_neuts)
        vecs = []
        for i, item in enumerate(sents):
            pos_vec = np.zeros(shape=(shape_r,))
            neg_vec = np.zeros(shape=(shape_r,))
            pos_len = len(item['pos_vec'])
            neg_len = len(item['neg_vec'])
            vec_item = {
                'pos_vec': [],
                'neg_vec': []
                }
            for i, word in enumerate(item['pos_vec']):
                vc = model.wv[word]
                pos_vec = np.add(pos_vec, vc)
            pos_vec = pos_vec / pos_len if avg > 0 else pos_vec
            for i, word in enumerate(item['neg_vec']):
                vc = model.wv[word]
                neg_vec = np.add(neg_vec, vc)
            neg_vec = neg_vec / neg_len if avg > 0 else neg_vec
            vec_item['pos_vec'] = pos_vec
            vec_item['neg_vec'] = neg_vec
            vecs.append(vec_item)

        return vecs
    
    ##Develops correlated polar sentences. Obtains polar sentences and then uses
    ## SVD to determine the correlation between the target word, its context word,
    ## and the polar word in the first sim-word's context.
    
    ##write_coed_sents = file name in string format for saving the sentences. Only text
    ##              format is supported
    ##vec_len = specify length of sentence in number of words
    def coed_polar_sents(self, model, target, tag_filters=[["N"], ["V", "J", "R"]],
                         short_filter=True, topn=10, write_plain_sents=None,
                         write_polar_sents=None, write_coed_sents=None,
                         pol_score=0.0, include_neuts=False, vec_len=25):
        polar_vecs = self.polar_sents(model, target, tag_filters,
                                      short_filter, topn, write_plain_sents,
                                      write_polar_sents, pol_score,
                                      include_neuts)
        corr_vecs = []
        if write_coed_sents:
            with open(write_coed_sents, 'w') as f:
                pass
        for i, vec in enumerate(polar_vecs):
            name = vec['pos_vec'][0]
            word = vec['pos_vec'][1]
            base_vec = [name, word]
            item = {
                'pos_vec': [],
                'neg_vec': []
                }
            pos_vec = self.svd_tricoed_sent(model, vec['pos_vec'],
                                           vec_len=vec_len)
            neg_vec = self.svd_tricoed_sent(model, vec['neg_vec'],
                                          vec_len=vec_len)
            for word in pos_vec:                
                item['pos_vec'] = item['pos_vec'] + base_vec + [word]
            for word in neg_vec:
                item['neg_vec'] = item['neg_vec'] + base_vec + [word]
            corr_vecs.append(item)
            if write_coed_sents:
                with open(write_coed_sents, 'a') as f:
                    f.write(u'Positive Vec: #: %s, vec: %s\n\n' %
                            (i, ' '.join(item['pos_vec'])))
                    f.write(u'Negative Vec: #: %s, vec: %s\n\n' %
                            (i, ' '.join(item['neg_vec'])))
                    
        return corr_vecs

##This method is redundant - when using the average of word vectors instead of the words
## words themselves, the order would not be important because the same vectors would be
## added and then averaged. So the result of this will be the same as that of polar vecs.

##However, if we were to modify the length of the vector, then the results will be
## different.

    def coed_polar_vecs(self, model, target, tag_filters=[["N"], ["V", "J", "R"]],
                         short_filter=True, topn=10, write_plain_sents=None,
                         write_polar_sents=None, write_coed_sents=None,
                         pol_score=0.0, include_neuts=False, vec_len=25,
                        shape_r=300, avg=1):
        sents = self.coed_polar_sents(model, target, tag_filters,
                                      short_filter, topn, write_plain_sents,
                                      write_polar_sents, write_coed_sents, pol_score,
                                      include_neuts, vec_len)
        vecs = []
        for i, item in enumerate(sents):
            pos_vec = np.zeros(shape=(shape_r,))
            neg_vec = np.zeros(shape=(shape_r,))
            pos_len = len(item['pos_vec'])
            neg_len = len(item['neg_vec'])
            vec_item = {
                'pos_vec': [],
                'neg_vec': []
                }
            for i, word in enumerate(item['pos_vec']):
                vc = model.wv[word]
                pos_vec = np.add(pos_vec, vc)
            pos_vec = pos_vec / pos_len if avg > 0 else pos_vec
            for i, word in enumerate(item['neg_vec']):
                vc = model.wv[word]
                neg_vec = np.add(neg_vec, vc)
            neg_vec = neg_vec / neg_len if avg > 0 else neg_vec
            vec_item['pos_vec'] = pos_vec
            vec_item['neg_vec'] = neg_vec
            vecs.append(vec_item)

        return vecs
    
    ##Convenience method for running tests,
    ##polar_sents=1 for polar sents, both
    ## just polar sents and correlated polar sents
    ##vecs = 1 for using numeric vectors instead of word vectors,
    ## for both polar and correlated polar sents
    def run_sent_test(self, d2vholder, d2vmodels, sents_vecs, corpus, polar_sents=True,
                      use_holder=False, topn=10, epochs=1000, write_to=None):
        if polar_sents:
            self.run_polar_sent_test(d2vholder, d2vmodels, sents_vecs, corpus, use_holder=use_holder,
                                     topn=topn, epochs=epochs, write_to=write_to)
        else:
            self.run_plain_sent_test(d2vholder, d2vmodels, sents_vecs, corpus, use_holder=use_holder,
                                     topn=topn, epochs=epochs, write_to=write_to)
        

    def run_vec_test(self, d2vmodel, sents_vecs, corpus, polar_sents=True, topn=10,
                     write_to=None):
        if polar_sents:
            self.run_polar_vec_test(d2vmodel, sents_vecs, corpus, topn=topn,
                                        write_to=write_to)
        else:
            self.run_plain_vec_test(d2vmodel, sents_vecs, corpus, topn=topn,
                                     write_to=write_to)
    

    def run_polar_sent_test(self, d2vholder, d2vmodels, sents, corpus, use_holder=False,
                            topn=10, epochs=1000, write_to=None):
        if write_to:
            with open(write_to, 'w') as f:
                pass

        for i, sent in enumerate(sents):
            pos_vec = []
            neg_vec = []
            if use_holder:
                pos_vec = d2vholder.infer_vector(sent['pos_vec'], epochs=epochs)
                neg_vec = d2vholder.infer_vector(sent['neg_vec'], epochs=epochs)
            else:
                pos_vec = np.concatenate([model.infer_vector(sent['pos_vec'], epochs=epochs) for model in d2vmodels])
                neg_vec = np.concatenate([model.infer_vector(sent['neg_vec'], epochs=epochs) for model in d2vmodels])
            
            sim_pos = d2vholder.dv.most_similar(pos_vec, topn=topn)
            sim_neg = d2vholder.dv.most_similar(neg_vec, topn=topn)
            if write_to:
                with open(write_to, 'a') as f:
                    pos_tags = [str(x) for x in corpus[sim_pos[0][0]].tags]
                    neg_tags = [str(x) for x in corpus[sim_neg[0][0]].tags]
                    f.write(u'Sentiment #: %s \n' % (str(i)))
                    f.write(u'Positive: %s \n' % (sim_pos))
                    f.write(u'1st Pos Sim: \n Tags: %s, \n Item: <<%s>> \n\n' %
                            (', '.join(pos_tags),
                             ' '.join(corpus[sim_pos[0][0]].words[:20])))
                    f.write(u'Negative: %s \n' % (sim_neg))
                    f.write(u'1st Neg Sim: \n Tags: %s, \n Item: <<%s>> \n\n' %
                            (', '.join(neg_tags),
                             ' '.join(corpus[sim_neg[0][0]].words[:20])))

    def run_polar_vec_test(self, d2vmodel, vecs, corpus, topn=10, write_to=None):
        if write_to:
            with open(write_to, 'w') as f:
                pass
        for i, item in enumerate(vecs):
            sim_pos = d2vmodel.dv.most_similar(item['pos_vec'], topn=topn)
            sim_neg = d2vmodel.dv.most_similar(item['neg_vec'], topn=topn)
            if write_to:
                with open(write_to, 'a') as f:
                    pos_tags = [str(x) for x in corpus[sim_pos[0][0]].tags]
                    neg_tags = [str(x) for x in corpus[sim_neg[0][0]].tags]
                    f.write(u'Sentiment #: %s \n' % (str(i)))
                    f.write(u'Positive: %s \n' % (sim_pos))
                    f.write(u'1st Pos Sim: \n Tags: %s, \n Item: <<%s>> \n\n' %
                            (', '.join(pos_tags),
                             ' '.join(corpus[sim_pos[0][0]].words[:20])))
                    f.write(u'Negative: %s \n' % (sim_neg))
                    f.write(u'1st Neg Sim: \n Tags: %s, \n Item: <<%s>> \n\n' %
                            (', '.join(neg_tags),
                             ' '.join(corpus[sim_neg[0][0]].words[:20])))
    

    def run_plain_sent_test(self, d2vholder, d2vmodels, sents, corpus, use_holder=False,
                            topn=10, epochs=1000, write_to=None):
        if write_to:
            with open(write_to, 'w') as f:
                pass

        for i, sent, in enumerate(sents):
            vec = np.concatenate([model.infer_vector(sent, epochs=epochs) for model in d2vmodels])
            if use_holder:
                vec = d2vholder.infer_vector(sent, epochs=epochs)
            sim = d2vholder.dv.most_similar(vec, topn=topn)
            if write_to:
                with open(write_to, 'a') as f:
                    str_tags = [str(x) for x in corpus[sim[0][0]].tags]
                    f.write(u'Serial #: %s \n' % (str(i)))
                    f.write(u'1st Sim: \n Tags: %s \n, Item: <<%s>> \n\n' %
                            (', '.join(str_tags),
                            ' '.join(corpus[sim[0][0]].words[:20])))

    def run_plain_vec_test(self, d2vmodel, vecs, corpus, topn=10, write_to=None):
        if write_to:
            with open(write_to, 'w') as f:
                pass

        for i, vec in enumerate(vecs):
            sim = d2vmodel.dv.most_similar(vec, topn=topn)
            if write_to:
                with open(write_to, 'a') as f:
                    str_tags = [str(x) for x in corpus[sim[0][0]].tags]
                    f.write(u'Serial #: %s \n' % (str(i)))
                    f.write(u'1st Sim: \n Tags: %s \n, Item: <<%s>> \n\n' %
                            (', '.join(str_tags),
                            ' '.join(corpus[sim[0][0]].words[:20])))

    def svd_tricoed_sent(self, model, word_vec, vec_len=10, increment=2):
        ##define coed range
        word_coed = {}
        add_len = 0
        for i, word in enumerate(word_vec):
            if i == add_len + increment:
                vec = [model.wv[word_vec[0]], model.wv[word_vec[1]],
                       model.wv[word]]            
                word_coed[word] = self.tricoed(vec)
                add_len = i + 1
        sortd_list = sorted(word_coed.items(), key=lambda x: x[1], reverse=True)
        return [i[0] for i in sortd_list[:vec_len]]


    def tricoed(self, vec):
        arr = np.stack(vec, axis=1)
        unit_arr = arr / np.linalg.norm(arr, axis=0)
        U, S, Vt = np.linalg.svd(unit_arr, full_matrices=False)
        coed = S[0] / unit_arr.shape[1]
        return coed


      
    def doc_cos_sim(self, vector, model, topn=10):
        sim_vals = {}
        top_n = topn
        for i in range(len(model.dv)):
            sim = np.dot(vector, model.dv[i]) / (norm(vector) *
                                                     norm(model.dv[i]))
            sim_vals[i] = sim
        sortd_list = sorted(sim_vals.items(), key=lambda x: x[1], reverse=True)
        if top_n > len(sortd_list):
            top_n = len(sortd_list)
        return [item for item in sortd_list[:top_n]]


    def exp_norm(self, vector):
        new_arr = np.exp(vector - np.max(vector))
        return new_arr

    def ss_norm(self, vector):
        new_arr = vector - np.max(vector)
        return np.sqrt(np.square(new_arr))


    def train_split(self, x_vals, y_vals, test_size=0.3):
        total_len = len(x_vals)
        test_len = int(round(test_size * total_len, 0))
        train_len = total_len - test_len
        x_train = [x for x in x_vals[:train_len]]
        x_test = [x for x in x_vals[train_len:total_len]]
        y_train = [x for x in y_vals[:train_len]]
        y_test = [x for x in y_vals[train_len:total_len]]
        return x_train, x_test, y_train, y_test
