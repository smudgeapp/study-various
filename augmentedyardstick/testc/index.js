const testC = require('[path to node addon]');


class Net {
	constructor() {
		const addC = testC;
		this.cfg_file = "[path to config file]";
	    this.weights_file = "[path to trained weights]";
		this.dNet = new addC.DWrap();
	    this.dNet.loadParams(this.cfg_file, this.weights_file);
	    	    
	}

	detect(imgFile) {
		var objDets = this.dNet.detect(imgFile);
		return objDets;
	}

	
    addDetectionListener(callback) {
       	this.dNet.onDetections(callback);
    }
  

}

module.exports = Net;










