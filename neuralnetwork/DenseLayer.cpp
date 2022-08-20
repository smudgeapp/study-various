#pragma once

#include "DenseLayer.h"

DenseLayer::DenseLayer() {

}

DenseLayer::DenseLayer(int inputs, int neurons, float wtReg1, float wtReg2, float biasReg1, float biasReg2) {
	//cols/input should be equal to the number of features per input neuron
	//rows/neurons should be equal to the desired neurons in the output layer
	WeightsBiasManager wtMngr = WeightsBiasManager();
	wtMat = wtMngr.getWeights(inputs, neurons);
	biasMat = wtMngr.getBias(neurons);
	//std::cout << "weights: " << wtMat << std::endl;
	wtCache = ArrayXXf::Zero(inputs, neurons);
	biasCache = ArrayXXf::Zero(1, neurons);
	wtMomentum = ArrayXXf::Zero(inputs, neurons);
	biasMomentum = ArrayXXf::Zero(1, neurons);
	wtRegLoss1 = wtReg1;
	wtRegLoss2 = wtReg2;
	biasRegLoss1 = biasReg1;
	biasRegLoss2 = biasReg2;	
}

void DenseLayer::regressionWtAdjustment(ArrayXXf wtadj, bool colwise) {
	//std::cout << "orig wts: " << this->wtMat << std::endl;
	ArrayXXf arr;
	if (colwise) {
		arr = wtadj.replicate(1, this->wtMat.cols());
	}
	else {
		arr = wtadj.replicate(this->wtMat.rows(), 1);
	}
	std::cout << "wt adj mid arr: " << arr << std::endl;
	ArrayXXf finalArr = this->wtMat + arr;
	this->wtMat = finalArr;
	//std::cout << "adjusted wts " << this->wtMat << std::endl;
}

Eigen::ArrayXXf DenseLayer::forward(Eigen::ArrayXXf inputMat) {
	Eigen::MatrixXf midMat(inputMat.rows(), this->wtMat.cols());
	midMat = (inputMat.matrix() * DenseLayer::wtMat.matrix());
	//Eigen::ArrayXXf outputMat(inputMat.rows(), this->wtMat.cols());
	//outputMat = midMat.array().rowwise() + DenseLayer::biasMat.row(0);
	midMat += this->biasMat.matrix().replicate(midMat.rows(), 1);
	this->forwardInput = inputMat;
	this->forwardOutput = midMat.array(); // outputMat;
	return midMat.array();
	//return outputMat;
	//return midMat.array();
}



//backward input from activationReLU
ArrayXXf DenseLayer::backward(Eigen::ArrayXXf backInputMat) {
	
	//std::cout << "dense backinput " << std::endl << backInputMat << std::endl;
	Eigen::MatrixXf fwdInputT = this->forwardInput.transpose().matrix();
	//std::cout << "fwdInputT " << std::endl << fwdInputT << std::endl;
	Eigen::MatrixXf dwtmid = fwdInputT * backInputMat.matrix();
	//std::cout << "dwtmid " << std::endl << dwtmid << std::endl;
	this->dWeights = dwtmid.array();
	//std::cout << "main dwt " << std::endl << this->dWeights << std::endl;
	Eigen::MatrixXf dinputmid = backInputMat.matrix() * this->wtMat.transpose().matrix();
	this->dInput = dinputmid.array();
	this->dBias = backInputMat.colwise().sum();
	
	//std::cout << "backward dbias " << std::endl << this->dBias << std::endl;

	auto regLoss1DFunc = [](float inVal) {
		if (inVal >= 0) {
			inVal = 1.0;
		}
		else {
			inVal = -1.0;
		}
		return inVal;
	};

	if (this->wtRegLoss1 > 0.f) {
		ArrayXXf wtRegLoss1D = this->wtMat.unaryExpr(regLoss1DFunc);
		this->dWeights += this->wtRegLoss1 * wtRegLoss1D;
	}

	if (this->biasRegLoss1 > 0.f) {
		ArrayXXf biasRegLoss1D = this->biasMat.unaryExpr(regLoss1DFunc);
		this->dBias += this->biasRegLoss1 * biasRegLoss1D;
	}

	if (this->wtRegLoss2 > 0.f) {
		this->dWeights += 2 * this->wtRegLoss2 * this->wtMat;
	}

	if (this->biasRegLoss2 > 0.f) {
		this->dBias += 2 * this->biasRegLoss2 * this->biasMat;
	}

	return this->dInput;

}


