import io
from torchtext.vocab import build_vocab_from_iterator
from torchtext.data.functional import to_map_style_dataset
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from torch.nn.functional import pad
import torch
import os
import pandas as pd
import csv
import unicodedata
import re
import numpy as np
import json
import spacy


train_set = 'img_desc_ABC.json'
valid_set = 'image_desc_valid.json'
all_data = 'all_img.json'

train_iter = ''
train_src_len = 0
train_tgt_len = 0
spacy_en = ''

try:
    #spacy_de = spacy.load('de_core_news_sm')
    spacy_en = spacy.load('en_core_web_sm')    
except IOError:
    #os.system("python -m spacy download de_core_news_sm")
    #spacy_de = spacy.load('de_core_news_sm')
    os.system("python -m spacy download en_core_web_sm")
    spacy_en = spacy.load('en_core_web_sm')
    

try:
    spacy_lg = spacy.load('en_core_web_lg')
except:
    os.system("python -m spacy download en_core_web_lg")
    spacy_lg = spacy.load('en_core_web_lg')

spacy_lg = spacy.load('en_core_web_lg')   

words = set(spacy_en.vocab.strings)
words_lg = set(spacy_lg.vocab.strings)

print(type(spacy_lg.vocab.strings))



with open(train_set, 'r', encoding='utf-8') as f:
    data = json.load(f)
    ctx = [ct['tweet'] for ct in data]
    resp = [res['image'] for res in data]
    train_iter = to_map_style_dataset(zip(ctx, resp))


valid_iter = ''
valid_src_len = 0
valid_tgt_len = 0

with open(valid_set, 'r', encoding='utf-8') as f:
    data = json.load(f)
    ctx = [ct['tweet'] for ct in data]
    resp = [res['image'] for res in data]
    valid_iter = to_map_style_dataset(zip(ctx, resp))


def tokenizer(text):
    return([tok for tok in text.split(' ')])


def yield_tokens(file_path, key):
    with open(file_path, encoding='utf-8') as f:
        data = json.load(f)
        items = [it[key] for it in data]
        for item in items:
            voc = item.strip().split()
            yield voc


def all_tokens(file_path):
    with open(file_path, encoding='utf-8') as f:
        data = json.load(f)
        ctx = [it['tweet'] for it in data]
        resp = [res['image'] for res in data]
        items = ctx + resp
        #print(items)
##        for item in items:
##            voc = item.strip().split()
##            yield voc

all_tokens(all_data)

def load_vocab(file_path, name='tweet_img_vocab.pt'):
    spc = ["<s>", "</s>", "<blank>", "<unk>"]
    
    def tokenize_en(text):        
        return tokenize(text, spacy_en)
                            
    if not os.path.exists(name):
        all_vocab = build_vocab_from_iterator(all_tokens(file_path),
                                      specials=spc)
        all_vocab.set_default_index(all_vocab["<unk>"])      
        
        torch.save(all_vocab, name)
    else:
        all_vocab = torch.load(name)

    #print(len(src_vocab))
    #save all vocab in in vocab - torch save dict for vocab with src and tgt
    return all_vocab

#all_vocab = load_vocab(all_data)

def spacy_vocab(vocab_path='tweet_img_vocab_ABC.pt'):
    spc = ["<s>", "</s>", "<blank>", "<unk>"]
    words = set(spacy_en.vocab.strings)
    spacy_words = []
    for i, j in enumerate(words):       
        spacy_words.append(j.lower())
    ##TODO words not being added in vocab - check why
    #items = []
    full_vocab = []
    with open(train_set, encoding='utf-8') as f:
        data = json.load(f)
        ctx = [it['tweet'] for it in data]
        resp = [res['image'] for res in data]
        items = ctx + resp
        for item in items:
            voc = item.strip().split()
            for i, j in enumerate(voc):
                #print(i)
                full_vocab.append(j.lower())
                
    all_words = spacy_words + full_vocab
    print(all_words[:20])
    def tokenizer():
        for i in all_words:
            yield i
    
    if not os.path.exists(vocab_path):
        all_vocab = build_vocab_from_iterator([all_words], specials=spc)
        all_vocab.set_default_index(all_vocab["<unk>"])
        torch.save(all_vocab, vocab_path)
    else:
        all_vocab = torch.load(vocab_path)
    return all_vocab

all_vocab = spacy_vocab()

print(len(all_vocab))
#print(all_vocab.get_stoi()['rallybook'])

#print(all_vocab.get_stoi())
##
##with open("vocab_dict.json", 'w') as f:
##    voc = all_vocab.get_stoi()
##    json.dump(voc, f, indent=2)

def len_vocab(file_path, key):
    spc = ["<s>", "</s>", "<blank>", "<unk>"]
    all_vocab = build_vocab_from_iterator(yield_tokens(file_path, key),
                                      specials=spc)       
        
    all_vocab.set_default_index(all_vocab["<unk>"])
        
    return len(all_vocab)


train_src_len = len_vocab(train_set, 'tweet')
train_tgt_len = len_vocab(train_set, 'image')

valid_src_len = len_vocab(valid_set, 'tweet')
valid_tgt_len = len_vocab(valid_set, 'image')


def collate_batch(batch, tokenizer, vocab, max_padding=128, pad_id=3):
    sos_id = torch.tensor([0])
    eos_id = torch.tensor([1])
    src_list, tgt_list = [], []
    #print('in collate-batchsize: ', len(batch))
    for i, (_src, _tgt) in enumerate(batch):
##        print("in collate")
##        print(_src)
##        print(_tgt)
        proc_src = torch.cat([sos_id, torch.tensor(vocab(tokenizer(_src)),
                                                   dtype=torch.int64),
                              eos_id], 0,)
        #print(proc_src)
        proc_tgt = torch.cat([sos_id, torch.tensor(vocab(tokenizer(_tgt)),
                                                   dtype=torch.int64),
                              eos_id], 0,)
        #print(proc_tgt)
        src_list.append(pad(proc_src, (0, max_padding - len(proc_src)), value=pad_id))
        tgt_list.append(pad(proc_tgt, (0, max_padding - len(proc_tgt)), value=pad_id))

        src = torch.stack(src_list)
        tgt = torch.stack(tgt_list)
        #print(i)
        return (src, tgt)


def get_max_padding(file_path):
    len_list = []
    src_len = 0
    tgt_len = 0
    with open(file_path, encoding='utf-8') as f:
        data = json.load(f)
        ctx = [ct['tweet'].split(' ') for ct in data]
        ctx_list = []
        for ct in ctx:
            ctx_list.append(len(ct))
        src_len = max(ctx_list)
        
        resp = [res['image'].split(' ') for res in data]
        res_list = []
        for res in resp:
            res_list.append(len(res))
        tgt_len = max(res_list)
        len_list = ctx_list + res_list
    return max(len_list), src_len, tgt_len


#max_pad, train_src_len, train_tgt_len = get_max_padding(all_data)
max_pad, len1, len2 = get_max_padding(all_data)
print('t src: ', train_src_len)
print('t tgt: ', train_tgt_len)


##def build_vocab(spacy_e):
##    spc = ["<s>", "</s>", "<blank>", "<unk>"]
##    def tokenize_en(text):
##        return tokenize(text,)     
##       
##    vocab_src = build_vocab_from_iterator(
##        yield_tokens(),
##        min_freq = 2,
##        specials = spc,)   
##    
##    vocab_src.set_default_index(vocab_src["<unk>"])
##    vocab_tgt.set_default_index(vocab_tgt["<unk>"])
##    return vocab_src, vocab_tgt
##

def collate_fn(batch):
    return collate_batch(batch, tokenizer, all_vocab,
                         max_padding=max_pad)


def get_train_dataloader():
    train = DataLoader(train_iter, batch_size=10, collate_fn=collate_fn,
                       shuffle=True)    
    return train


def get_valid_dataloader():
    valid = DataLoader(valid_iter, batch_size=10, collate_fn=collate_fn,
                       shuffle=True)
    return valid

