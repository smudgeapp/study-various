#pragma once


#include "OptimizerSGD.h"

//initiate the optimizer, provide optimizers input as applicable.

OptimizerSGD::OptimizerSGD(float learning_rate, float learning_decay, float moment, float epsilonIn, float rhoIn, float beta1In, float beta2In) {
	this->inputLR = learning_rate;
	this->learningRate = this->inputLR;
	this->learningDecay = learning_decay;
	this->momentum = moment;
	this->epsilon = epsilonIn;
	this->rho = rhoIn;
	this->beta1 = beta1In;
	this->beta2 = beta2In;
}



void OptimizerSGD::autoUpdateParams() {
	this->iteration += 1;
	this->learningRate = this->inputLR * (1 / (1 + (this->learningDecay * this->iteration)));
	//std::cout << "OPTIMIZER UPDATE = " << this->iteration << std::endl;
	//std::cout << "learning rate = " << this->learningRate << std::endl;
}

void OptimizerSGD::resetParams() {
	this->iteration = 0;
	this->learningRate = this->inputLR;
}

//set the type of optimizer

void OptimizerSGD::setOptimizer(int optimizertype) {
	this->optType = optimizertype;
	
}


//single function to update layers - layers are updated as per input variables and the selected optimizer.

void OptimizerSGD::updateLayer(ArrayXXf wtGradients, ArrayXXf biasGradients, DenseLayer &layer) {
	//std::cout << "opt update " << layer.dInput << std::endl;
	if (this->optType == PLAINSGD) {
		plainSGD(wtGradients, biasGradients, layer);
	}
	else if (this->optType == ADAGRAD) {
		adaGrad(wtGradients, biasGradients, layer);
	}
	else if (this->optType == RMSPROP) {
		rmsProp(wtGradients, biasGradients, layer);
	}
	else if (this->optType == ADAM) {
		adam(wtGradients, biasGradients, layer);
	}
	
}

void OptimizerSGD::plainSGD(ArrayXXf wtGradients, ArrayXXf biasGradients, DenseLayer &layer) {
	//std::cout << "biasgrad = " << biasGradients << std::endl;
	ArrayXXf weightUpdates;
	ArrayXXf biasUpdates;
	weightUpdates = (this->momentum * layer.wtMomentum) - (this->learningRate * wtGradients);
	biasUpdates = (this->momentum * layer.biasMomentum) - (this->learningRate * biasGradients);

	//std::cout << "weight * momentum: " << std::endl << this->momentum * layer.wtMomentum << std::endl;
	layer.wtMomentum = weightUpdates;
	layer.biasMomentum = biasUpdates;
	//std::cout << "weight updates " << std::endl << layer.wtMomentum << std::endl;

	//std::cout << "prior update " << std::endl << layer.wtMat << std::endl;
	layer.wtMat += weightUpdates;
	//std::cout << "update bias " << std::endl << layer.biasMat << std::endl;
	layer.biasMat += biasUpdates;
	//std::cout << "update wts " << std::endl << layer.wtMat << std::endl;
}

void OptimizerSGD::adaGrad(ArrayXXf wtGradients, ArrayXXf biasGradients, DenseLayer& layer) {
	layer.wtCache += wtGradients.square();
	layer.biasCache += biasGradients.square();

	layer.wtMat += -this->learningRate * wtGradients / (layer.wtCache.sqrt() + this->epsilon);
	//std::cout << "ada grad wts: " << layer.wtMat << std::endl;
	layer.biasMat += -this->learningRate * biasGradients / (layer.biasCache.sqrt() + this->epsilon);
}

void OptimizerSGD::rmsProp(ArrayXXf wtGradients, ArrayXXf biasGradients, DenseLayer& layer) {
	layer.wtCache = (this->rho * layer.wtCache) + ((1 - this->rho) * wtGradients.square());
	layer.biasCache = (this->rho * layer.biasCache) + ((1 - this->rho) * biasGradients.square());

	layer.wtMat += -this->learningRate * wtGradients / (layer.wtCache.sqrt() + this->epsilon);
	layer.biasMat += -this->learningRate * biasGradients / (layer.biasCache.sqrt() + this->epsilon);
}

void OptimizerSGD::adam(ArrayXXf wtGradients, ArrayXXf biasGradients, DenseLayer& layer) {
	ArrayXXf weightUpdates; //momentum update weights
	ArrayXXf biasUpdates; //momentum update bias
	ArrayXXf weightcacheUpdate; //cache update wts
	ArrayXXf biascacheUpdate; //cache update bias

	layer.wtMomentum = (this->beta1 * layer.wtMomentum) + ((1 - this->beta1) * wtGradients);
	layer.biasMomentum = (this->beta1 * layer.biasMomentum) + ((1 - this->beta1) * biasGradients);
	//std::cout << "adam wtmomentum: " << layer.wtMomentum << std::endl;
	weightUpdates = layer.wtMomentum / (1 - pow(this->beta1, this->iteration + 1));
	biasUpdates = layer.biasMomentum / (1 - pow(this->beta1, this->iteration + 1));

	layer.wtCache = (this->beta2 * layer.wtCache) + ((1 - this->beta2) * wtGradients.square());
	layer.biasCache = (this->beta2 * layer.biasCache) + ((1 - this->beta2) * biasGradients.square());

	weightcacheUpdate = layer.wtCache / (1 - pow(this->beta2, this->iteration + 1));
	biascacheUpdate = layer.biasCache / (1 - pow(this->beta2, this->iteration + 1));
	
	this->udBeta1 = 1 - pow(this->beta1, this->iteration + 1);
	this->udBeta2 = 1 - pow(this->beta2, this->iteration + 1);

	layer.wtMat += -this->learningRate * weightUpdates / (weightcacheUpdate.sqrt() + this->epsilon);
	layer.biasMat += -this->learningRate * biasUpdates / (biascacheUpdate.sqrt() + this->epsilon);
	
}

