#pragma once

#include <Eigen/Core>
#include "GlobalHelper.h"

//Convenience class for generating random input weights and biases.
//Inputs may be any number, neurons have to be equivalent to the desired number of neurons of the output layer.

class WeightsBiasManager {
public:
	WeightsBiasManager();
	Eigen::ArrayXXf getWeights(int inputs, int neurons);
	Eigen::ArrayXXf getBias(int neurons);
	GlobalHelper gHelper;
	
};
