#pragma once


#include "GlobalHelper.h"

GlobalHelper::GlobalHelper() {
	srand(time(0));
}

float GlobalHelper::getRandomFloat(int min, int max) {
	float rndNo = rand() % max + (min);
	
	float div = rand() % 10000 + (100);
	div = 100;
	return (float)rndNo / div;
}

float GlobalHelper::accuracy(ArrayXXf softmaxout, ArrayXi classes) {
	float accurateVals;	
	ArrayXXf smaxMax = argmax(softmaxout, 0);
	accurateVals = ((smaxMax.cast<int>() - classes) == 0).count();
	float accuracy = accurateVals / classes.size();
	return accuracy;
}