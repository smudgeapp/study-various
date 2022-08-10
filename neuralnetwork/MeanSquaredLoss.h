#pragma once


#include <Eigen/Core>
#include <iostream>
#include "Loss.h"


using namespace Eigen;

class MeanSquaredLoss : public Loss{
private:
	void forward();
public:
	ArrayXXf fwdInput;
	ArrayXXf fwdClass;
	ArrayXXf fwdOutput;
	ArrayXXf dMeanSqLoss;
	float calculate(ArrayXXf input, ArrayXi classes);
	float calculateReg(ArrayXXf input, ArrayXXf classes);
	ArrayXXf backward(ArrayXXf dinput);

};