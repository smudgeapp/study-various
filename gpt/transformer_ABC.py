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
import traceback
import tweet_img
import type_tweet



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

class GPTEncoder(nn.Module):
    def __init__(self, encoder, src_embed, generator):
        super(GPTEncoder, self).__init__()
        self.encoder = encoder
        self.src_embed = src_embed
        self.generator = generator

    def forward(self, src, src_mask):
        return self.encode(src, src_mask)
    

    def encode(self, src, src_mask):
        log.p("GPTEncoder encode")
        return self.encoder(self.src_embed(src), src_mask)
        

    

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
        #traceback.print_stack()
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
        log.r("at multihead attention forward after attention going to linears")
        log.s(x)
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

def make_gpt_model(src_vocab, tgt_vocab, N=6,
                   d_model=512, d_ff=2048, h=8, dropout=0.1):
    c = copy.deepcopy
    attn = MultiHeadedAttention(h, d_model)
    ff = PositionwiseFeedForward(d_model, d_ff, dropout)
    position = PositionalEncoding(d_model, dropout)
    model = GPTEncoder(Encoder(EncoderLayer(d_model, c(attn), c(ff), dropout), N),
                       nn.Sequential(Embeddings(d_model, src_vocab), c(position)),
                       Generator(d_model, tgt_vocab))

    for p in model.parameters():
        if p.dim() > 1:
            nn.init.xavier_uniform(p)

    return model


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


def run_gpt_epoch(data_iter, model, loss_compute, epoch, log_post="gpt_training"):
    start = time.time()
    total_tokens = 0
    total_loss = 0
    tokens = 0

    for i, batch in enumerate(data_iter):
        out = model.forward(batch.src, batch.src_mask)
        loss = loss_compute(out, batch.tgt_y, batch.ntokens)
        total_loss += loss
        total_tokens += batch.ntokens
        tokens += batch.ntokens
        if i % 50 == 1:
            elapsed = time.time() - start
            print("Epoch Step: %d Loss: %f Tokens per Sec: %f" % (i, loss / batch.ntokens, tokens / elapsed))
            start = time.time()
            tokens = 0
            print("training epoch: ", epoch)
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


def gpt_greedy_decode(model, src, src_mask, max_len, start_symbol):
    ys = torch.ones(1, 1).fill_(start_symbol).type_as(src.data)
    
    #for i in range(max_len - 1):
    memory = model.encode(src, src_mask)
    print(memory)
    print(memory[:, -1])
    
    log.e(ys)
    prob = model.generator(memory[:, -1])
    print(prob)
    #_, next_word = torch.max(prob, dim=1)
    _, words = torch.topk(prob, k=max_len)
    #print("torch topk: ", torch.topk(prob, k=max_len, dim=1))
    print(words)
    #print(next_word)
    #next_word = next_word.data[0]
    #print("next word data")
    #print(next_word)
    
    #ys = torch.cat([ys, torch.ones(1, 1).type_as(src.data).fill_(words)], dim=1)
    return words



##LOADING DATA FOR FULL TRAINING


def training_run(data_loader, model_path):
    train_gpt = data_loader.get_train_dataloader()
    all_vocab = data_loader.all_vocab

    pad_idx = all_vocab["<blank>"]

    criterion = LabelSmoothing(size=len(all_vocab),
                               padding_idx=pad_idx, smoothing=0.1)
    gpt_model_d = make_model(len(all_vocab),
                               len(all_vocab), N=6)
    gpt_modeld_opt = NoamOpt(gpt_model_d.src_embed[0].d_model, 1, 400,
                        torch.optim.Adam(gpt_model_d.parameters(), lr=0,
                                         betas=(0.9, 0.98), eps=1e-9))
    
    model_load = False
    epoch = 0
    start_time = time.time()

    for ep in range(3000):
        log.p("\n\n-------------------------------------------------------START------------------------------------------------------------------------------------------------------------------------------------------------\n\n")
        if model_load == False:
            if os.path.exists(model_path):
                print("path exists")
                chkpt = torch.load(model_path)
                gpt_model_d.load_state_dict(chkpt['model_state_dict'])
                gpt_modeld_opt.optimizer.load_state_dict(chkpt['optimizer_state_dict'])
                epoch = chkpt['epoch']
                loss = chkpt['loss']
                model_load = True
                
        gpt_model_d.train()

        loss = run_epoch((Batch(b[0], b[1], pad_idx) for b in train_gpt),
                         gpt_model_d,
                         SimpleLossCompute(gpt_model_d.generator, criterion,
                                           gpt_modeld_opt))
##        gpt_model_d.eval()
##        print(run_epoch((Batch(b[0], b[1], pad_idx) for b in valid_gpt),
##                            gpt_model_d,
##                            SimpleLossCompute(gpt_model_d.generator, criterion,
##                                              gpt_modeld_opt)))
        
        if (epoch % 100 == 0):
            print('saving model: ', epoch)
            torch.save({
                'epoch': epoch,
                'model_state_dict': gpt_model_d.state_dict(),
                'optimizer_state_dict': gpt_modeld_opt.optimizer.state_dict(),
                'loss': loss
                }, model_path)
        epoch += 1
        elapsed = time.time() - start_time
        print("Elapsed time: ", round(elapsed, 2))
        

def prediction_run(data_loader, model_path, text):
    train_gpt = data_loader.get_train_dataloader()
    valid_gpt = data_loader.get_valid_dataloader()
    all_vocab = data_loader.all_vocab

    pad_idx = all_vocab["<blank>"]

    criterion = LabelSmoothing(size=len(all_vocab),
                               padding_idx=pad_idx, smoothing=0.1)
    gpt_model_d = make_model(len(all_vocab),
                               len(all_vocab), N=6)
    gpt_modeld_opt = NoamOpt(gpt_model_d.src_embed[0].d_model, 1, 400,
                        torch.optim.Adam(gpt_model_d.parameters(), lr=0,
                                         betas=(0.9, 0.98), eps=1e-9))
    
    if os.path.exists(model_path):
        print("path exists")
        chkpt = torch.load(model_path)
        gpt_model_d.load_state_dict(chkpt['model_state_dict'])
        gpt_modeld_opt.optimizer.load_state_dict(chkpt['optimizer_state_dict'])
        epoch = chkpt['epoch']
        loss = chkpt['loss']
        gpt_model_d.eval()
    text = text.lower()
    def tokenizer(text):
        return([tok for tok in text.split(' ')])    
    tens_arr = []

    for i in text.split():
        try:
            index = all_vocab.get_stoi()[i]
            tens_arr.append(index)
        except:
            continue
    
    src = torch.LongTensor(tens_arr)
    #src = torch.LongTensor([all_vocab.get_stoi()[x] for x in text.split()])
    src = Variable(src)

    sos_id = torch.tensor([0])
    eos_id = torch.tensor([1])
    mem_src = torch.cat([sos_id, torch.tensor(all_vocab(tokenizer(text)),
                                              dtype=torch.int64),
                         eos_id], 0,)
    #print(mem_src)
    max_padding = 512
    src_list = [pad(mem_src, (0, max_padding - len(mem_src)), value=pad_idx)]
    #print(src_list)
    memory = torch.stack(src_list)
    #print(memory)
    src_mask = (memory != all_vocab.get_stoi()["<blank>"]).unsqueeze(-2)
    chkpt = torch.load(model_path)

    gpt_model_d.eval()

    out = greedy_decode(gpt_model_d, memory, src_mask, max_len=100,
                            start_symbol=all_vocab.get_stoi()["<s>"])
    print("GPT output: ", end="\t")
    output = "<s>"
    print(out[0])
    for i in range(1, out.size(1)):
        print(out[0, i])
        sym = all_vocab.get_itos()[out[0, i]]
        if sym == "</s>": break
        output += sym + " "
    print(output)
 

##TWEET TO IMAGE MODEL RUNS

##training_run(tweet_img, "tweet_image_ABC.pt")

prediction_run(tweet_img, "tweet_image_ABC.pt",
               "Make a statement with ABC Garments. Our stylish designs speak volumes about your personality.")



##SPACY DATA MODEL RUNS

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
