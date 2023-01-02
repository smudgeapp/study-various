from gensim.models.callbacks import CallbackAny2Vec
from gensim.models import Word2Vec
import os


class w2vcallback(CallbackAny2Vec):

    def __init__(self, modelname=None):
        self.epoch = 0
        self.model_name = modelname

    def on_epoch_end(self, model):
        loss = model.get_latest_training_loss()
        log_entry = ""
        if self.epoch == 0:
            log_entry = 'Loss after epoch {}: Loss {}'.format(self.epoch, loss)
            print('Loss after epoch {}: Loss {}'.format(self.epoch, loss))
        else:
            log_entry = 'Loss after epoch {}: Loss {}: Change {}'.format(self.epoch, loss, \
                                                    loss - self.prev_loss)
            print('Loss after epoch {}: Loss {}: Change {}'.format(self.epoch, loss, \
                                                    loss - self.prev_loss))
        self.epoch += 1
        self.prev_loss = loss
        filename = self.model_name + ".txt"
        with open(filename, 'a') as f:
            f.write(log_entry + '\n')
            f.close()
