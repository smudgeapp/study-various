#pragma once

#include "ActivationSoftmax.h"



Eigen::ArrayXXf ActivationSoftmax::forward(Eigen::ArrayXXf input) {
	this->forwardInput = input;
	ArrayXXf smaxout = exp(input - input.rowwise().maxCoeff().replicate(1, input.cols()));
	smaxout = smaxout / smaxout.rowwise().sum().replicate(1, smaxout.cols());
	this->smaxOutput = smaxout;
	return smaxout;
}

Eigen::ArrayXXf ActivationSoftmax::backward(Eigen::ArrayXXf backInput) {
	Eigen::MatrixXf outMat = Eigen::MatrixXf::Zero(this->forwardInput.rows(), this->forwardInput.cols());
	Eigen::ArrayXXf outArr;
	Eigen::MatrixXf bInputMat = backInput.matrix();
	for (int i = 0; i < this->smaxOutput.rows(); i++) {
		Eigen::ArrayXXf smaxSingle = this->smaxOutput.row(i).transpose();
		Eigen::ArrayXXf zeroArr = Eigen::ArrayXXf::Zero(smaxSingle.size(), smaxSingle.size());
		Eigen::ArrayXXf smaxRowIdentity = rowIdentity(zeroArr, smaxSingle);
		//std::cout << "actvsmax row id " << std::endl << smaxRowIdentity << std::endl;
		Eigen::MatrixXf smaxDerivative = smaxRowIdentity.matrix() - (smaxSingle.matrix() * smaxSingle.transpose().matrix());
		//std::cout << "actvsmax smaxderivative " << std::endl << smaxDerivative << std::endl;
		//std::cout << "binput i " << std::endl << bInputMat.row(i) << std::endl;
		Eigen::MatrixXf outVal = smaxDerivative * bInputMat.row(i).transpose();
		//std::cout << "actvsmax outval " << std::endl << outVal << std::endl;
		outMat.row(i) = outVal.transpose().row(0);
		
	}
	outArr = outMat.array();
	//std::cout << "outArr smax " << std::endl << outArr << std::endl;
	return outArr;
}