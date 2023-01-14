# WORD2VEC Implementation in C++ [using components from the general neural network in this repo](./neuralnetwork)

This is an implementation of the word2vec model in c++ using the basic components of the neural network, separately contained in this repo.

The data input and certain components were modified to fit the word2vec. 

**This is just to gain better understanding of the underlying calculations of the model, therefore, there is no support for full corpus input and pre-processing.**

## Guide

The Word2Vec class contains all the logic for the model.

All training is for the SkipGram model only.

*Epochs are not time-based, in which case, they shouldn't even be called epochs. But the term is used in the code as a matter of differentiation between an iteration and each iteration within that iteration - hopefully that made sense. ;)*

There are several options for running the training.

1. Simple 'train' method will run the training on all words of the corpus each iteraton.
2. 'trainSG' method will run the training on each word seperately wherever it occurs in the corpus. It will obtain the context words then run iterations for each word till a stop condition is met. For each new word, the loss and learning rate is reset.

As a result of the different training modalities, the corpus input methods to the network also vary.

1. For the simple 'train' method only 'setTrainingDataSGAllWords' will work.
2. For 'trainSG' input data can come from 'setTrainingDataSGBothSide' where window moves, over a its length, including words before the target word and after it. The 'setTrainingDataSGFwd' window will move including words only after the target word.

## Instructions

Just simple c++ code, load in editor of choice and run. Only dependency is Eigen. [Get Eigen here.](https://eigen.tuxfamily.org/index.php?title=Main_Page)


*P.S. please excuse the code not being, entirely, cleanly written with a lot of commented parts. Also wrote the code some time back, and although ran it and checked any missing parts before uploading, but it may still contain bugs - hopefully minor ones.*