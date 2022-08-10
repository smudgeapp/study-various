#pragma once

#include <Eigen/Core>
#include "Loss.h"
#include <iostream>




class BinaryCrossEntropyLoss : public Loss {
private:
	ArrayXXf forward();
public:
	ArrayXXf fwdInput;
	ArrayXi fwdClasses;
	ArrayXXf fwdOutput;
	ArrayXXf dBinLoss;
	
	float calculate(ArrayXXf input, ArrayXi classes);
	void backward(ArrayXXf dinput);

};
