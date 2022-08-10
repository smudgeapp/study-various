#pragma once


#include <Eigen/Core>


using namespace Eigen;

class ActivationSigmoid {
public:
	ArrayXXf fwdInput;
	ArrayXXf fwdOutput;
	ArrayXXf dSigmoid;
	void forward(ArrayXXf input);
	void backward(ArrayXXf dinput);


};
