const {contextBridge, ipcRenderer} = require("electron");

contextBridge.exposeInMainWorld("datatransfer", {
    send: (channel, data) => {
       // var validChannel = "fromHTML";
        //if (validChannel == channel) {
            ipcRenderer.send(channel, data);
        //}
    },
    receive: (channel, func) => {
        var validChannel = "toHTML";
        if (validChannel == channel) {
            ipcRenderer.on(channel, (event, ...args) => func(...args));
        }
    },
    dets: (channel, func) => {
        var validChannel = "passDets";
        if (validChannel == channel) {
            ipcRenderer.on(channel, (event, ...args) => func(...args));
        }
    },
    save: (channel, func) => {
        var validChannel = "saveComplete";
        if (validChannel == channel) {
            ipcRenderer.on(channel, (event, ...args) => func(...args));
        }
    }
});

