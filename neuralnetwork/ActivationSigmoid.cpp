#pragma once


#include "ActivationSigmoid.h"



void ActivationSigmoid::forward(ArrayXXf input) {
	this->fwdInput = input;
	auto sigmoidfwd = [](float inVal) {
		inVal = 1 / (1 + exp(-inVal));
		return inVal;

	};
	this->fwdOutput = input.unaryExpr(sigmoidfwd);
}


void ActivationSigmoid::backward(ArrayXXf dinput) {
	this->dSigmoid = dinput * ((1 - this->fwdOutput) * this->fwdOutput);
}