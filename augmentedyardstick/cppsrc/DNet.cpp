#pragma once
#include "DNet.h"


DNet::DNet() {

}

void DNet::setParams(std::string cfg, std::string weights) {
	this->cfg_file = cfg;
	this->weights_file = weights;
	Detector newDet(cfg, weights);
	
	
}

std::string DNet::getCfg() {
	return cfg_file;
}

void DNet::initDetect(std::string filename) {
	this->img_file = filename;
	detect();
}

void DNet::detect() {
	Detector detNet(this->cfg_file, this->weights_file);
	std::vector<bbox_t> detections = detNet.detect(this->img_file);
	bbox_t dBox = detections[0];
	this->x = dBox.x;
	this->y = dBox.y;
	this->w = dBox.w;
	this->h = dBox.h;
}




