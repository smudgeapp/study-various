#pragma once

#include "DenseLayer.h"
#include "ActivationReLU.h"
#include "ActivationLinear.h"
#include "Dropout.h"
#include "MeanSquaredLoss.h"
#include "MeanAbsoluteError.h"
#include "OptimizerSGD.h"
#include "WeightsBiasManager.h"
#include "Loss.h"
#include <vector>
#include <cstdarg>
#include <string>
#include <map>
#include <fstream>
#include <iostream>

//Regression model using the various neural net component classes.
//Takes csv format inputs and saves the output weights and biases in the same format.

using namespace std;

class RegressionModel {
public:
	vector<DenseLayer> layerList;
	vector<ActivationReLU> activationLayers;
	vector<DenseLayer> allDenseLayers;
	string learningRateId = "LEARNING_RATE";
	string learningDecayId = "LEARNING_DECAY";
	string momentId = "MOMENT";
	string epsilonId = "EPSILON";
	string rhoId = "RHO";
	string betaId = "BETA";
	string beta2Id = "BETA2";
	float learning_rate = 0.0f;
	float learning_decay = 0.0f;
	float moment = 0.01f;
	float epsilon = 0.0f;
	float rho = 0.0f;
	float beta = 0.0f;
	float beta2 = 0.0f;
	float wtReg = -1.0f;
	float wtReg2 = -1.0f;
	float biasReg = -1.0f;
	float biasReg2 = -1.0f;
	int inputs;
	int outputs;
	int midLayers;
	int totalLayers;
	int midLayerNeurons = 32;
	float mse;
	float mae;
	float totalLoss;
	float accuracyVal;
	float prevLoss;
	float lossCt = 0;
	float dropoutRate = 0;
	int trainCount = 0;
	float stdev;
	MeanSquaredLoss msqLoss = MeanSquaredLoss();
	MeanAbsoluteError maLoss = MeanAbsoluteError();
	OptimizerSGD mOptimizer;
	ArrayXXf mainInput;
	ArrayXXf actualOutput;
	ArrayXXf wtAdj;
	DenseLayer inputLayer;
	DenseLayer outputLayer;
	ActivationReLU firstActlayer = ActivationReLU();
	ActivationLinear finalActLayer = ActivationLinear();
	Dropout inputDropout;
	RegressionModel(int inputCt, int outputCt, int midLayersCt, ArrayXXf inputs, ArrayXXf actualOutputT);
	void addLayer();
	float loss();
	float accuracy(ArrayXXf prediction, ArrayXXf actualVals);
	void setOptimizer(int optimizerType, map<string, float> params);
	void train();
	void adjustInputWeights(ArrayXXf wtadj, bool colwise);
	void validate(ArrayXXf input);

private:
	bool endtraining();
	void saveModel();


};
