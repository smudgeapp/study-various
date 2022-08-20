#pragma once


#include "InputManager.h"





InputManager::InputManager() {
	gHelper = GlobalHelper();

}

InputManager::InputManager(map<string, char> inMap) {
	gHelper = GlobalHelper();
	inputMap = inMap;
	map<string, char>::iterator it;
	int i = 0;
	inputMat(inputMap.size(), 3);
	for (it = inputMap.begin(); it != inputMap.end(); it++) {
		inputMat(i, 0) = inputMap.at(ROTATION);
		inputMat(i, 1) = inputMap.at(CORNER);
		inputMat(i, 2) = inputMap.at(BOUNDARY);
	}

}

void InputManager::generateInput(int sample, int classes) {

	auto classVar = [classes](float inVal) {
		int outVal = floor((inVal * (classes - 1)) + 1);
		return abs(outVal);
	};

	testSample = 4 * Eigen::ArrayXXf::Random(sample, 3);
	Eigen::ArrayXf classRands = Eigen::ArrayXf::Random(sample);
	classTestVals = classRands.unaryExpr(classVar);

}

//translation from Python to generate spiral data set
void InputManager::generateSpiralData(int samples, int classes, int dimensions) {
	ArrayXXf sampleVals = ArrayXXf::Zero((float)samples * classes, dimensions);
	ArrayXi classVals = ArrayXi::Zero((float)samples * classes, 1);
	srand((unsigned int)time(0));
	int j = 0;
	int innerloop = 0;
	for (int i = 0; i < classes; i++) {
		int p = samples;
		int q = dimensions;
		VectorXf r = VectorXf::LinSpaced(p, 0., 1.);
		VectorXf t = VectorXf::LinSpaced(p, (float)i * 4, (float)(i + 1) * 4);
		VectorXf random = VectorXf::Random(p) * 0.2;
		t = t + random;
		for (j = 0; j < p; j++) {
			sampleVals(innerloop, 0) = r(j) * sin(t(j));
			sampleVals(innerloop, 1) = r(j) * cos(t(j));
			classVals(innerloop, 0) = i;
			innerloop++;
		}

		this->testSample = sampleVals;
		this->classTestVals = classVals;

	}


}



