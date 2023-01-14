#pragma once


#include "SkipgramSoftmaxLoss.h"

ArrayXXf SkipgramSoftmaxLoss::forward(ArrayXXf input, ArrayXXf targets) {
	//this->forwardInput = input * targets.colwise().sum();
	this->forwardInput = input - input.maxCoeff();
	ArrayXXf smaxout = exp(this->forwardInput);
	smaxout = smaxout / smaxout.sum();
	this->forwardOutput = smaxout;
	return smaxout;
}


float SkipgramSoftmaxLoss::loss(ArrayXXf targets) {
	//cout << "in loss target: " << targets << endl;
	auto clipVals = [](float inVal) {
		if (inVal < 1e-7) {
			inVal = 1e-7;
		}
		else if (inVal > 1.0 - 1e-7) {
			inVal = 1 - 1e-7;
		}
		else {
			inVal = inVal;
		}
		return inVal;
	};
	ArrayXXf output = this->forwardOutput.unaryExpr(clipVals);
	float loss = 0;
	//MatrixXf lossFwd = targets.matrix() * output.transpose().matrix();
	ArrayXXf lossFwdF = output * targets.colwise().sum();
	//cout << "lossFwd = " << lossFwdF << endl;
	loss = lossFwdF.sum();
	loss = log(loss) * -1;
	return loss;
}

ArrayXXf SkipgramSoftmaxLoss::backward(ArrayXXf targets) {
	ArrayXXf newTarget = targets.colwise().sum();
	ArrayXXf smaxBwd = newTarget * this->forwardOutput;
	smaxBwd = this->forwardOutput - newTarget;
	//smaxBwd = this->forwardOutput - targets;
	//cout << "smax bwd " << endl << smaxBwd << endl;
	smaxBwd = smaxBwd / smaxBwd.cols();
	//cout << "smaxbwd div " << endl << smaxBwd << endl;
	return smaxBwd;

}