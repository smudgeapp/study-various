// w2vimp.cpp : This file contains the 'main' function. Program execution begins and ends there.
//


#include <iostream>
#include <list>
#include <vector>
#include <random>
#include <string>
#include <iterator>
#include <map>

#include <Eigen/Core>

#include "DenseLayer.h"
#include "OptimizerSGD.h"
#include "SkipgramSoftmaxLoss.h"
#include "Word2Vec.h"

using namespace std;
using namespace Eigen;



int main()
{
    cout << "Hello World!\n";

    map<string, int> vocab;
    

    vector<vector<string>> sentences = { {"this", "is", "the", "first", "sentence"},
        {"this", "is", "the", "second", "sentence"},
        {"here", "is", "another", "sentence"},
        {"thats", "it", "final", "sentence"} };

    vector<vector<string>> sentences1 = { {"quick", "brown", "fox", "jumped", "over", "lazy", "rabbit"},
        {"cat", "loves", "play", "yarn"},
        {"dog", "likes", "bone"},
        {"dog", "loves", "bone"} };

    vector<vector<string>>::iterator itr;
    vector<string>::iterator in_itr;
    vector<string> sent = { "this", "is", "the", "first", "sentence" };

   
    Word2Vec w2v = Word2Vec(sentences1);
    w2v.trainSG();

   
    return 0;
   
}


