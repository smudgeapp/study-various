#pragma once

#include <iostream>
#include "CategoricalCrossEntropy_Loss.h"




Eigen::ArrayXf CategoricalCrossEntropy_Loss::forward(Eigen::ArrayXXf output, Eigen::ArrayXi classes) {
	Eigen::ArrayXf outArr;
	this->forwardInput = output;
	this->classes = classes;
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
	//document says each value in a row corresponds to a class, but actual calculation comes from input of a single class, that is, a single value of a single class is taken from each set of layer's output
	//it is possible this is what is desired
	//if not, the inputs array would have to be transposed
	Eigen::ArrayXXf clippedArr = output.unaryExpr(clipVals);
	//std::cout << "clipped arr loss: " << clippedArr << std::endl;
	//TODO fix indexing since each column is a single neuron output for the samples = no. of rows
	Eigen::ArrayXf indexedVals = arrayColumnIndices(clippedArr, classes);
	//std::cout << "indexvals loss: " << clippedArr << std::endl;
	//std::cout << "clippedvals " << std::endl << clippedArr << std::endl;
	//std::cout << "indexvals " << std::endl << indexedVals << std::endl;
	outArr = indexedVals.log() * -1;
	//std::cout << "outarr loss: " << clippedArr << std::endl;	
	return outArr;
}


float CategoricalCrossEntropy_Loss::calculate(Eigen::ArrayXXf inputs, Eigen::ArrayXi classes) {
	//std::cout << "input to ccloss: " << inputs << std::endl;
	Eigen::ArrayXf outputArr = forward(inputs, classes);
	//std::cout << "loss fwd:  " << outputArr << std::endl;
	float meanLoss = outputArr.mean();
	//std::cout << "calc loss:  " << meanLoss << std::endl;
	return meanLoss;
}


Eigen::ArrayXXf CategoricalCrossEntropy_Loss::backward(Eigen::ArrayXXf predictions) {
	Eigen::ArrayXXf zeroArr = Eigen::ArrayXXf::Zero(predictions.rows(), predictions.cols());
	Eigen::ArrayXXf classHotEncode = hotEncode(zeroArr, this->classes);
	Eigen::ArrayXXf outArr = -classHotEncode / predictions;
	//std::cout << "pred in: " << std::endl << predictions << std::endl;
	//std::cout << "pred size " << std::endl << predictions.size() << std::endl;
	//std::cout << "classhotencode " << std::endl << classHotEncode << std::endl;
	outArr = outArr / predictions.rows();
	//TODO this backward is not used while softmaxloss is being used - if it is used check outarr calculation first.
	return outArr;

}