#pragma once

#include "RegressionModel.h"

RegressionModel::RegressionModel(int inputCt, int outputCt, int midLayerCt, ArrayXXf inputs, ArrayXXf actualOutputT) {
	this->inputs = inputCt;
	this->outputs = outputCt;
	this->midLayers = midLayerCt;
	this->mainInput = inputs;
	this->actualOutput = actualOutputT;
	this->totalLayers = 2 + this->midLayers;
	this->wtReg2 = 0.01f;
	this->biasReg2 = 0.01f;
	this->inputLayer = DenseLayer(inputCt, this->midLayerNeurons, this->wtReg, this->wtReg2, this->biasReg, this->biasReg2);
	this->inputDropout = Dropout(&this->inputLayer, this->dropoutRate);
	this->allDenseLayers.push_back(this->inputLayer);
	for (int i = 0; i < this->midLayers; i++) {
		addLayer();
	}
	this->outputLayer = DenseLayer(this->midLayerNeurons, outputCt);
	this->allDenseLayers.push_back(this->outputLayer);
}


//convenience method for adjusting input weights. This is for outside model/manual adjustment of weights
//depending on the context of the regression problem. For instance, random input weights for tax revenue forecasting may be adjusted by
//a normalized version of any number of influencing factors, like, GDP, Imports, Employment, etc.

//Original method is in DenseLayer class
void RegressionModel::adjustInputWeights(ArrayXXf wtAdj, bool colwise) {
	this->wtAdj = wtAdj;
	this->inputLayer.regressionWtAdjustment(wtAdj, colwise);
}

void RegressionModel::addLayer() {
	DenseLayer newlayer = DenseLayer(this->midLayerNeurons, this->midLayerNeurons);
	this->layerList.push_back(newlayer);
	ActivationReLU newActLayer = ActivationReLU();
	this->activationLayers.push_back(newActLayer);
	this->allDenseLayers.push_back(newlayer);
}


void RegressionModel::setOptimizer(int optimizerType, map<string, float> params) {
	
	this->learning_rate = params[this->learningRateId];
	this->learning_decay = params[this->learningDecayId];
	if (optimizerType == mOptimizer.PLAINSGD) {
		this->moment = params[this->momentId];
		
	}
	else if (optimizerType == mOptimizer.ADAGRAD) {
		this->epsilon = params[this->epsilonId];
	}
	else if (optimizerType == mOptimizer.RMSPROP) {
		this->rho = params[this->rhoId];
		this->epsilon = params[this->epsilonId];
	}
	else if (optimizerType == mOptimizer.ADAM) {
		this->epsilon = params[this->epsilonId];
		this->beta = params[this->betaId];
		this->beta2 = params[this->beta2Id];
	}
	this->mOptimizer = OptimizerSGD(this->learning_rate, this->learning_decay, this->moment, this->epsilon, this->rho, this->beta, this->beta2);
	this->mOptimizer.setOptimizer(optimizerType);
	

}

void RegressionModel::train() {
	bool endtrain = false;
	while (!endtrain) {
		
		//FORWARD
		ArrayXXf fwdOutput = this->inputLayer.forward(mainInput);
		ArrayXXf fwdInput = fwdOutput;
		fwdOutput = this->firstActlayer.forward(fwdInput);
		fwdInput = fwdOutput;
		//cout << "first layer fwd: " << fwdOutput << endl;
		//cout << "first wts: " << this->inputLayer.wtMat << endl;
		fwdOutput = this->inputDropout.forward(fwdInput);
		fwdInput = fwdOutput;
		//cout << "dropput 1: " << fwdOutput << endl;
		
		for (int i = 0; i < this->layerList.size(); i++) {
			fwdOutput = this->layerList[i].forward(fwdInput);
			fwdInput = fwdOutput;
			//cout << "mid layer " << i << " output " << fwdOutput << endl;
			//cout << "mid wts " << i << " fwd " << layerList[i].wtMat << endl;
			fwdOutput = this->activationLayers[i].forward(fwdInput);
			//cout << "mid layer " << i << " activ out; " << fwdOutput << endl;
			fwdInput = fwdOutput;
		}
		
		fwdOutput = this->outputLayer.forward(fwdInput);
		fwdInput = fwdOutput;
		//cout << "output layer fwd: " << fwdOutput << endl;
		//cout << "output wts: " << this->outputLayer.wtMat << endl;
		fwdOutput = this->finalActLayer.forward(fwdInput);
		fwdInput = fwdOutput;
		this->mse = this->msqLoss.calculateReg(fwdInput, this->actualOutput);
		this->totalLoss = mse + msqLoss.regularizationLoss(this->allDenseLayers);
		this->accuracyVal = accuracy(fwdInput, this->actualOutput);
		
		//BACKWARD
		ArrayXXf bwdOutput = msqLoss.backward(fwdInput);

		ArrayXXf bwdInput = bwdOutput;
		bwdOutput = this->finalActLayer.backward(bwdInput);
		bwdInput = bwdOutput;
		bwdOutput = this->outputLayer.backward(bwdInput);
		bwdInput = bwdOutput;
		//cout << "output bwd " << bwdOutput << endl;
		
		for (int j = this->layerList.size() - 1; j >= 0; j--) {
			//cout << "outputbwd in midlayer loop: " << bwdOutput << endl;
			bwdOutput = this->activationLayers[j].backward(bwdInput);
			bwdInput = bwdOutput;
			//cout << "mid act: " << j << " bwd out " << bwdOutput << endl;
			bwdOutput = this->layerList[j].backward(bwdInput);
			bwdInput = bwdOutput;
			//cout << "mid dense: " << j << " bwd out " << bwdOutput << endl;
		}
		
		//cout << "before dropoutbwd: " << bwdOutput << endl;
		bwdOutput = this->inputDropout.backward(bwdInput);
		//cout << "after dropout bwd: " << bwdOutput << endl;
		bwdInput = bwdOutput;
		bwdOutput = this->firstActlayer.backward(bwdInput);
		bwdInput = bwdOutput;
		//cout << "first actv bwd: " << bwdOutput << endl;
		bwdOutput = this->inputLayer.backward(bwdInput);
		//cout << "final input bwd: " << bwdOutput << endl;
		

		//OPTIMIZATION
		mOptimizer.updateLayer(this->inputLayer.dWeights, this->inputLayer.dBias, this->inputLayer);
		//this->inputLayer.regressionWtAdjustment(this->wtAdj, false);
		for (int k = 0; k < this->layerList.size(); k++) {
			DenseLayer layer = this->layerList[k];
			mOptimizer.updateLayer(layer.dWeights, layer.dBias, layer);
		}
		mOptimizer.updateLayer(this->outputLayer.dWeights, this->outputLayer.dBias, this->outputLayer);
		mOptimizer.autoUpdateParams();

		this->trainCount += 1;
		if (this->trainCount % 500 == 0) {
			cout << "End: iteration = " << this->trainCount;
			cout << ", MSE = " << this->mse;
			cout << ", RegLoss = " << this->totalLoss;
			cout << ", Accuracy = " << this->accuracyVal;
			cout << ", LR = " << this->mOptimizer.learningRate << endl;
		}
		endtrain = endtraining();
		
	}
	cout << "output predictions: " << this->outputLayer.forwardOutput << endl;
	this->saveModel();
}

void RegressionModel::validate(ArrayXXf input) {
	ArrayXXf output = this->inputLayer.forward(input);
	ArrayXXf inputArr = output;
	output = this->firstActlayer.forward(inputArr);
	inputArr = output;
	for (int i = 0; i < this->layerList.size(); i++) {
		output = this->layerList[i].forward(inputArr);
		inputArr = output;
		output = this->activationLayers[i].forward(inputArr);
		inputArr = output;
	}
	output = this->outputLayer.forward(inputArr);
	inputArr = output;
	output = this->finalActLayer.forward(inputArr);
	cout << "Validation Output: " << output << endl;
}

float RegressionModel::accuracy(ArrayXXf prediction, ArrayXXf actual) {
	ArrayXXf diff = prediction.row(0) - actual;
	diff = diff.abs();
	float tempAcc = diff.mean();
	return tempAcc;
}


//set criteria for ending model training
//could be any combination of factors or a single one - number of iterations, loss reduction, etc.

bool RegressionModel::endtraining() {
	bool endtrain = false;
	if (this->prevLoss == this->mse) {
		this->lossCt += 1;
	}
	else {
		this->lossCt = 0;
	}
	this->prevLoss = this->mse;
	if (this->lossCt > 10) {
		cout << "Loss unchanged." << endl;
		endtrain = true;
	}
	if (this->mOptimizer.learningRate <= 0.0000f) {
		cout << "LR zero" << endl;
		endtrain = true;
	}
	if (this->trainCount > 1000) {
		cout << "Train count reached." << endl;
		endtrain = true;
	}
	return endtrain;
}

//input desired save location/path

void RegressionModel::saveModel() {
	ofstream modelFile;
	modelFile.open("[input save path]");
	for (int i = 0; i < this->allDenseLayers.size(); i++) {
		ArrayXXf wtArr = this->allDenseLayers[i].wtMat;
		modelFile << "Layer " << i << "\n";
		modelFile << "Weights" << "\n";
		for (auto row : wtArr.rowwise()) {
			for (auto it = row.begin(); it != row.end(); it++) {
				modelFile << *it << ",";
			}
			modelFile << "\n";
		}
		ArrayXXf biasArr = this->allDenseLayers[i].biasMat;
		modelFile << "Bias" << "\n";
		for (auto row : biasArr.rowwise()) {
			for (auto it = row.begin(); it != row.end(); it++) {
				modelFile << *it << ",";
			}
			modelFile << "\n";
		}
		
	}
	
}