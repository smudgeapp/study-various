const { parentPort, WorkerData } = require('worker_threads');

parentPort.postMessage({ WorkerData });