#pragma once

#include <Eigen/Core>
#include <iostream>


using namespace Eigen;

class MeanAbsoluteError {
private:
	void forward();
public:
	ArrayXXf fwdInput;
	ArrayXXf fwdClasses;
	ArrayXXf fwdOutput;
	ArrayXXf dMeanAbsErr;
	float calculate(ArrayXXf inputs, ArrayXi classes);
	void backward(ArrayXXf dinputs);
};
