#pragma once


#include "GlobalHelper.h"

GlobalHelper::GlobalHelper() {
	srand(time(0));
}

float GlobalHelper::getRandomFloat(int min, int max) {
	int rndNo = rand() % max + (min);
	
	return (float)rndNo / 100;
}

float GlobalHelper::accuracy(ArrayXXf softmaxout, ArrayXi classes) {
	float accurateVals;	
	ArrayXXf smaxMax = argmax(softmaxout, 0);
	accurateVals = ((smaxMax.cast<int>() - classes) == 0).count();
	float accuracy = accurateVals / classes.size();
	return accuracy;
}