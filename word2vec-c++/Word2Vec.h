#pragma once


#include <vector>
#include <iostream>
#include <map>
#include <algorithm>

#include <Eigen/Core>

#include "DenseLayer.h"
#include "OptimizerSGD.h"
#include "SkipgramSoftmaxLoss.h"


using namespace std;
using namespace Eigen;

//TODO iterate each word individually and then save the weights.

class Word2Vec {
public:
	map<string, int> vocab;
	map<int, string> wordkeys;
	vector<vector<string>> corpus;
	map<int, map<int, string>> corpusMap;
	map<string, ArrayXXf> hiddenWts;
	map<string, ArrayXXf> outputWts;
	vector<int> trainwords;
	int totalWordCount = 0;
	int totalSentCount = 0;
	int sentItr = 0;
	int wordItr = 0;
	bool epochEnd = false;
	int features = 3;
	int windowsize = 2;
	DenseLayer inputLayer;
	DenseLayer outputLayer;
	SkipgramSoftmaxLoss sgSmax;
	OptimizerSGD optimizer;
	GlobalHelper helper;
	float learningRate = 0.025f;
	float learningDecay = 0.025f;
	float momentum = 0.5f;
	float loss = 100000000;
	int epochs = 30000;
	ArrayXXf targetVecs;
	ArrayXXf inputVec;
	ArrayXXf totalVec;
	Word2Vec(vector<vector<string>> corpus, int featuresize = 3, int windowsize = 2, float learningRate = 0.8f, 
		float learningDecay = 1.0f, float momentum = 0.5f);
	void train();
	void trainSG();
	bool setTrainingDataSGFwd(string trainword);
	
	

private:
	void createVocab();
	void setTrainingDataSGAllWords();
	bool setTrainingDataSGBothSide(string trainword);
	
	int getWordSerial(string word);
	void saveWeights(string word);
	
};
