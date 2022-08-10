#pragma once


#include <Eigen/Core>

#include "Loss.h"
#include "GlobalHelper.h"



 class CategoricalCrossEntropy_Loss : public Loss {
private:
	
	//TODO figure out its return val in python - but first get softmax done	
public:
	Eigen::ArrayXf forwardOutput;
	Eigen::ArrayXXf forwardInput;
	Eigen::ArrayXi classes;
	float calculate(Eigen::ArrayXXf input, Eigen::ArrayXi classes);
	Eigen::ArrayXf forward(Eigen::ArrayXXf output, Eigen::ArrayXi classes);
	Eigen::ArrayXXf backward(Eigen::ArrayXXf predictions);
};