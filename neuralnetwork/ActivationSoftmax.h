#pragma once


#include <Eigen/Core>

#include <iostream>
#include "GlobalHelper.h"

class ActivationSoftmax {
public:
	Eigen::ArrayXXf forwardInput;
	Eigen::ArrayXXf smaxOutput;
	Eigen::ArrayXXf forward(Eigen::ArrayXXf input);
	Eigen::ArrayXXf backward(Eigen::ArrayXXf backInput);
};
