#pragma once

#include "Dropout.h"


Dropout::Dropout() {

}

Dropout::Dropout(DenseLayer* layer, float dropoutRate) {
	this->rate = 1 - dropoutRate;
	this->layerM = layer;
	//TODO denselayer is not used but left here just in case

}

//TODO fix dropout sequence - dropout is after activation of dense layer
ArrayXXf Dropout::forward(ArrayXXf inputVals) {
	std::default_random_engine generator;
	std::binomial_distribution<int> distribution(1, this->rate);

	ArrayXXi dropoutInput = ArrayXXi::Ones(inputVals.rows(), inputVals.cols());

	auto randGen = [&](int) {
		return distribution(generator);
	};
	if (this->rate < 1) {
		dropoutInput = dropoutInput.unaryExpr(randGen);
	}
	//std::cout << "dropout mask: " << std::endl << this->dropoutMask.cast<float>() << std::endl;
	this->dropoutMask = dropoutInput.cast<float>() / this->rate;
	this->dropoutFwd = this->dropoutMask * inputVals;
	//std::cout << "dropout fwd mult: " << std::endl << this->dropoutFwd << std::endl;
	//this->dropoutFwd = this->dropoutFwd / this->rate;
	//std::cout << "dropout fwd final: " << std::endl << this->dropoutFwd << std::endl;
	return this->dropoutFwd;
}


ArrayXXf Dropout::backward(ArrayXXf dValues) {
	if (this->rate < 1) {
		this->dDropout = dValues * this->dropoutMask;
	}
	else {
		this->dDropout = dValues;
	}
	
	return this->dDropout;
}