#pragma once

#include <Eigen/Core>


using namespace Eigen;


class ActivationLinear {
public:
	ArrayXXf fwdInputs;
	ArrayXXf fwdOutput;
	ArrayXXf dActLinear;

	ArrayXXf forward(ArrayXXf inputs);
	ArrayXXf backward(ArrayXXf dinputs);


};
