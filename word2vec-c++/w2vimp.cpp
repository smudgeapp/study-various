// w2vimp.cpp : This file contains the 'main' function. Program execution begins and ends there.
//


#include <iostream>
#include <list>
#include <vector>
#include <random>
#include <fstream>
#include <string>
#include <sstream>
#include <iterator>
#include <map>
#include <regex>

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

// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu

// Tips for Getting Started: 
//   1. Use the Solution Explorer window to add/manage files
//   2. Use the Team Explorer window to connect to source control
//   3. Use the Output window to see build output and other messages
//   4. Use the Error List window to view errors
//   5. Go to Project > Add New Item to create new code files, or Project > Add Existing Item to add existing code files to the project
//   6. In the future, to open this project again, go to File > Open > Project and select the .sln file
