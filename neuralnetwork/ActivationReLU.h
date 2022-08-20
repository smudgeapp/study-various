#pragma once

#include <iostream>
#include <Eigen/Core>


class ActivationReLU {
public:
	Eigen::ArrayXXf forwardInput;
	Eigen::ArrayXXf backwardOutput;
	Eigen::ArrayXXf forward(Eigen::ArrayXXf input);
	Eigen::ArrayXXf backward(Eigen::ArrayXXf backInput);
};
