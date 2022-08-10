#pragma once


#include <Eigen/Core>

#include "GlobalHelper.h"
#include "ActivationSoftmax.h"
#include "CategoricalCrossEntropy_Loss.h"
#include "Loss.h"

#include <iostream>
#include <vector>

using namespace Eigen;

class SoftmaxLoss {
public:
	ActivationSoftmax softmax;
	Loss* cceLoss;
	ArrayXXf fwdInputs;
	ArrayXi classtargets;
	ArrayXXf softmaxOutput;
	ArrayXXf lossVals;
	float mainLoss;
	std::vector<DenseLayer> layers;
	SoftmaxLoss();
	SoftmaxLoss(std::vector<DenseLayer> layerList);
	float forward(ArrayXXf inputs, ArrayXi classtargets);
	ArrayXXf backward();
	//TODO method to get regularization for multiple classes.
};
