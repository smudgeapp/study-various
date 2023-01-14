#pragma once

#include "Word2Vec.h"




Word2Vec::Word2Vec(vector<vector<string>> corpus, int featuresize, int windowsize, float learningRate, 
					float learningDecay, float momentum)  {
	this->helper = GlobalHelper();
	this->features = featuresize;
	this->windowsize = windowsize;
	this->learningRate = learningRate;
	this->learningDecay = learningDecay;
	this->momentum = momentum;
	this->corpus = corpus;
	this->windowsize = windowsize;
	createVocab();
	this->inputLayer = DenseLayer(this->vocab.size(), this->features);
	this->outputLayer = DenseLayer(this->features, this->vocab.size());
	this->sgSmax = SkipgramSoftmaxLoss();
	this->optimizer = OptimizerSGD(this->learningRate, this->learningDecay, this->momentum);	

}

void Word2Vec::train() {
	ArrayXXf hidden;
	ArrayXXf output;
	ArrayXXf smaxFwd;
	ArrayXXf smaxBwd;
	ArrayXXf otBwd;
	int itr = 0;
	float itrLoss = 0;
	while (this->loss > 1e-6) {
		setTrainingDataSGAllWords();
		hidden = this->inputLayer.forward(this->inputVec);
		output = this->outputLayer.forward(hidden);
		smaxFwd = this->sgSmax.forward(output, this->targetVecs);
		itrLoss += this->sgSmax.loss(this->targetVecs);
		smaxBwd = this->sgSmax.backward(this->targetVecs);
		otBwd = this->outputLayer.backwardW2V(smaxBwd.colwise().sum());
		this->inputLayer.backwardW2V(otBwd);
		this->optimizer.updateLayer(this->outputLayer.dWeightsW2V, this->outputLayer.dBiasW2V, this->outputLayer);
		this->optimizer.updateLayer(this->inputLayer.dWeightsW2V, this->inputLayer.dBiasW2V, this->inputLayer);
		this->optimizer.autoUpdateParams();
		if (this->epochEnd) {
			cout << "ITR = " << itr + 1 << endl;
			itr += 1;
			this->loss = itrLoss;
			cout << "Loss = " << this->loss << endl;
			cout << "Hidden:" << endl;
			cout << this->inputLayer.wtMat << endl;
			this->epochEnd = false;

		}
	}
}

void Word2Vec::trainSG() {
	ArrayXXf hidden;
	ArrayXXf output;
	ArrayXXf smaxFwd;
	ArrayXXf smaxBwd;
	ArrayXXf otBwd;
	int itr = 0;
	float itrLoss = 0;
	for (int i = 0; i < wordkeys.size(); i++) {
		string word = wordkeys[i];
		cout << "WORD TRAINING = " << word << endl;
		this->wordItr = 0;
		this->sentItr = 0;
		itr = 0;
		this->loss = 1000000;
		this->sgSmax = SkipgramSoftmaxLoss();
		this->optimizer.resetParams();
		float priorLoss = 0;
		bool stop = false;
		string cdn = "Nil";
		while(!stop) {
			if (setTrainingDataSGFwd(word)) {
				/*
				vector<int>::iterator twitr;
				for (twitr = this->trainwords.begin(); twitr != this->trainwords.end(); twitr++) {
					string word = this->wordkeys[*twitr];
					cout << "TARGET WORD = " << word << endl;
				}
				*/
				priorLoss = this->loss;
				//cout << "targets = " << this->targetVecs << endl;
				hidden = this->inputLayer.forward(this->inputVec);
				output = this->outputLayer.forward(hidden);
				smaxFwd = this->sgSmax.forward(output, this->targetVecs);
				itrLoss = this->sgSmax.loss(this->targetVecs);
				//cout << "loss one word = " << itrLoss << endl;
				smaxBwd = this->sgSmax.backward(this->targetVecs);
				otBwd = this->outputLayer.backwardW2V(smaxBwd);
				this->inputLayer.backwardW2V(otBwd);
				this->optimizer.updateLayer(this->outputLayer.dWeightsW2V, this->outputLayer.dBiasW2V, this->outputLayer);
				this->optimizer.updateLayer(this->inputLayer.dWeightsW2V, this->inputLayer.dBiasW2V, this->inputLayer);
				this->optimizer.autoUpdateParams();
				if (this->epochEnd) {
					itr += 1;
					this->loss = itrLoss;					
					//cout << "SMAX:" << endl;
					//cout << this->sgSmax.forwardOutput.colwise().sum() << endl;
					//cout << this->targetVecs << endl;
					this->epochEnd = false;
					if (this->loss <= 0) {
						stop = true;
						cdn = "loss";
					}
					if (this->optimizer.learningRate < 1e-7f) {
						stop = true;
						cdn = "learning rate";
					}
					if (itr >= this->epochs) {
						stop = true;
						cdn = "epochs";
					}
					if (priorLoss == this->loss) {
						//this->loss = 1e-7;
					}
					if (stop) {
						cout << "WORD # = " << i << endl;
						cout << "ITR = " << itr + 1 << endl;
						cout << "CURR. WORD = " << word << endl;
						cout << "LR = " << this->optimizer.learningRate << endl;
						cout << "Loss = " << this->loss << endl;
						cout << "Stop Condition = " << cdn << endl;
					}
				}
				
				
			}
		}
		cout << "hidden = " << endl << this->inputLayer.wtMat << endl;
		cout << "hidden bias = " << endl << this->inputLayer.biasMat << endl;
		cout << "output = " << endl << this->outputLayer.wtMat << endl;
		cout << "output bias = " << endl << this->outputLayer.biasMat << endl;
		

	}
}

void Word2Vec::createVocab() {	
	vector<vector<string>>::iterator oitr;
	vector<string>::iterator itr;
	vector<int> sentlen;
	int sentCount = 0;
	int wordCount = 0;	

	for (oitr = this->corpus.begin(); oitr != this->corpus.end(); oitr++) {
		vector<string> sent = *oitr;
		sentlen.push_back(sent.size());
		map<int, string> wordMap;
		for (itr = sent.begin(); itr != sent.end(); itr++) {
			string word = *itr;
			this->vocab[word] += 1;			
			wordMap[wordCount] = word;
			wordCount += 1;
			
		}
		this->totalWordCount += wordCount;
		wordCount = 0;
		this->corpusMap[sentCount] = wordMap;
		sentCount += 1;
	}

	this->totalSentCount = sentCount;
	
	int wordSerial = 0;
	map<string, int>::iterator vitr;
	for (vitr = this->vocab.begin(); vitr != this->vocab.end(); vitr++) {
		wordkeys[wordSerial] = vitr->first;
		cout << "key = " << wordSerial << ", word = " << vitr->first << endl;
		wordSerial += 1;
	}	

	this->totalVec = ArrayXXf::Zero(vocab.size(), vocab.size());
	//this->inputVec = ArrayXXf::Zero(vocab.size(), vocab.size());
	//this->targetVecs = ArrayXXf::Zero(vocab.size(), vocab.size());

	for (int i = 0; i < vocab.size(); i++) {
		string word = wordkeys[i];
		for (int j = 0; j < vocab.size(); j++) {
			if (word == wordkeys[j]) {
				this->totalVec(i, j) = 1;
				break;
			}
		}
	}
	auto maxlen = max_element(begin(sentlen), end(sentlen));
	
	if (this->windowsize > *maxlen) {
		this->windowsize = *maxlen;
	}

	

}


void Word2Vec::setTrainingDataSGAllWords() {
	ArrayXXf targets = ArrayXXf::Zero((int) this->windowsize * 2, this->totalVec.cols());
	
	map<int, string> sentence = this->corpusMap[this->sentItr];
	
	string word = sentence[this->wordItr];
	int wordkey = getWordSerial(word);
	this->inputVec = this->totalVec.row(wordkey);
	int bwditr = this->wordItr;
	if (this->wordItr == 0) {
		bwditr = sentence.size();
	}
	int targetRow = 0;
		for (int j = 0; j < this->windowsize; j++) {
			string tword = sentence[bwditr - 1];
			int key = getWordSerial(tword);
			targets.row(targetRow) = this->totalVec.row(key);
			bwditr = bwditr - 1;
			targetRow += 1;
		}
	int fwditr = this->wordItr;
	if (this->wordItr == sentence.size() - 1) {
		fwditr = -1;
	}
	for (int j = 0; j < this->windowsize; j++) {
		string tword = sentence[fwditr + 1];
		int key = getWordSerial(tword);
		targets.row(targetRow) = this->totalVec.row(key);
		fwditr += 1;
		targetRow += 1;
		}
	//cout << "target = " << targets << endl;
	this->targetVecs = targets;

	if (this->wordItr == sentence.size() - 1) {
		this->wordItr = 0;
		this->sentItr += 1;
	}
	else {
		this->wordItr += 1;
	}
	if (this->sentItr == this->corpusMap.size() - 1) {
		this->epochEnd = true;
		this->sentItr = 0;
		this->wordItr = 0;
	}
	
}

bool Word2Vec::setTrainingDataSGBothSide(string trainword) {
	//this->inputVec = ArrayXXf::Zero(this->vocab.size(), this->vocab.size());
	//this->targetVecs = ArrayXXf::Zero(this->vocab.size(), this->vocab.size());
	bool wordfound = true;
	int wordkey = getWordSerial(trainword);
	this->inputVec = this->totalVec.row(wordkey);
	//TODO fix bwditr and fwditr within loop
	map<int, string> sentence = this->corpusMap[this->sentItr];
	//cout << "sentitr = " << this->sentItr << endl;
	string word = sentence[this->wordItr];
	ArrayXXf targets = ArrayXXf::Zero(this->windowsize * 2, this->totalVec.cols());
	if (word == trainword) {
		//cout << "word found" << endl;
		wordfound = true;
		int bwditr = this->wordItr;
		if (this->wordItr == 0) {
			bwditr = sentence.size();
		}
		int targetRow = 0;
		for (int j = 0; j < this->windowsize; j++) {
			string tword = sentence[bwditr - 1];
			int key = getWordSerial(tword);
			targets.row(targetRow) = this->totalVec.row(key);
			//this->targetVecs.row(key) = this->totalVec.row(key);
			bwditr = bwditr - 1;
			targetRow += 1;
		}
		int fwditr = this->wordItr;
		if (this->wordItr == sentence.size() - 1) {
			fwditr = -1;
		}
		for (int j = 0; j < this->windowsize; j++) {
			string tword = sentence[fwditr + 1];
			int key = getWordSerial(tword);
			targets.row(targetRow) = this->totalVec.row(key);
			//this->targetVecs.row(key) = this->totalVec.row(key);
			fwditr += 1;
			targetRow += 1;
		}
		//cout << "targets set" << endl;
		//cout << "targets " << targets << endl;
		this->targetVecs = targets;
		
	}
	else {
		wordfound = false;
		
	}

	if (this->wordItr == sentence.size() - 1) {
			this->sentItr += 1;
			this->wordItr = 0;
		}
	else {
		this->wordItr += 1;
	}

	if (this->sentItr == this->corpusMap.size()) {
		//cout << "epoch end condition = " << this->sentItr << " word found " << wordfound << endl;
		this->sentItr = 0;
		this->wordItr = 0;
		this->epochEnd = true;
	}
	

	
	return wordfound;
}

bool Word2Vec::setTrainingDataSGFwd(string trainword) {
	this->trainwords.clear();
	bool wordfound = true;
	int wordkey = getWordSerial(trainword);
	this->inputVec = this->totalVec.row(wordkey);
	map<int, string> sentence = this->corpusMap[this->sentItr];
	//cout << "sentitr = " << this->sentItr << endl;
	string word = sentence[this->wordItr];
	ArrayXXf targets = ArrayXXf::Zero(this->windowsize, this->totalVec.cols());
	if (word == trainword) {
		//cout << "word found" << endl;
		wordfound = true;
		
		int targetRow = 0;
		
		int fwditr = this->wordItr;
		
		for (int j = 0; j < this->windowsize; j++) {
			string tword;
			bool breakLoop = false;
			if (this->wordItr == sentence.size() - 1) {
				tword = sentence[fwditr - 1];
				fwditr -= 1;
				if (fwditr <= 0) {
					breakLoop = true;
				}
			}
			else {
				tword = sentence[fwditr + 1];
				fwditr += 1;
				if (fwditr >= sentence.size()) {
					breakLoop = true;
				}
			}
			//cout << "tword = " << tword << endl;
			int key = getWordSerial(tword);
			this->trainwords.push_back(key);
			targets.row(targetRow) = this->totalVec.row(key);
			//this->targetVecs.row(key) = this->totalVec.row(key);
			targetRow += 1;
			if (breakLoop) {
				break;
			}
		}
		//cout << "targets set" << endl;
		//cout << "targets " << targets << endl;
		this->targetVecs = targets;
		
	}
	else {
		wordfound = false;

	}

	if (this->wordItr == sentence.size() - 1) {
		this->sentItr += 1;
		this->wordItr = 0;
	}
	else {
		this->wordItr += 1;
	}

	if (this->sentItr == this->corpusMap.size()) {
		//cout << "epoch end condition = " << this->sentItr << " word found " << wordfound << endl;
		this->sentItr = 0;
		this->wordItr = 0;
		this->epochEnd = true;
	}



	return wordfound;
}

int Word2Vec::getWordSerial(string word) {
	int wordkey = 0;
	for (int i = 0; i < this->wordkeys.size(); i++) {
		if (this->wordkeys[i] == word) {
			wordkey = i;
			break;
		}
	}
	return wordkey;
}

void Word2Vec::saveWeights(string word) {
	this->hiddenWts[word] = this->inputLayer.wtMat;
	this->outputWts[word] = this->outputLayer.wtMat;

}


