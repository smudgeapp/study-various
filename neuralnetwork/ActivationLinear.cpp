#pragma once

#include "ActivationLinear.h"



ArrayXXf ActivationLinear::forward(ArrayXXf inputs) {
	this->fwdInputs = inputs;
	this->fwdOutput = inputs;
	return this->fwdOutput;
}


ArrayXXf ActivationLinear::backward(ArrayXXf dinputs) {
	this->dActLinear = dinputs;
	return this->dActLinear;
}