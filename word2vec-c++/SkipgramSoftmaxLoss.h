#pragma once


#include <math.h>
#include <iostream>


#include <Eigen/Core>


using namespace std;
using namespace Eigen;

class SkipgramSoftmaxLoss {
public:
	ArrayXXf forwardInput;
	ArrayXXf forwardOutput;
	ArrayXXf forward(ArrayXXf input, ArrayXXf targets);
	ArrayXXf backward(ArrayXXf targets);
	float loss(ArrayXXf targets);
	
};