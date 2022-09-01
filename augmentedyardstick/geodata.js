const fs = require('fs');
const https = require('https');
const { Worker, isMainThread, parentPort } = require('worker_threads');

class Geodata {
    #georesponse;
    #accessToken;
    #geoUri;
    #inputId = 0;
    #uriAppend;
    #saved = true;
    #saveCallback
    constructor(accessToken) {
        this.#georesponse = "./testc/mapimages/georesponse.json";
        this.#accessToken = accessToken;
        this.#geoUri = 'https://api.mapbox.com/geocoding/v5/mapbox.places/';
        this.#uriAppend = '.json?access_token=' + this.#accessToken;

    }

    #update(data) {
        var cds = data.coordinates;
        https.get(this.#geoUri + cds.lng + ',' + cds.lat + this.#uriAppend, (response) => {
            var recData = ""
            response.on('data', (data) => {
                //console.log(data);
                recData += data;
                 
            });
            
            
            response.on('end', async () => {
                   var processR = this.#processResponse(JSON.parse(recData));
                   var inList = [];
                        var newItem = {
                        id: this.#inputId,
                        coordinates: cds,
                        area: data.area,
                        poi: processR.poi,
                        city: processR.place,
                        province: processR.region
                    };
                    inList.push(newItem);
                    this.#saveThread(inList)
                    	   
            });
            
        });

    }

    #processResponse(response) {
        var poi = response.features[0].text;
        var place = response.features[1].text;
        var region = response.features[2].text;
        var processR = {
            poi: poi,
            place: place,
            region: region
        };
       // console.log("processR " + JSON.stringify(processR));
        return processR
        
    }

    #saveComplete() {
    	this.#saveCallback();
    }

    onSaveComplete(callback) {
        this.#saveCallback = callback;
    }

    
   #jsonStringAdj(inStr) {
   //	console.log(inStr);
   	//TODO catch syntax error and check for bracket
   	    var lastChar = inStr.charAt(inStr.length - 1);
    	var secondLastChar = inStr.charAt(inStr.length - 2);
    	if (secondLastChar == "]") {
   			var tmpArr = inStr.split('');
			tmpArr = tmpArr.slice(0, inStr.length - 1);
			inStr = tmpArr.join('');
			}
		else if (lastChar != "]") {
			inStr += "]";
		}
		
    
		return inStr;
    }
  

    #save(data) {
    	fs.exists(this.#georesponse, (exists) => {
            if (exists) {
                fs.readFile(this.#georesponse, (err, filedata) => {
                    if (err) throw err;
                    var exData = JSON.parse(this.#jsonStringAdj(filedata.toString()));
                    var idList = [];
                    for (const i of exData) {
                        idList.push(i.id);
                    }
                    var maxId = Math.max(...idList);
                    data[0].id = maxId + 1;                    
                    exData.push(data[0]);
                    var saveStr = "[";
					var exLen = exData.length;
					
					for (var j = 0; j < exData.length; j++) {
						var item = exData[j];
						if (j < exLen - 1) {
						    saveStr += JSON.stringify(item) + "," + "\n";
						}
						else {
							saveStr += JSON.stringify(item) + "\n";
						}
					
					}
					
					saveStr = this.#jsonStringAdj(saveStr);

                    fs.writeFile(this.#georesponse, saveStr, (err) => {
                             if (err) throw err;
                             

                        });                 
                    
                });
            }
            else {
            	
            	var inData = this.#jsonStringAdj(JSON.stringify(data));
                fs.writeFile(this.#georesponse, inData, (err) => {
                        if (err) throw err;
                        console.log("file first saved");
                        
                     });
            }
        });
        
    }

    #getMaxId() {
        var maxId = -1;
        fs.exists(this.#georesponse, (exists) => {
            if (exists) {
                fs.readFile(this.#georesponse, (err, filedata) => {
                    if (err) throw err;
                    var jsonData = JSON.parse(filedata);
                    console.log(jsonData)
                    var idList = [];
                    for (const i of jsonData) {
                        console.log(i);
                        idList.push(i.id);
                    }
                    maxId = Math.max(...idList);
                    console.log("max id " + maxId.toString());

                });
            }
        });
        return maxId;
    }

    

    process(data) {
        const geoProcess = async (inData) => {
           return new Promise((resolve, reject) => {
           const worker = new Worker("./geoupdate.js", { inData });

           worker.on('message', resolve => {
                this.#update(inData);
                });

           worker.on('error', reject => {
               console.log("save transaction could not be completed.");
                }); 

           worker.on('exit', (code) => {
               if (code != 0) {
                   console.log(new Error("save transaction stopped with ${code} exit code."));
               }
           });
          });

        }

        geoProcess(data).catch(err => console.error(err));
    }

    #saveThread(data) {
         const geoSave = (inData) => {
           return new Promise((resolve, reject) => {
           const worker = new Worker("./geosave.js", { inData });

           worker.on('message', resolve => {
                this.#save(inData);
                });

           worker.on('error', reject => {
               console.log("save transaction could not be completed.");
                }); 

           worker.on('exit', (code) => {
               if (code != 0) {
                   console.log(new Error("save transaction stopped with ${code} exit code."));
               }
               else {
               	this.#saveComplete();
               }
              
           });
          });

        }

        geoSave(data).catch(err => console.error(err));
    }


}

module.exports = Geodata;