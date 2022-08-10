#pragma once


#include "SoftmaxLoss.h"

SoftmaxLoss::SoftmaxLoss() {
	this->softmax = ActivationSoftmax();
	this->cceLoss = new CategoricalCrossEntropy_Loss();
}

SoftmaxLoss::SoftmaxLoss(std::vector<DenseLayer> layerList) {
	this->softmax = ActivationSoftmax();
	this->cceLoss = new CategoricalCrossEntropy_Loss();
	this->layers = layerList;
}

float SoftmaxLoss::forward(ArrayXXf inputs, ArrayXi classtargets) {
	float lossVal;

	this->fwdInputs = inputs;
	this->classtargets = classtargets;
	this->softmaxOutput = softmax.forward(inputs);
	lossVal = this->cceLoss->calculate(this->softmaxOutput, classtargets);
	//loss forward
	this->mainLoss = lossVal;
	lossVal += this->cceLoss->regularizationLoss(this->layers);
	return lossVal;
}


ArrayXXf SoftmaxLoss::backward() {
	ArrayXXf softmaxLossBack;

	ArrayXXf zeroArr = ArrayXXf::Zero(this->fwdInputs.rows(), this->fwdInputs.cols());
	ArrayXXf classHotEncode = hotEncode(zeroArr, this->classtargets);
	softmaxLossBack = this->softmaxOutput - classHotEncode;
	softmaxLossBack = softmaxLossBack / this->softmaxOutput.rows();
	return softmaxLossBack;
}

