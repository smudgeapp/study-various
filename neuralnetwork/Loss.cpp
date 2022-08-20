#pragma once


#include "Loss.h"

float Loss::regularizationLoss(std::vector<DenseLayer> layerlist) {
	float regLoss = 0.0;

	for (int i = 0; i < layerlist.size(); i++) {
		DenseLayer layer = layerlist[i];
		//std::cout << "checking layer " << std::endl << layer.biasMat << std::endl;
		if (layer.wtRegLoss1 > 0) {
			regLoss += layer.wtRegLoss1 * layer.wtMat.abs().sum();
		}

		if (layer.wtRegLoss2 > 0) {
			regLoss += layer.wtRegLoss2 * layer.wtMat.square().sum();
		}

		if (layer.biasRegLoss1 > 0) {
			regLoss += layer.biasRegLoss1 * layer.biasMat.abs().sum();
		}

		if (layer.biasRegLoss2 > 0) {
			regLoss += layer.biasRegLoss2 * layer.biasMat.square().sum();
		}
	}

	return regLoss;
}

