#pragma once

#include "ActivationReLU.h"

using namespace std;

Eigen::ArrayXXf ActivationReLU::forward(Eigen::ArrayXXf input) {
	Eigen::ArrayXXf actvMat;
	auto reluFwdFunc = [](float inVal) {
		if (inVal <= 0) {
			inVal = 0.;
		}
		return inVal;
	};
	actvMat = input.unaryExpr(reluFwdFunc);
	return actvMat;
}

Eigen::ArrayXXf ActivationReLU::backward(Eigen::ArrayXXf backInput) {
	auto drelufunc = [](float inVal) {
		if (inVal > 0) {
			inVal = 1;
		}
		else {
			inVal = 0.;
		}
		return inVal;
	};

	Eigen::ArrayXXf backwardOut = backInput.unaryExpr(drelufunc);
	return backwardOut;
}