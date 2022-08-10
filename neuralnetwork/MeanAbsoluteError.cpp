#pragma once

#include "MeanAbsoluteError.h"


void MeanAbsoluteError::forward() {
	this->fwdOutput = this->fwdClasses - this->fwdInput;
	this->fwdOutput = this->fwdOutput.abs();
	ArrayXXf meanarr = this->fwdOutput.rowwise().mean();
	this->fwdOutput = meanarr;

}


float MeanAbsoluteError::calculate(ArrayXXf inputs, ArrayXi classes) {
	this->fwdInput = inputs;
	this->fwdClasses = classes.cast<float>().replicate(1, inputs.cols()); //check is this is required when building model
	this->forward();
	float lossVal = this->fwdOutput.mean();
	return lossVal;
}



void MeanAbsoluteError::backward(ArrayXXf dinputs) {
	auto absdiff = [](float inVal) {
		if (inVal > 0) {
			inVal = 1;
		}
		else {
			inVal = -1;
		}
		return inVal;
	};

	this->dMeanAbsErr = dinputs.unaryExpr(absdiff);
	this->dMeanAbsErr = this->dMeanAbsErr / dinputs.cols();
	this->dMeanAbsErr = this->dMeanAbsErr / dinputs.rows();

}


