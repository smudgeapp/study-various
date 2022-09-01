#pragma once

#include <darknet.h>
#include <yolo_v2_class.hpp>


class DNet {
public:
	DNet();
	void setParams(std::string cfg, std::string weights);
	std::string getCfg();
	void initDetect(std::string filename);
	int x;
	int y;
	int w;
	int h;

private:	
	std::string cfg_file;
	std::string weights_file;
	std::string img_file;
	void detect();
	
	
	
	
};