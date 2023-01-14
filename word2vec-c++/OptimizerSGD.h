#pragma once

#include <Eigen/Core>

#include <iostream>
#include "GlobalHelper.h"
#include "DenseLayer.h"


using namespace Eigen;

//This includes all the different kinds of optimizers. Initially, it was supposed to be a single class for
//each optimizer, but since other optimizers are a variation on SGD, they were all combined into this class.

class OptimizerSGD {
public:
	const static int PLAINSGD = 1;
	const static int ADAGRAD = 2;
	const static int RMSPROP = 3;
	const static int ADAM = 4;
	float learningRate = 1.0f;
	float inputLR = 1.0f;
	float learningDecay = 0.0f;
	float momentum = 0.0f;
	float epsilon = 0.0f;
	float rho = 0.5f;
	float beta1 = 0.9f;
	float beta2 = 0.9f;
	int optType = 1;
	int iteration = 0;
	float udBeta1 = beta1;
	float udBeta2 = beta2;
	OptimizerSGD(float learning_rate = 1.0, float learning_decay = 0.0, float moment = 0.0, float epsilonIn = 0.0, float rhoIn = 0.5, float beta1In = 0.9, float beta2In = 0.9);
	void setOptimizer(int optimizertype = PLAINSGD);
	void updateLayer(ArrayXXf wtGradients, ArrayXXf biasGradients, DenseLayer &layer);
	void autoUpdateParams();
	void resetParams();
private:
	void plainSGD(ArrayXXf wtGradients, ArrayXXf biasGradients, DenseLayer& layer);
	void adaGrad(ArrayXXf wtGradients, ArrayXXf biasGradients, DenseLayer& layer);
	void rmsProp(ArrayXXf wtGradients, ArrayXXf biasGradients, DenseLayer& layer);
	void adam(ArrayXXf wtGradients, ArrayXXf biasGradients, DenseLayer& layer);
	


};
