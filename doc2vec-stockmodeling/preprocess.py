import re
import string
import os
import smart_open
import json
from nltk import word_tokenize, pos_tag, sent_tokenize
from gensim.utils import simple_preprocess
from datetime import datetime
from datetime import timedelta
import pandas as pd




class Preprocess:
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    text_index = 1
    deftags = (0, ["N", "V", "R", "J", "P", "U"])
    tagsm = deftags
    sent_count = 0
    word_count = 0
    avg_para_len = 0
    price_date_gap = 3
    stock_data = pd.DataFrame()
    


    
    def __init__(self, pricedata=None, datacols=None):
        print("called")
        if pricedata:
            if datacols:
                self.stock_data = pd.read_csv(pricedata,
                                              usecols=datacols)
            else:
                try:
                    raise Exception("The datacols value must be provided when price data file is specified.")
                except Exception as err:
                    print(err)

        def convertDate(date):
            n_date = re.sub(self.regex, r' ', date).split()
            #yr, mth, day
            n_date = datetime(int(n_date[2]),
                              int(n_date[0]),
                              int(n_date[1]))
            return n_date
                            
        if not self.stock_data.empty:
            self.stock_data['Date'] = self.stock_data['Date'].apply(convertDate)
        


    def getCorpusStats(self):
        return self.sent_count, self.word_count, self.avg_para_len
    
    
    def getJSONData(self, filepath, text_index=-1, stock_data=False,
                    stock_day_ct=1, max_fwd_days=10, *jsonargs):
        f = open(filepath)
        data = json.load(f)
        corpus_data = []
        if text_index > -1:
            self.text_index = text_index
        else:
            try:
                raise Exception("Must assign an index for text stored in JSON.")
            except Exception as error:
                print(error)
        for i in data:
            item = ()
            if len(jsonargs) > 0:
                for j in jsonargs:
                    value = (i[j],)
                    item = item + value
                corpus_data.append(item)
            else:
                value = i['article']
                name = i['name']
                ##date stored in raw corpus must be in the form "full month name dd, yyyy"
                date = self.convertTextDate(i['date'])
                item = (name.upper(), value, date)
                if stock_data:
                    stock_tag = self.getStockData(date, i['name'].upper())
                    item = item + (stock_tag,)
                corpus_data.append(item)
        self.calcCorpusStats(corpus_data)
        return corpus_data

    
    def calcCorpusStats(self, corpus):
        total_ct = 0
        para_len = 0
        sent_ct = 0
        word_ct = 0
        for i in corpus:
            item = i[self.text_index]
            para_len += len(item)
            total_ct += 1
            sent_ct += len(sent_tokenize(item))
            word_ct += len(word_tokenize(item))
        self.avg_para_len = para_len / total_ct
        self.sent_count = sent_ct
        self.word_count = word_ct
        
    
    def getStockData(self, date, ticker, day_count=1, max_fwd_days=10):
        totalchange = 0
        day_itr = 0
        i = 0
        ##in the test data, the stock prices were averaged, basically, a moving
        ## average was used, and stored in seperate columns.
        ##For general use, ticker can be modified to suit the dataset.
        ticker = ticker + '_Avg'
        data_val = pd.DataFrame()          
        n_date = date

        def holiday_adjustment(df, val, date, days_iter, ticker, max_days):
            while val.empty:
                days_iter += 1
                n_date = date + timedelta(days=days_iter)
                val = df.loc[self.stock_data['Date'] == n_date,
                                              ticker]
                if day_itr > max_days:
                    break
            return val, days_iter

        change = 0
        for i in range(day_count):
            data_val, days_itr = holiday_adjustment(self.stock_data,
                                                    data_val, n_date,
                                                    day_itr, ticker,
                                                    max_fwd_days)
            day_itr += 1 
            n_date = date + timedelta(days=day_itr)
            if not data_val.empty:
                change += data_val.item()
            

        if change:
            totalchange = change / day_count
        else:
            totalchange = 0
        
        return totalchange
       
    
        
    def convertTextDate(self, date):
        n_date = datetime(2022, 9, 1)
        if date:
            n_date = re.sub(self.regex, r' ', date)
            n_date = n_date.split()
            n_date = datetime(int(n_date[2]),
                              datetime.strptime(n_date[0], '%B').month,
                              int(n_date[1]))
        return n_date
    


    def getTextData(self, filepath):
        corpus = []
        f = open(filepath)
        for i in enumerate(f):
            corpus.append(i)
        return corpus


    def saveText(self, corpus_lines, save_flag = 'w', file_name='corpus.txt'):
        filename = file_name
        with open(filename, save_flag) as f:
            for i in corpus_lines:
                f.write(i + '\n')
        
        return os.path.join('./', filename)


    def breakCorpusLines(self, corpus):
        lines = []
        for i in corpus:
            line = i[self.getTextIndex()]
            line1 = re.sub(r'[0-9]+\.', r' ', line)
            line2 = re.findall(r'.*?\.', line1)
            for j in line2:
                lines.append(j)
        return lines
            

    
    #basic preprocess for all data
    ##target_names is a dictionary for regex, all replace_regex and replace_with
    def preprocess(self, text, tags=None, target_names=None, remove_nnp=False):
        replacement1 = re.sub('-', '', text)
        #combine proper nouns
        replacement2 = self.combineProperNouns(replacement1)
        replacement3 = replacement2        
        if target_names:
            replacement3 = self.processTargetName(replacement2, \
                         replace_dict=target_names)
                              
        #select tags
        replacement4 = replacement3
        if tags:
            self.setTags(tags)
            if remove_nnp:
                if target_names == None:
                    raise Exception("Target name must be provided to remove NNPs")
            replacement4 = self.selectTags(replacement3, 
                                remove_nnp=remove_nnp, 
                        target_name=[x['replace'] for x in target_names])
        replacement5 = self.removePunctuation(replacement4)
        replacement6 = self.removeNumbers(replacement5)
        return replacement6.lower()




    def preprocessDocs(self, corpus, tags=None, target_names=None,
                   remove_nnp=False):
        #TODO write to file maybe ... loses tagging ... tagging reference would
        #still have to be held on ram. probably less memory that way, but
        #for now lets just go with this.
        index = 0
        for i in corpus:
            tuple_replace = ()
            for j in range(len(i)):
                if j == self.text_index:
                    item = (self.preprocess(i[j], tags, target_names, remove_nnp),)
                    tuple_replace = tuple_replace + item
                else:
                    item = (i[j],)
                    tuple_replace = tuple_replace + item
            corpus[index] = tuple_replace
            index += 1
        return corpus

    
              
    def preprocessSG(self, corpus, tags=None,
                     target_names=None, remove_nnp=False,
                     corpus_name='corpus.txt'):
        lines = []
        for j in corpus:
            text = j[self.text_index]
            lines += sent_tokenize(text)
        proclines = []
        for i in lines:
            textproc = self.preprocess(i, tags, target_names, remove_nnp)
            proclines.append(textproc)
        filepath = self.saveText(proclines, file_name=corpus_name)
        #TODO maybe call reset default tags after preprocess done
        return filepath
        
        
    
    ##target_name = list of target names
    def selectTags(self, text, remove_nnp=False, target_name=None):
        def fullTags(tag):
            tagfound = False
            for j in self.tagsm[1]:
                if j == tag:
                    tagfound = True
                    break
            return tagfound

        def shortTags(tag):
            tagfound = False
            for j in self.tagsm[1]:
                if tag.find(j, 0, 1) >= 0:
                    tagfound = True
                    break
            return tagfound

        def removeNNP(remove_nnp, nltk_tag, target):
            if remove_nnp:
                if 'NNP' in nltk_tag[1]:
                    if nltk_tag[0].lower() in target:
                        return False
                    else:
                        return True
                else:
                    return False
            else:
                return False

          
        taggedwords = []
        tokens = word_tokenize(text)
        tagged = pos_tag(tokens)
        
        for i in tagged:
            if len(i[0]) < 3:
                continue
            else:
                findreg = re.findall(r'\.|-|&|and\s', i[0], re.IGNORECASE)
                if len(findreg) > 0:
                    taggedwords.append(i[0])
                else:
                    if self.tagsm[0] > 0:
                        if fullTags(i[1]):
                            if removeNNP(remove_nnp, i, target_name):
                                continue
                            else:
                                taggedwords.append(i[0])
                    else:
                        if shortTags(i[1]):
                            if removeNNP(remove_nnp, i, target_name):
                                continue
                            else:
                                taggedwords.append(i[0])
        #print("Tagged \n", tagged)
        #print("Words \n", taggedwords)
        with open('checktags.txt', 'w') as f:
            pass
        with open('checktags.txt', mode='a', errors='ignore') as f:
            wstr = u'Tagged \n %s, \n Words \n %s \n' % (str(tagged),
                                                         str(taggedwords))
            f.write(wstr)
            
            
        return ' '.join(taggedwords)
        

    def tagFilter(self, tag_list, word, filter_short=True):
        def fullTags(tag, taglist):
            tagfound = False
            for j in taglist:
                if j == tag:
                    tagfound = True
                    break
            return tagfound

        def shortTags(tag, taglist):
            tagfound = False
            for j in taglist:
                if tag.find(j, 0, 1) >= 0:
                    tagfound = True
                    break
            return tagfound
        tag_found = False
        wtag = pos_tag([word])
        if filter_short:
            tag_found = shortTags(wtag[0][1], tag_list)
        else:
            tag_found = fullTags(wtag[0][1], tag_list)

        return tag_found
    
    
    def resetDefaultTags():
        self.tagsm = self.deftags

    def getDefaultTags():
        return self.deftags
    
    def setTags(self, tag_tuple):
        self.tagsm = tag_tuple
          
    def removePunctuation(self, text):
       item = text.encode("ascii", "ignore")
       return self.regex.sub(' ', item.decode())

    def removeNumbers(self, text):
        item = re.sub(r'[0-9]', r'', text)
        return item
        
    def combineProperNouns(self, text):
        def lowercasefirst(obj):
            return obj.group(0).lower()

        def lowercasesent(obj):
            return obj.group(0).lower()
        
        def addspace(obj):
            if '  ' in obj.group(0):
                return obj.group(0)
            else:
                return '  ' + obj.group(0)

        def capcombine(obj):
            replace = ""
            if ' ' in obj.group(0):
                replace = re.sub(r'\s+\Z', r'', obj.group(0))
                return replace
            else:
                return obj.group(0)

        lowerf = re.sub(r'\A\b[A-Z]|\A\s*\b[A-Z]|:\s*\b[A-Z]', lowercasefirst,
                        text)               
        dspaced = re.sub(r'\s*\b[a-z]+', addspace, lowerf)        
        ccaps = re.sub(r'\b[A-Z][a-z]+\s', capcombine, dspaced)
        lowersentf = re.sub(r'\.\s*[A-Z]*', lowercasesent, ccaps)
        #NOTE gensim tokenize will remove additional whitespace
        regularize = re.sub(r'  ', r' ', lowersentf)
        return regularize

    def processTargetName(self, text, replace_dict, ignore_case=True):
        replacedtext = text
        for i in replace_dict:
            replacedtext = re.sub(i['regex'], i['replace'], text,\
                            flags=re.IGNORECASE if ignore_case else 0)
            
        return replacedtext
        
        
   

    def getTextIndex(self):
        return self.text_index
