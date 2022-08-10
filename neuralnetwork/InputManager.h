#pragma once


#include <map>
#include <string>
#include <stdio.h>
#include <Eigen/Core>
#include "GlobalHelper.h"

//Convenience class for generating random input data.
//Also has the translation from Python to generate the spiral data set used in the book.

using namespace std;


class InputManager {
public:
	map<string, char> inputMap;
	Eigen::ArrayXXf inputMat;
	Eigen::ArrayXXf testSample;
	Eigen::ArrayXi classTestVals;
	InputManager();
	InputManager(map<string, char> inMap);
	void generateInput(int sample, int classes);
	void generateSpiralData(int samples, int classes, int dimensions);


	const string ROTATION = "rotation";
	const string CORNER = "corner";
	const string BOUNDARY = "boundary";
	const string SAMPLEVAL = "sampleval";
	const string SAMPLECLASS = "sampleclass";
	GlobalHelper gHelper;




}; 
