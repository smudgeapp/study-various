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

src_file = 'english.txt'#'sindhi-english/new-eng-text.txt'
tgt_file = 'german.txt'#'sindhi-english/new-sindhi-text.txt'
##src_pdf_file = 'sindhi-english/2023-eng.pdf'
##tgt_pdf_file = 'sindhi-english/2023-sindhi.pdf'
##src_csv = 'sindhi-english/eng-csv.csv'
##tgt_csv = 'sindhi-english/sindhi-csv.csv'
src_train = 'eng_t.txt'#'sindhi-english/eng_t.txt'
src_valid = 'eng_v.txt'#'sindhi-english/eng_v.txt'
tgt_train = 'ger_t.txt'#'sindhi-english/sindhi_t.txt'
tgt_valid = 'ger_v.txt'#'sindhi-english/sindhi_v.txt'
src_vocab_text = 'eng_vocab.txt'#'sindhi-english/eng_vocab_text.txt'
tgt_vocab_text = 'ger_vocab.txt'#'sindhi-english/sindhi_vocab_text.txt'


text = 'مالى سال'
bin_data = text.encode('utf-8', errors='ignore')
print(bin_data)
d_lat = bin_data.decode('utf-8')
print(d_lat)


##WRITING TEXT WITH OWN SENTENCE EOL REGEX AND SPLIT TRAIN & VALID

##EOL_REGEX = b'\n'#b'(?<!Rs)\. (?![0-9]) *'
##REP_REGEX = b'\r\n|\n|\r'
##
##
##
##def readlines(fio, size):
##    buf = bytearray(size)
##    while True:
##        if fio.tell() >= size:
##            break               
##        fio.readinto(buf)            
##        for line in re.split(EOL_REGEX, buf):
##            print(line)
##            yield line
##            
####            line = re.sub(REP_REGEX, b'', line)
####            if len(line) > 100:
####                yield line
##
##src_size = os.path.getsize(src_file)
##print(src_size)
##tgt_size = os.path.getsize(tgt_file)
##print(tgt_size)
##
##with io.open(src_train, mode='w', encoding='utf-8', errors='ignore') as e_train, \
##     io.open(src_valid, mode='w', encoding='utf-8', errors='ignore') as e_valid, \
##     io.open(tgt_train, mode='w', encoding='utf-8', errors='ignore') as s_train, \
##     io.open(tgt_valid, mode='w', encoding='utf-8', errors='ignore') as s_valid, \
##     io.open(src_vocab_text, mode='w', encoding='utf-8', errors='ignore') as s_vocab, \
##     io.open(tgt_vocab_text, mode='w', encoding='utf-8', errors='ignore') as t_vocab, \
##     io.FileIO(src_file) as f, io.FileIO(tgt_file) as t:
##    for i, (s_line, t_line) in enumerate(zip(readlines(f, src_size), readlines(t, tgt_size))):
##        s_vocab.write(('%s') % (s_line.decode('utf-8')))
##        t_vocab.write(('%s') % (t_line.decode('utf-8')))
##        if i < 1:        
##            e_train.write(('%s\n') % (s_line.decode('utf-8')))
##            s_train.write(('%s\n') % (t_line.decode('utf-8')))
##        else:
##            e_valid.write(('%s\n') % (s_line.decode('utf-8')))
##            s_valid.write(('%s\n') % (t_line.decode('utf-8')))


##MAKE DATASET AND DATALOADER

train_iter = ''
valid_iter = ''


with io.open(src_train, encoding='utf-8', errors='ignore') as f, \
     io.open(tgt_train, encoding='utf-8', errors='ignore') as t:
    train_iter = to_map_style_dataset(zip(f, t))
    print("train_iter")
    print(len(train_iter))
    
#print(train_iter[10][0])
#print(train_iter[10][1])


with io.open(src_valid, encoding='utf-8', errors='ignore') as f, \
     io.open(tgt_valid, encoding='utf-8', errors='ignore') as t:
    valid_iter = to_map_style_dataset(zip(f, t))
    print("valid_iter")
    print(len(valid_iter))



##CREATE VOCAB FROM DATASET FEED


def tokenizer(text):
    return([tok for tok in text.split(' ')])

def yield_tokens(file_path):
    with io.open(file_path, encoding='utf-8') as f:
        for line in f:
            sent = line.strip().split()
            yield sent

def load_vocab(src_f, tgt_f):
    spc = ["<s>", "</s>", "<blank>", "<unk>"]
    if not os.path.exists('vocab.pt'):
        src_vocab = build_vocab_from_iterator(yield_tokens(src_vocab_text),
                                              specials=spc)
        tgt_vocab = build_vocab_from_iterator(yield_tokens(tgt_vocab_text),
                                              specials=spc)
        src_vocab.set_default_index(src_vocab["<unk>"])
        tgt_vocab.set_default_index(tgt_vocab["<unk>"])
        torch.save((src_vocab, tgt_vocab), 'vocab.pt')
    else:
        src_vocab, tgt_vocab = torch.load('vocab.pt')

    print(len(src_vocab))
    print(len(tgt_vocab))
    return src_vocab, tgt_vocab


src_vocab, tgt_vocab = load_vocab(src_file, tgt_file)

sent = 'The occasion though  fills us with pride'

def collate_batch(batch, tokenizer, s_vocab, t_vocab, max_padding=128, pad_id=3):
    sos_id = torch.tensor([0])
    eos_id = torch.tensor([1])
    src_list, tgt_list = [], []
    print('in collate-batchsize: ', len(batch))
    for i, (_src, _tgt) in enumerate(batch):
        print("in collate")
        print(_src)
        print(_tgt)
        proc_src = torch.cat([sos_id, torch.tensor(s_vocab(tokenizer(_src)),
                                                   dtype=torch.int64),
                              eos_id], 0,)
        print(proc_src)
        proc_tgt = torch.cat([sos_id, torch.tensor(t_vocab(tokenizer(_tgt)),
                                                   dtype=torch.int64),
                              eos_id], 0,)
        print(proc_tgt)
        src_list.append(pad(proc_src, (0, max_padding - len(proc_src)), value=pad_id))
        tgt_list.append(pad(proc_tgt, (0, max_padding - len(proc_tgt)), value=pad_id))

        src = torch.stack(src_list)
        tgt = torch.stack(tgt_list)
        print(i)
        return (src, tgt)

def get_max_padding(src_text, tgt_text):
    len_list = []
    with io.open(src_text, encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = [tok for tok in line.split(' ')]
            len_list.append(len(line))
    
    with io.open(tgt_text, encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = [tok for tok in line.split(' ')]
            len_list.append(len(line))
    return max(len_list)

max_pad = get_max_padding(src_train, tgt_train)

def collate_fn(batch):
    return collate_batch(batch, tokenizer, src_vocab, tgt_vocab,
                         max_padding=max_pad)


def get_train_dataloader():
    train = DataLoader(train_iter, batch_size=100, collate_fn=collate_fn,
                       shuffle=True)
    return train

def get_valid_dataloader():
    valid = DataLoader(valid_iter, batch_size=10, collate_fn=collate_fn,
                       shuffle=True, drop_last=False)
    return valid


##print("iter len: ", len(valid_iter))
##valid = get_valid_dataloader()
##v_iter = iter(valid)
##
##lim = 10
##i = 0


