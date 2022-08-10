#pragma once

#include "MeanSquaredLoss.h"


void MeanSquaredLoss::forward() {
	ArrayXXf mclass = this->fwdClass.replicate(this->fwdInput.rows(), 1);
	this->fwdOutput = mclass - this->fwdInput;
	this->fwdOutput = this->fwdOutput.square();
	ArrayXXf rowmean = this->fwdOutput.rowwise().mean();
	this->fwdOutput = rowmean;	
	}


float MeanSquaredLoss::calculateReg(ArrayXXf input, ArrayXXf classes) {
	this->fwdInput = input;
	this->fwdClass = classes;
	this->forward();
	float lossval = this->fwdOutput.mean();
	return lossval;
}

ArrayXXf MeanSquaredLoss::backward(ArrayXXf dinput) {
	ArrayXXf mclass = this->fwdClass.replicate(dinput.rows(), 1);
	this->dMeanSqLoss = (-2 * (mclass - dinput)) / dinput.cols();
	this->dMeanSqLoss = this->dMeanSqLoss / dinput.rows();
	//std::cout << "dmeansqloss " << this->dMeanSqLoss << std::endl;
	return this->dMeanSqLoss;

}

float MeanSquaredLoss::calculate(ArrayXXf input, ArrayXi classes) {
	
	
	return 0.0;
}