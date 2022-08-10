#pragma once

#include <iostream>
#include <random>
#include "DenseLayer.h"
#include "GlobalHelper.h"


class Dropout {
public:
	float rate;
	DenseLayer* layerM;
	ArrayXXf dropoutMask;
	ArrayXXf dropoutFwd;
	ArrayXXf dDropout;
	Dropout();
	Dropout(DenseLayer* layer, float dropoutRate);
	ArrayXXf forward(ArrayXXf inputVals);
	ArrayXXf backward(ArrayXXf dValues);
};