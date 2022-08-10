#pragma once



#include <Eigen/Core>

#include <iostream>
#include "WeightsBiasManager.h"


using namespace Eigen;

class DenseLayer {
public:
	Eigen::ArrayXXf wtMat;
	Eigen::ArrayXXf biasMat;
	Eigen::ArrayXXf forwardInput;
	ArrayXXf forwardOutput;
	Eigen::ArrayXXf dInput;
	Eigen::ArrayXXf dWeights;
	Eigen::ArrayXXf dBias;
	Eigen::ArrayXXf wtMomentum;
	Eigen::ArrayXXf biasMomentum;
	ArrayXXf wtCache;
	ArrayXXf biasCache;
	float wtRegLoss1 = -1.0;
	float wtRegLoss2 = -1.0;
	float biasRegLoss1 = -1.0;
	float biasRegLoss2 = -1.0;
	DenseLayer();
	DenseLayer(int rows, int cols, float wtReg1 = -1.0, float wtReg2 = -1.0, float biasReg1 = -1.0, float biasReg2 = -1.0);
	Eigen::ArrayXXf forward(Eigen::ArrayXXf inputMat);
	ArrayXXf backward(Eigen::ArrayXXf backInputMat);
	void regressionWtAdjustment(ArrayXXf wtAdjustment, bool colwise);
	


};
