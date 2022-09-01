const { app, BrowserWindow, ipcMain } = require("electron");
const path = require("path");
const Net = require("./testc/index.js");
const fs = require("fs");
const https = require('https');
const Geodata = require('./geodata.js');
const accessToken = '[add mapbox access token]';



let geoCodeUri = 'https://api.mapbox.com/geocoding/v5/mapbox.places/';
let geoCodeUriAppend = '.json?access_token=' + accessToken;
let mNet = new Net();
let geoD = new Geodata(accessToken);
let mainWindow;


const loadMainWindow = () => {
    mainWindow = new BrowserWindow({
        width : 1200,
        height: 800,
        webPreferences: {
            nodeIntegration: true,
            preload: path.join(__dirname, "DataTransfer.js")
        }
    });
    
    
    mainWindow.loadFile(path.join(__dirname, "index.html"));   
	mainWindow.webContents.openDevTools();
	
}

app.on("ready", loadMainWindow);

mNet.addDetectionListener((dets) => {
  console.log("mnet listener");
  console.log(dets);
  mainWindow.webContents.send("passDets", dets);

});

ipcMain.on("fromHTML", (event, args) => {
  console.log("in Main - data rec");  
  var data = args;
  data = data.replace(/^data:image\/\w+;base64,/, '');
  //console.log(data);
  fs.writeFile("./testc/mapimages/img.png", data, {encoding: 'base64' }, (err) => {
  if (err) throw err;
    console.log("file saved");
    mNet.detect("./testc/mapimages/img.png");   
    });

});

ipcMain.on("detCenter", (event, args) => {
  //console.log("det center send event ");
  geoD.process(args);
  //TODO save process causing crash - try save in c++
  

  
});

geoD.onSaveComplete(() => {
  mainWindow.webContents.send("saveComplete", "completedSave");
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});

app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        loadMainWindow();
    }
});