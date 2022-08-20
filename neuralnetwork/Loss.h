#pragma once

#include <Eigen/Core>

#include <list>
#include <vector>
#include "DenseLayer.h"

using namespace Eigen;

static class Loss {
public:
	virtual ~Loss() {};
	virtual float calculate(Eigen::ArrayXXf input, Eigen::ArrayXi classes) = 0;
	float regularizationLoss(std::vector<DenseLayer> layerList);
	

};
