#pragma once


// main.cpp : This file contains the 'main' function. Program execution begins and ends there.
//




#include <iostream>
#include <list>
#include <vector>
#include <random>
#include <fstream>
#include <string>
#include <sstream>
#include <iterator>

#include <Eigen/Core>

#include "InputManager.h"
#include "WeightsBiasManager.h"
#include "DenseLayer.h"
#include "ActivationReLU.h"
#include "ActivationSoftmax.h"
#include "CategoricalCrossEntropy_Loss.h"
#include "GlobalHelper.h"
#include "SoftmaxLoss.h"
#include "OptimizerSGD.h"
#include "Dropout.h"
#include "BinaryCrossEntropyLoss.h"
#include "ActivationSigmoid.h"
#include "MeanSquaredLoss.h"
#include "RegressionModel.h"



using namespace Eigen;
using namespace std;


//helper function to get data from csv file
vector<vector<string>> getCSVData(string filename) {    
    vector<vector<string>> content;
    vector<string> row;
    string line, word;

    fstream file(filename, ios::in);
    if (file.is_open()) {
        while (getline(file, line)) {
            row.clear();
            stringstream str(line);
            while (getline(str, word, ',')) {
                row.push_back(word);
                //cout << "word: " << word << endl;

            }
            content.push_back(row);
            //cout << "outside inner while" << endl;
        }
    }
    else {
        cout << "Could not open file." << endl;
    }
    return content;
}

int main()
{
    std::cout << "Hello World!\n";
   

    /* //************************remove this comment for regression model*****************
    
    //REGRESSION MODEL EXAMPLE - special model class using neural net component classes
    //similarly other models can be made using the component classes.
    // 
    //in this particular instance, the regression model is being used to project one-period forward tax revenues.
    //multiple taxes actual collection values are used over several years as the input. 16 taxes, 5 years
    //output is one-period forward actual value to train the model to project this value.
    //data set is obviously very small, but it is only for testing the code.

    string revcolfile = "[path of input file]";
    string gvacolfile = "[path of wt adjustment parameter file]";

    ArrayXXf inputdata(5, 16); //input array - tested on revenue data for five periods, with sixteen values in each period
    ArrayXXf outputdata(1, 16); //output is the immediate year after the input data - for instance input data ranged from FY16-20, then output data was FY21
    ArrayXXf gvaWtAdj(1, 6); //this is for adjusting input weights to account for impact of external factors influence

    vector<vector<string>> inData = getCSVData(revcolfile); //get data from csv file
    vector<vector<string>> gvaData = getCSVData(gvacolfile);
    

    //fill the arrays with data pulled from csv files.
    for (int i = 1; i < inData.size(); i++) {
        vector<string> row = inData[i];
        for (int j = 1; j < row.size(); j++) {
            if (i < inData.size() - 1) {
                inputdata(i - 1, j - 1) = atof(row[j].c_str());
            }
            else {
                outputdata(0, j - 1) = atof(row[j].c_str());
            }
        }
    }
    
    
    for (int i = 0; i < gvaData[1].size(); i++) {

        gvaWtAdj(0, i) = atof(gvaData[1][i].c_str());
    }
      

    //INIT

    //initiate regression model with no. of inputs, no. of outputs, hidden layers, input data and desired output data
    //For example, input data can be historic values and desired output can be one period forward actual values, then the model can be used for projections
    RegressionModel model = RegressionModel(16, 16, 1, inputdata, outputdata); 
    
    //model.adjustInputWeights(gvaWtAdj, false); //for adjusting input weights - see notes in class cpp file.

    //set optimizer paramters as a map
    map<string, float> optParams;
    optParams[model.learningRateId] = 0.005f;
    optParams[model.learningDecayId] = 1e-5f;
    optParams[model.momentId] = 0.05f;
    optParams[model.epsilonId] = 1e-7f;
    //optParams[model.rhoId] = 0.999f;
    optParams[model.betaId] = 0.99f;
    optParams[model.beta2Id] = 0.99f;
    model.setOptimizer(OptimizerSGD::ADAM, optParams); //set optimizer for the regression model
    model.train(); //train the model
    ArrayXXf fy16 = inputdata.row(0);
    model.validate(fy16); //validation method - in this case in sample data is being used since this is for testing, but normally out of training sample data is used for validation
    ArrayXXf fy19 = inputdata.row(3); 
    model.validate(fy19); //same as above
    
    */ //************************remove this comment for regression model*****************




    
    /* //************************remove this comment for generic model*****************
    // GENERIC MODEL EXAMPLE
    //INIT
    int layer1Out = 64;
    int layer2Out = 2;
    GlobalHelper helper = GlobalHelper(); //helper class with various functions
    vector<DenseLayer> layerList; //list to contain dense layers.
    InputManager inputMngr = InputManager(); //to generate random input for testing
    OptimizerSGD sgdOpt = OptimizerSGD(0.001, 5e-7, 0., 1e-7, 0., 0.999, 0.999); //setting up optimizer
    sgdOpt.setOptimizer(OptimizerSGD::ADAM); //setting type of optimizer
    inputMngr.generateSpiralData(5, 2, 2); //generated small spiral data for testing - 5 samples, 2 classes (no. of colors), 2 dimensions (x and y coordinates)
    DenseLayer layer1 = DenseLayer(2, layer1Out); //first layer with 2 classes
    layerList.push_back(layer1); //add layer1 to the layer list
    Dropout dOut1 = Dropout(&layer1, 0.1); //initiate the dropout layer    
    ActivationReLU actvFunc = ActivationReLU(); //initiate activation function - rectified linear
    DenseLayer layer2 = DenseLayer(layer1Out, layer2Out); //initiate denselayer 2 with input = output of layer 1 and output = 2
    layerList.push_back(layer2); //add layer 2 to layer list
    SoftmaxLoss smaxLoss = SoftmaxLoss(layerList); //initiate softmax loss - combined softmax activation and categorical cross entropy loss


    //activation sigmoid may be used instead of softmax. different loss variable is used with this activation.
    //respective class backward and forward functions have to be used
    // 
    //ActivationSigmoid sigActivation = ActivationSigmoid();
    //BinaryCrossEntropyLoss binLoss = BinaryCrossEntropyLoss();

    //MeanSquaredLoss mseLoss = MeanSquaredLoss();

           
    // FIRST FORWARD PASS
    Eigen::ArrayXXf layer1out = layer1.forward(inputMngr.testSample); // layer 1 forward
    Eigen::ArrayXXf actvlayer = actvFunc.forward(layer1out); //activation ReLU forward
    dOut1.forward(actvlayer); // dropout forward
    Eigen::ArrayXXf layer2out = layer2.forward(dOut1.dropoutFwd); //dropout output into layer 2    
    float combineLoss = smaxLoss.forward(layer2out, inputMngr.classTestVals); //final softmax activation and loss calculation
    

    //FIRST BACKWARD PASS    
    //backward pass in reverse order to the forward pass

    ArrayXXf smaxLossBack = smaxLoss.backward(); //loss to softmax backward   

    layer2.backward(smaxLossBack); //layer 2 backward
    dOut1.backward(layer2.dInput); //dropout backward
    ArrayXXf actvReluBack = actvFunc.backward(dOut1.dDropout); //actv relu backward
    layer1.backward(actvReluBack); //layer 1 backward

    //optimize weights and biases after complete iteration
    sgdOpt.updateLayer(layer1.dWeights, layer1.dBias, layer1);
    sgdOpt.updateLayer(layer2.dWeights, layer2.dBias, layer2);
    sgdOpt.autoUpdateParams();
    
   
    //calculate accuracy and print to console

    float accuracyVal = helper.accuracy(smaxLoss.softmaxOutput, inputMngr.classTestVals);
    std::cout << "accuracy " << endl << accuracyVal << endl;

    //loop through desired iterations of the model.

    int loopCount = 0;
    int printCount = -1;
    float prevLoss = combineLoss;
    int lossLim = 10;
    int lossConstant = 0;
    
    for (int i = 0; i < 10000; i++) {
        layer1out = layer1.forward(inputMngr.testSample);
        actvlayer = actvFunc.forward(layer1out);
        dOut1.forward(actvlayer);
        layer2out = layer2.forward(dOut1.dropoutFwd);       
        combineLoss = smaxLoss.forward(layer2out, inputMngr.classTestVals);        
        accuracyVal = helper.accuracy(smaxLoss.softmaxOutput, inputMngr.classTestVals);        
        smaxLossBack = smaxLoss.backward();
        layer2.backward(smaxLossBack);
        dOut1.backward(layer2.dInput);        
        actvReluBack = actvFunc.backward(dOut1.dDropout);
        layer1.backward(actvReluBack);
        sgdOpt.updateLayer(layer1.dWeights, layer1.dBias, layer1);
        sgdOpt.updateLayer(layer2.dWeights, layer2.dBias, layer2);
        sgdOpt.autoUpdateParams();        
        if (loopCount >= printCount) {
            printCount += 500;
            std::cout << "==================================" << endl;
            std::cout << "iteration = " << loopCount;
            //std::cout << "preReg lossVal = " << smaxLoss.mainLoss << endl;
            //std::cout << "lossVal = " << smaxlossVal << endl;
            //std::cout << "preReg lossVal = " << smaxLoss.mainLoss << endl;
            std::cout << ", lossVal = " << combineLoss;
            std::cout << ", accuracy = " << accuracyVal;
            std::cout << ", adam beta1 = " << sgdOpt.udBeta1;
            std::cout << ", adam beta2 = " << sgdOpt.udBeta2 << endl;;
        }
        loopCount += 1;
        if (prevLoss == combineLoss) {
            lossConstant += 1;
            if (lossConstant >= lossLim) {
                cout << "loss not changing.\n";
                printf("lossVal = %d, iteration = %d, accuracy = %d, ", combineLoss, loopCount, accuracyVal);
                break;
            }
            
        }
        prevLoss = combineLoss;
        
    }
    
  */    //************************remove this comment for generic model*****************

}

