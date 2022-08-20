#pragma once

#include "WeightsBiasManager.h"

WeightsBiasManager::WeightsBiasManager() {
	gHelper = GlobalHelper();
}


Eigen::ArrayXXf WeightsBiasManager::getWeights(int inputs, int neurons) {
	//this is according to no. of neurons and then for each feature in the neuron
	//instead of transpose at the time of output forward, shape is set at this stage. Each column x row is the weight for a single neuron's each feature/input
	Eigen::ArrayXXf wts(inputs, neurons);
	for (int i = 0; i < inputs; i++) {
		for (int j = 0; j < neurons; j++) {
			float rndNo = gHelper.getRandomFloat(-10, 201);
			wts(i, j) = rndNo;
			
		}
	}

	return wts;

}


Eigen::ArrayXXf WeightsBiasManager::getBias(int neurons) {
	//this is according to no. of neurons - each set of wt outputs a single neuron output to which a single bias is applied
	//Eigen::ArrayXXf bias(1, neurons);
	//ArrayXXf bias = ArrayXXf::Zero(1, neurons);
	ArrayXXf bias = ArrayXXf::Zero(1, neurons);

	
	for (int i = 0; i < neurons; i++) {
		bias(0, i) = gHelper.getRandomFloat(100, 201);

	}
	

	return bias;
	
}

