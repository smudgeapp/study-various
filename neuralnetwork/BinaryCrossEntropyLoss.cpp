#pragma once

#include "BinaryCrossEntropyLoss.h"


ArrayXXf BinaryCrossEntropyLoss::forward() {
	ArrayXXf fwdOut;
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

	ArrayXXf clipFwdInput = this->fwdInput.unaryExpr(clipVals);
	ArrayXXf clipFwdInput1 = 1 - clipFwdInput;
	clipFwdInput = clipFwdInput.log();
	clipFwdInput1 = clipFwdInput1.log();
	ArrayXXf mclass = this->fwdClasses.cast<float>();
	ArrayXXf mclass1 = 1 - mclass;
	this->fwdOutput = (mclass.replicate(1, clipFwdInput.cols()) * clipFwdInput) + (mclass1.replicate(1, clipFwdInput1.cols()) * clipFwdInput1);

	return this->fwdOutput;
}

float BinaryCrossEntropyLoss::calculate(ArrayXXf input, ArrayXi classes) {
	this->fwdInput = input;
	this->fwdClasses = classes;
	this->fwdOutput = this->forward();
	float lossVal = this->fwdOutput.rowwise().mean().mean();
	return lossVal;
}


void BinaryCrossEntropyLoss::backward(ArrayXXf dinputs) {
	ArrayXXf mclass = this->fwdClasses.cast<float>().replicate(1, dinputs.cols());
	ArrayXXf mclass1 = 1 - this->fwdClasses.cast<float>();
	mclass1 = mclass1.cast<float>().replicate(1, dinputs.cols());
	this->dBinLoss = (-(mclass / dinputs) + (mclass1 / (1 - dinputs))) / dinputs.cols();
	//std::cout << "binloss backward cols " << this->dBinLoss << std::endl;
	this->dBinLoss = this->dBinLoss / dinputs.rows();
	//std::cout << "binloss backward rows " << this->dBinLoss << std::endl;
	
}