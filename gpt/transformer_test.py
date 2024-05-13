import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.functional import pad
import math, copy, time
from torch.autograd import Variable
import matplotlib.pyplot as plt
import seaborn
import sys
from clrprint import *
import torchtext.datasets as datasets
from torchtext.vocab import build_vocab_from_iterator
from torchtext import data
from torchtext.data.functional import to_map_style_dataset
import spacy
from torch.utils.data import DataLoader
from torch.utils.data.distributed import DistributedSampler
import torch.distributed as dist
import os



try:
    #spacy_de = spacy.load('de_core_news_sm')
    spacy_en = spacy.load('en_core_web_sm')
except IOError:
    #os.system("python -m spacy download de_core_news_sm")
    #spacy_de = spacy.load('de_core_news_sm')
    os.system("python -m spacy download en_core_web_sm")
    spacy_en = spacy.load('en_core_web_sm')

##os.system("python -m spacy download de_core_news_sm")
##spacy_de = spacy.load('de_core_news_sm')
##os.system("python -m spacy download en_core_web_sm")
##spacy_en = spacy.load('en_core_web_sm')
    
seaborn.set_context(context="talk")


print("Dependencies imported")

class mLogging:
    activeP = True
    activeR = True
    activeS = True
    activeE = True
    
    def __init__(self):
        print("Logging...")

    def p(self, msg):
        if self.activeP:
            clrprint(msg, clr='green')
            
    def r(self, msg):
        if self.activeR:
            clrprint(msg, clr='purple')
        
    def s(self, msg):
        if self.activeS:
            clrprint(msg, clr='blue')

    def e(self, msg):
        if self.activeE:
            clrprint(msg, clr='yellow')

    def activateP(self, val=True):
        self.activeP = val

    def activateR(self, val=True):
        self.activeR = val

    def activateS(self, val=True):
        self.activeS = val

    def activateE(self, val=True):
        self.activeE = val

log = mLogging()
log.activateP(False)
log.activateR(False)
log.activateS(False)
log.activateE(True)

class EncoderDecoder(nn.Module):
    def __init__(self, encoder, decoder, src_embed, tgt_embed, generator):
        super(EncoderDecoder, self).__init__()
        log.p("EncoderDecoder init")
        self.encoder = encoder
        self.decoder = decoder
        self.src_embed = src_embed
        self.tgt_embed = tgt_embed
        self.generator = generator
        

    def forward(self, src, tgt, src_mask, tgt_mask):
        log.p("EncoderDecoder fwd")
        return self.decode(self.encode(src, src_mask), src_mask, tgt, tgt_mask)

    def encode(self, src, src_mask):
        log.p("EncoderDecoder encode")
        return self.encoder(self.src_embed(src), src_mask)

    def decode(self, memory, src_mask, tgt, tgt_mask):
        log.p("EncoderDecoder decode")
        return self.decoder(self.tgt_embed(tgt), memory, src_mask, tgt_mask)

class Generator(nn.Module):
    def __init__(self, d_model, vocab):
        log.p("Generator init")
        super(Generator, self).__init__()        
        self.proj = nn.Linear(d_model, vocab)
        

    def forward(self, x):
        log.p("Generator fwd")
        return F.log_softmax(self.proj(x), dim=-1)

def clones(module, N):
    log.p("clones")
    return nn.ModuleList([copy.deepcopy(module) for _ in range(N)])

class Encoder(nn.Module):
    def __init__(self, layer, N):
        log.p("Encoder init")
        super(Encoder, self).__init__()
        self.layers = clones(layer, N)
        self.norm = LayerNorm(layer.size)
        

    def forward(self, x, mask):
        log.p("Encoder fwd")
        for layer in self.layers:
            x = layer(x, mask)

        log.r("encoder loop end")
        log.s(self.norm(x))
        return self.norm(x)

class LayerNorm(nn.Module):
    def __init__(self, features, eps=1e-6):
        log.p("LayerNorm init")
        super(LayerNorm, self).__init__()
        self.a_2 = nn.Parameter(torch.ones(features))
        self.b_2 = nn.Parameter(torch.zeros(features))
        self.eps = eps
        

    def forward(self, x):
        log.p("LayerNorm fwd")
        mean = x.mean(-1, keepdim=True)
        std = x.std(-1, keepdim=True)        
        return self.a_2 * (x - mean) / (std + self.eps) + self.b_2


class SublayerConnection(nn.Module):
    def __init__(self, size, dropout):
        log.p("SublayerConn init")
        super(SublayerConnection, self).__init__()
        self.norm = LayerNorm(size)
        self.dropout = nn.Dropout(dropout)
        

    def forward(self, x, sublayer):
        log.p("SublayerConn fwd")
        log.r(sublayer)
        log.s(x)
        return x + self.dropout(sublayer(self.norm(x)))
    


class EncoderLayer(nn.Module):
    def __init__(self, size, self_attn, feed_fwd, dropout):
        log.p("EncoderLayer init")
        super(EncoderLayer, self).__init__()
        self.self_attn = self_attn
        self.feed_fwd = feed_fwd
        self.sublayer = clones(SublayerConnection(size, dropout), 2)
        self.size = size
        

    def forward(self, x, mask):
        log.p("EncoderLayer fwd")
        x = self.sublayer[0](x, lambda x: self.self_attn(x, x, x, mask))        
        return self.sublayer[1](x, self.feed_fwd)

class Decoder(nn.Module):
    def __init__(self, layer, N):
        log.p("Decoder init")
        super(Decoder, self).__init__()
        self.layers = clones(layer, N)
        self.norm = LayerNorm(layer.size)
        

    def forward(self, x, memory, src_mask, tgt_mask):
        log.p("Decoder fwd")
        for layer in self.layers:
            x = layer(x, memory, src_mask, tgt_mask)

        log.r("decoder loop end")
        log.s(x)
        return self.norm(x)

class DecoderLayer(nn.Module):
    def __init__(self, size, self_attn, src_attn, feed_fwd, dropout):
        log.p("DecoderLayer init")
        super(DecoderLayer, self).__init__()
        self.size = size
        self.self_attn = self_attn
        self.src_attn = src_attn
        self.feed_fwd = feed_fwd
        self.sublayer = clones(SublayerConnection(size, dropout), 3)
        

    def forward(self, x, memory, src_mask, tgt_mask):
        log.p("DecoderLayer fwd")
        m = memory
        log.s(tgt_mask)
        log.s(src_mask)
        log.s(m)
        x = self.sublayer[0](x, lambda x: self.self_attn(x, x, x, tgt_mask))
        x = self.sublayer[1](x, lambda x: self.src_attn(x, m, m, src_mask))
        return self.sublayer[2](x, self.feed_fwd)

def subsequent_mask(size):
    log.p("subsequent mask")
    attn_shape = (1, size, size)
    subsequent_mask = np.triu(np.ones(attn_shape), k=1).astype('uint8')
    
    return torch.from_numpy(subsequent_mask) == 0
        
##plt.figure(figsize=(5,5))
##plt.imshow(subsequent_mask(20)[0])
##plt.show()


def attention(query, key, value, mask=None, dropout=None):
    log.p("attention")
    d_k = query.size(-1)
    scores = torch.matmul(query, key.transpose(-2, -1)) / math.sqrt(d_k)
    log.p("attention scores before mask")
    log.s(scores)
    if mask is not None:
        scores = scores.masked_fill(mask == 0, -1e9)
    log.p("attention scores after mask")
    log.s(scores)
    p_attn = F.softmax(scores, dim = -1)
    if dropout is not None:
        p_attn = dropout(p_attn)
    
    return torch.matmul(p_attn, value), p_attn


class MultiHeadedAttention(nn.Module):
    def __init__(self, h, d_model, dropout=0.1):
        log.p("MultiHeadAttn init")
        super(MultiHeadedAttention, self).__init__()
        assert d_model % h == 0
        self.d_k = d_model // h
        self.h = h
        self.linears = clones(nn.Linear(d_model, d_model), 4)
        self.attn = None
        self.dropout = nn.Dropout(p=dropout)
        

    def forward(self, query, key, value, mask=None):
        log.p("MultiHeadAttn fwd")
        if mask is not None:
            mask = mask.unsqueeze(1)
        nbatches = query.size(0)
        #for i in self.linears:
            #print(i)
            #print(i.weight)
        query, key, value = [l(x).view(nbatches, -1, self.h, self.d_k).transpose(1, 2) for l, x in zip(self.linears, (query, key, value))]
        log.r(self.h)
        log.r(self.d_k)
        log.s(query)
        log.s(key)
        log.s(value)
        x, self.attn = attention(query, key, value, mask=mask, dropout=self.dropout)
        log.s(x)
        log.s(self.attn)
        x = x.transpose(1, 2).contiguous().view(nbatches, -1, self.h * self.d_k)       
        return self.linears[-1](x)

class PositionwiseFeedForward(nn.Module):
    def __init__(self, d_model, d_ff, dropout=0.1):
        log.p("FeedFwd init")
        super(PositionwiseFeedForward, self).__init__()
        self.w_1 = nn.Linear(d_model, d_ff)
        self.w_2 = nn.Linear(d_ff, d_model)
        self.dropout = nn.Dropout(dropout)
        

    def forward(self, x):
        log.p("FeedFwd fwd")
        return self.w_2(self.dropout(F.relu(self.w_1(x))))


class Embeddings(nn.Module):
    def __init__(self, d_model, vocab):
        log.p("Embeddings init")
        super(Embeddings, self).__init__()
        self.lut = nn.Embedding(vocab, d_model)
        self.d_model = d_model
        

    def forward(self, x):        
        log.p("Embeddings fwd")
        emb_ret = self.lut(x) * math.sqrt(self.d_model)
        return emb_ret

    
class PositionalEncoding(nn.Module):
    def __init__(self, d_model, dropout, max_len=5000):
        log.p("PosEncoding init")
        super(PositionalEncoding, self).__init__()
        self.dropout = nn.Dropout(p=dropout)
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2) * -(math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0)
        self.register_buffer('pe', pe)
        

    def forward(self, x):
        log.p("PosEncoding fwd")
        x = x + Variable(self.pe[:, :x.size(1)], requires_grad=False)        
        return self.dropout(x)

  
##plt.figure(figsize=(15, 5))
##pe = PositionalEncoding(20, 0)
##y = pe.forward(Variable(torch.zeros(1, 100, 20)))
##plt.plot(np.arange(100), y[0, :, 4:8].data.numpy())
##plt.legend(["dim %d"%p for p in [4,5,6,7]])
##plt.show()

def make_model(src_vocab, tgt_vocab, N=6, d_model=512, d_ff=2048, h=8, dropout=0.1):
    log.p("make_model")
    c = copy.deepcopy
    attn = MultiHeadedAttention(h, d_model)
    ff = PositionwiseFeedForward(d_model, d_ff, dropout)
    position = PositionalEncoding(d_model, dropout)
    model = EncoderDecoder(
        Encoder(EncoderLayer(d_model, c(attn), c(ff), dropout), N),
        Decoder(DecoderLayer(d_model, c(attn), c(attn), c(ff), dropout), N),
        nn.Sequential(Embeddings(d_model, src_vocab), c(position)),
        nn.Sequential(Embeddings(d_model, tgt_vocab), c(position)),
        Generator(d_model, tgt_vocab))

    for p in model.parameters():
        if p.dim() > 1:
            nn.init.xavier_uniform(p)
    
    return model

##tmp_model = make_model(10, 10, 2)

class Batch:
    def __init__(self, src, tgt=None, pad=0):
        log.p("Batch init")
        self.src = src
##        log.e(src)
##        log.e(tgt)
        self.src_mask = (src != pad).unsqueeze(-2)
        if tgt is not None:
            self.tgt = tgt[:, :-1]
            self.tgt_y = tgt[:, 1:]
            self.tgt_mask = self.make_std_mask(self.tgt, pad)
            self.ntokens = (self.tgt_y != pad).data.sum()
        

    @staticmethod
    def make_std_mask(tgt, pad):
        log.p("Batch make_std_mask")
        tgt_mask = (tgt != pad).unsqueeze(-2)
        tgt_mask = tgt_mask & Variable(subsequent_mask(tgt.size(-1)).type_as(tgt_mask.data))        
        return tgt_mask


def run_epoch(data_iter, model, loss_compute, log_post="training"):
    log.r("run_epoch entry")
    log.r("\n\n----------" + log_post + "------------\n\n")
    start = time.time()
    total_tokens = 0
    total_loss = 0
    tokens = 0
    
    log.r("before looping")
    for i, batch in enumerate(data_iter):
        log.r("in run_epoch loop")
        log.s(batch.src)
        log.s(batch.tgt)
        out = model.forward(batch.src, batch.tgt, batch.src_mask, batch.tgt_mask)
        loss = loss_compute(out, batch.tgt_y, batch.ntokens)
        total_loss += loss
        total_tokens += batch.ntokens
        tokens += batch.ntokens
        if i % 50 == 1:
            elapsed = time.time() - start
            print("Epoch Step: %d Loss: %f Tokens per Sec: %f" % (i, loss / batch.ntokens, tokens / elapsed))
            start = time.time()
            tokens = 0
    log.r("run_epoch end")
    return total_loss / total_tokens
                         
global max_src_in_batch, max_tgt_in_batch

def batch_size_fn(new, count, sofar):
    log.p("batch_size_fn")
    global max_src_in_batch, max_tgt_in_batch
    if count == 1:
        max_src_in_batch = 0
        max_tgt_in_batch = 0
    max_src_in_batch = max(max_src_in_batch, len(new.src))
    max_tgt_in_batch = max(max_tgt_in_batch, len(new.trg) + 2)
    src_elements = count * max_src_in_batch
    tgt_elements = count * max_tgt_in_batch
    
    return max(src_elements, tgt_elements)

class NoamOpt:
    def __init__(self, model_size, factor, warmup, optimizer):
        log.p("NoamOpt init")
        self.optimizer = optimizer
        self._step = 0
        self.warmup = warmup
        self.factor = factor
        self.model_size = model_size
        self._rate = 0
        

    def step(self):
        log.p("NoamOpt step")
        self._step += 1
        rate = self.rate()
        for p in self.optimizer.param_groups:
            p['lr'] = rate
        self._rate = rate
        self.optimizer.step()
        


    def rate(self, step=None):
        log.p("NoamOpt rate")
        if step is None:
            step = self._step
        
        return self.factor * (self.model_size ** (-0.5) * min(step**(-0.5), step * self.warmup**(-1.5)))

def get_std_opt(model):
    log.p("get_std_opt")
    return NoamOpt(model.src_embed[0].d_model, 2, 4000, torch.optim.Adam(model.parameters(), lr=0, betas=(0.9, 0.98), eps=1e-9))


class LabelSmoothing(nn.Module):
    def __init__(self, size, padding_idx, smoothing=0.0):
        log.p("LabeSmoothing init")
        super(LabelSmoothing, self).__init__()
        self.criterion = nn.KLDivLoss(size_average=False)
        self.padding_idx = padding_idx
        self.confidence = 1.0 - smoothing
        self.smoothing = smoothing
        self.size = size
        self.true_dist = None
        

    def forward(self, x, target):
        log.p("LabelSmoothing forward")
        assert x.size(1) == self.size
        true_dist = x.data.clone()
        true_dist.fill_(self.smoothing / (self.size - 2))
        true_dist.scatter_(1, target.data.unsqueeze(1), self.confidence)
        true_dist[:, self.padding_idx] = 0
        mask = torch.nonzero(target.data == self.padding_idx)
        if mask.dim() > 0:
            true_dist.index_fill_(0, mask.squeeze(), 0.0)
        self.true_dist = true_dist
        
        return self.criterion(x, Variable(true_dist, requires_grad=False))
        
    
def data_gen(V, batch, nbatches):
    log.p("data_gen")
    for i in range(nbatches):
        log.r("data gen itr = " + str(i))
        data = torch.from_numpy(np.random.randint(1, V, size=(batch, 5), dtype="int64"))
        data[:, 0] = 1
        src = Variable(data, requires_grad=False)
        tgt = Variable(data, requires_grad=False)
        yield Batch(src, tgt, 0)

class SimpleLossCompute:
    def __init__(self, generator, criterion, opt=None):
        log.p("SimpleLoss init")
        self.generator = generator
        self.criterion = criterion
        self.opt = opt
        

    def __call__(self, x, y, norm):
        log.p("SimpleLoss call")        
        x = self.generator(x)
        log.r(norm)
        loss = self.criterion(x.contiguous().view(-1, x.size(-1)), y.contiguous().view(-1)) / norm
        log.r(loss)
        loss.backward()
        if self.opt is not None:
            self.opt.step()
            self.opt.optimizer.zero_grad()
        log.r(loss.data)
        return loss.item() * norm
        

V = 6
criterion = LabelSmoothing(size=V, padding_idx=0, smoothing=0.0)
model_test = make_model(V, V, N=2, d_model=2, d_ff=8, h=2)
model_opt_test = NoamOpt(model_test.src_embed[0].d_model, 1, 400, torch.optim.Adam(model_test.parameters(), lr=0, betas=(0.9, 0.98), eps=1e-9))

##for epoch in range(1):
##    log.p("\n\n-------------------------------------------------------START------------------------------------------------------------------------------------------------------------------------------------------------\n\n")
##    model_test.train()
##    run_epoch(data_gen(V, 5, 5), model_test, SimpleLossCompute(model_test.generator, criterion, model_opt_test))
##    model_test.eval()
##    evalVal = run_epoch(data_gen(V, 5, 1), model_test, SimpleLossCompute(model_test.generator, criterion, None), log_post="eval")
##    print("eval Ot = ", evalVal)
##    log.r("transformer loop end")

def greedy_decode(model, src, src_mask, max_len, start_symbol):
    memory = model.encode(src, src_mask)
    #log.e(memory)
    ys = torch.ones(1, 1).fill_(start_symbol).type_as(src.data)
    log.e(ys)
    for i in range(max_len - 1):
        out = model.decode(memory, src_mask, Variable(ys), Variable(subsequent_mask(ys.size(1)).type_as(src.data)))
        #log.e(out)
        prob = model.generator(out[:, -1])
        _, next_word = torch.max(prob, dim=1)
        next_word = next_word.data[0]
        ys = torch.cat([ys, torch.ones(1, 1).type_as(src.data).fill_(next_word)], dim=1)
    return ys

##model_test.eval()
##src = Variable(torch.LongTensor([[1,3,3,2,5]]))
##src_mask = Variable(torch.ones(1,1,5))
##print(src_mask)
##ot = greedy_decode(model_test, src, src_mask, max_len=10, start_symbol=1)
##print(ot)

##LOADING DATA FOR FULL TRAINING



def yield_tokens(data_iter, tokenizer, index):
    for from_to_tuple in data_iter:
        yield tokenizer(from_to_tuple[index])

def tokenize(text, tokenizer):
    return [tok.text for tok in tokenizer.tokenizer(text)]

def build_vocab(spacy_d, spacy_e):
    spc = ["<s>", "</s>", "<blank>", "<unk>"]
    def tokenize_en(text):
        return tokenize(text, spacy_e)

    def tokenize_de(text):
        return tokenize(text, spacy_d)
    
    print("Building German Vocab...")
    train, val, test = datasets.Multi30k(language_pair=("de", "en"))
    vocab_src = build_vocab_from_iterator(
        yield_tokens(train + val + test, tokenize_de, index=0),
        min_freq = 2,
        specials = spc,)

    print("Building English Vocab...")
    train, val, test = datasets.Multi30k(language_pair=("de", "en"))
    vocab_tgt = build_vocab_from_iterator(
        yield_tokens(train + val + test, tokenize_en, index=1),
        min_freq=2,
        specials=spc,)
    
    vocab_src.set_default_index(vocab_src["<unk>"])
    vocab_tgt.set_default_index(vocab_tgt["<unk>"])
    return vocab_src, vocab_tgt

def load_vocab(spacy_d, spacy_e):
    if not os.path.exists("vocab.pt"):
        vocab_src, vocab_tgt = build_vocab(spacy_d, spacy_e)
        torch.save((vocab_src, vocab_tgt), "vocab.pt")
    else:
        vocab_src, vocab_tgt = torch.load("vocab.pt")
    print("Finished. \nVocab Size: ")
    print(len(vocab_src))
    print(len(vocab_tgt))
    return vocab_src, vocab_tgt

##src_pipeline, tgt_pipeline = load_vocab(spacy_de, spacy_en)


def collate_batch(batch, src_pipeline, tgt_pipeline, src_vocab, tgt_vocab, device=None,
                  max_padding=128, pad_id=2,):
    bs_id = torch.tensor([0], device=device)
    eos_id = torch.tensor([1], device=device)
    src_list, tgt_list = [], []
    for (_src, _tgt) in batch:
        print(_src)
        print(_tgt)
        processed_src = torch.cat([bs_id, torch.tensor(src_vocab(src_pipeline(_src)),
                                                       dtype=torch.int64,
                                                       device=device,),
                                   eos_id,
                                   ],
                                  0,)
        processed_tgt = torch.cat([bs_id, torch.tensor(tgt_vocab(tgt_pipeline(_tgt)),
                                                        dtype=torch.int64,
                                                        device=device),
                                    eos_id,],
                                  0,)
        src_list.append(pad(processed_src, (0,
                                            max_padding - len(processed_src),
                                            ),
                            value=pad_id,)
                        )

        tgt_list.append(
            pad(processed_tgt,
                (0, max_padding - len(processed_tgt)),
                value=pad_id,))
        src = torch.stack(src_list)
        tgt = torch.stack(tgt_list)
        print(src)
        return (src, tgt)

def create_dataloaders(
    vocab_src, vocab_tgt, spacy_d, spacy_e, batch_size=12000,
    max_padding=128, device=None, is_distributed=False,):
    def tokenize_en(text):
        return tokenize(text, spacy_e)

    def tokenize_de(text):
        return tokenize(text, spacy_d)

    def collate_fn(batch):
        return collate_batch(batch, tokenize_de, tokenize_en, vocab_src, vocab_tgt,
                             device, max_padding=max_padding,
                             pad_id=vocab_src.get_stoi()["<blank>"],)

    train_iter, valid_iter, test_iter = datasets.Multi30k(language_pair=("de", "en"))
    #above creates a map of translation - for each sentence tuple (de sent, en sent)
    train_iter_map = to_map_style_dataset(train_iter)
    train_sampler = (DistributedSampler(train_iter_map) if is_distributed else None)
    valid_iter_map = to_map_style_dataset(valid_iter)
    valid_sampler = (DistributedSampler(valid_iter_map) if is_distributed else None)
    train_dataloader = DataLoader(train_iter_map,
                                  batch_size=batch_size,
                                  shuffle=(train_sampler is None),
                                  sampler=train_sampler,
                                  collate_fn=collate_fn,)
    valid_dataloader = DataLoader(valid_iter_map,
                                  batch_size=batch_size,
                                  shuffle=(valid_sampler is None),
                                  sampler=valid_sampler,
                                  collate_fn=collate_fn,)
    #returns an iterable - the text is converted to vectors using collate_fn
    return train_dataloader, valid_dataloader

##train, valid = create_dataloaders(src_pipeline, tgt_pipeline, spacy_de, spacy_en)
##print("train size: " + str(train.__len__()))
##for i, batch in enumerate(train):
##    print(batch.shape)
train1 = iter_check.get_train_dataloader()
print("train1 size: " + str(train1.__len__()))
src_pipeline = iter_check.src_vocab
tgt_pipeline = iter_check.tgt_vocab
#print("valid size: " + str(valid.__len__()))
pad_idx = src_pipeline["<blank>"]
criterion = LabelSmoothing(size=len(tgt_pipeline), padding_idx=pad_idx, smoothing=0.1)
model = make_model(len(src_pipeline), len(tgt_pipeline), N=6)
model_opt = NoamOpt(model.src_embed[0].d_model, 1, 400, torch.optim.Adam(model.parameters(), lr=0, betas=(0.9, 0.98), eps=1e-9))
model_path = "eng_sindhi_model.pt"
model_load = False
epoch = 0

for ep in range(500):
    log.p("\n\n-------------------------------------------------------START------------------------------------------------------------------------------------------------------------------------------------------------\n\n")
    if model_load == False:
        if os.path.exists(model_path):
            print("path exists")
            chkpt = torch.load(model_path)
            model.load_state_dict(chkpt['model_state_dict'])
            model_opt.optimizer.load_state_dict(chkpt['optimizer_state_dict'])
            epoch = chkpt['epoch']
            loss = chkpt['loss']
            model_load = True
    model.train()
    
    loss = run_epoch((Batch(b[0], b[1], pad_idx) for b in train1), model, SimpleLossCompute(model.generator, criterion, model_opt))
    log.e(("Loss = %s, EPOCH = %s") % (str(loss), str(epoch)))
    if (epoch % 100 == 0):
        torch.save({
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': model_opt.optimizer.state_dict(),
            'loss': loss
            }, "eng_sindhi_model.pt")
    epoch += 1
        
        


torch.save({
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': model_opt.optimizer.state_dict(),
            'loss': loss
            }, model_path)


##valid = iter_check.get_valid_dataloader()
##
##v_batch = (Batch(b[0], b[1], pad_idx) for b in valid)
##
##print(v_batch)
##
##for i in v_batch:
##    print("\n---greedy decoding---\n")
##    src = i.src
##    print("src: ", src)
##    src_mask = (src != src_pipeline.get_stoi()["<unk>"]).unsqueeze(-2)
##    print("src_mask: ", src_mask)
##    out = greedy_decode(model, src, src_mask, max_len=60,
##                        start_symbol=tgt_pipeline.get_stoi()["<s>"])
##    print("out: ", out)
##    print("\nprediction: ")
##    for k in range(1, out.size(1)):
##        sym = tgt_pipeline.get_itos()[out[0, k]]
##        if sym == "</s>": break
##        print(sym, end = " ")
##    print("\nactual: ")
##    for j in range(1, i.tgt.size(1)):
##        sym = tgt_pipeline.get_itos()[i.tgt[0, j]]
##        if sym == "</s>": break
##        print(sym, end = " ")
##    print()
##    break



##    out = greedy_decode(model, src, src_mask, max_len=60,
##                        start_symbol=src_pipline.get_stoi()["<s>"])
##    print("Translation = ", end="\t")
##    for i in range(1, out.size(1)):
##        sym = tgt_pipeline.itos()[out[0, i]]
##        if sym == "</s>": break
##        print(sym, end=" ")
##    print()
##    print("Target = ", end="\t")
##    break

##
##model.load_state_dict(torch.load("m_state_dict.pt"))
##def check_outputs(dataloader, model, vocab_src, vocab_tgt, n_examples=3, pad_idx=2,
##                  eos_string="</s>"):
##
##    results = [()] * n_examples
##    for idx in range(n_examples):
##        print("\nExamples %d =====\n" % idx)
##        b = next(iter(dataloader))
##        print("loader")
##        rb = Batch(b[0], b[1], pad_idx)
##        print("batching")
##        greedy_decode(model, rb.src, rb.src_mask, 64, 0)[0]
##        print("g_decode")
##        src_tokens = [vocab_src.get_itos()[x] for x in rb.src[0] if x != pad_idx]
##        print("gen src token")
##        print(src_tokens[:10])
##        tgt_tokens = [vocab_tgt.get_itos()[x] for x in rb.tgt[0] if x != pad_idx]
##        
##
##        log.e("Input: " + " ".join(src_tokens).replace("\n", ""))
##        log.e("Target Output: " + " ".join(tgt_tokens).replace("\n", ""))
##
##        model_out = greedy_decode(model, rb.src, rb.src_mask, 72, 0)[0]
##        model_txt = (" ".join([vocab_tgt.get_itos()[x] for x in model_out if x != pad_idx])
##                     .split(eos_string, 1)[0] + eos_string)
##        log.e("Model Output: " + model_txt.replace("\n", ""))
##        results[idx] = (rb, src_tokens, tgt_tokens, model_out, model_txt)
##    return results
##
##check_outputs(valid, model, src_pipeline, tgt_pipeline)
##        
####model.load_state_dict(torch.load("m_state_dict.pt"))
####    model.eval()
####    evalVal = run_epoch(data_gen(V, 5, 1), model, SimpleLossCompute(model.generator, criterion, None), log_post="eval")
####    print("eval Ot = ", evalVal)
####    log.r("transformer loop end")
##
##
##    
##    
##                                                    
####BOS_WORD = '<s>'
####EOS_WORD = '</s>'
####BLANK_WORD = "<blank>"
####SRC = data.Field(tokenize=tokenize_de, pad_token=BLANK_WORD)
####TGT = data.Field(tokenize=tokenize_en, init_token=BOS_WORD, eos_token=EOS_WORD, pad_token=BLANK_WORD)
####
####MAX_LEN = 100
####train, val, test = datasets.IWSLT.splits(exts=('.de', '.en'), fields=(SRC, TGT),
####                                         filter_pred=lambda x: len(vars(x)['src']) <= MAX_LEN and
####                                         len(vars(x)['trg']) <= MAX_LEN)
####MIN_FREQ = 2
####SRC.build_vocab(train.src, min_freq=MIN_FREQ)
####TGT.build_vocab(train.trg, min_freq=MIN_FREQ)
####print(len(SRC.vocab))
##
####class mIterator(data.Iterator):
####    def create_batches(self):
####        if self.train:
####            def pool(d, random_shuffler):
####                for p in data.batch(d, self.batch_size * 100):
####                    p_batch = data.batch(sorted(p, key=self.sort_key),
####                                         self.batch_size, self.batch_size_fn)
####                    for b in random_shuffler(list(p_batch)):
####                        yield b
####            self.batches = pool(self.data(), self.random_shuffler)
####        else:
####            self.batches = []
####            for b in data.batch(self.data(), self.batch_size, self.batch_size_fn):
####                self.batches.append(sorted(b, key=self.sort_key))
####
####
####    def rebatch(pad_idx, batch):
####        src, trg = batch.src.transpose(0, 1), batch.trg.transpose(0, 1)
####        return Batch(src, trg, pad_idx)
##
##
