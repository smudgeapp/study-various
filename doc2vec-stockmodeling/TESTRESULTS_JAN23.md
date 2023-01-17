# TEST RESULTS

The corpus contains data for 7 companies, total of 449 articles. Training was done over entire corpus but tests were run only for one of those companies, namely, Pakistan State Oil Company with ticker 'PSO'. 

## Doc2Vec Model

As recommended in the original paper (Le and Mikolov, 2014), better results can be obtained by combining the two types of models, Distributed Bag of Words (=dbow) and Distributed Memory (=dm). 

Custom method for combining the two models is included in the code, which concatenates the paragraph vectors and the word vectors of the two models. This is then stored in a third model (=com for combined) which is just a holder of the requisite data for running similarities. 

The com model vector size definition is twice that of dbow or dm, and obviously dbow and dm vector size are equal. 

At inference stage, the vector is inferred similar to gensim's implementation, that is concatenation of the inferred vector obtained from dbow and dm models. 

Just for testing sake, the com model can also be trained to get weights and then used for running inference after the paragraph and word vectors have been replaced with the dbow and dm model vectors. This obviously does not fit with the definition of the doc2vec neural network, since the com weights for the word vectors are entirely different from the dbow and dm models. So at inference stage the word vectors are from dbow and dm and the weights are from com model. However, the results say differently and therefore mandate a review, at least. 

## Representative Vector Construction - Top-Level

This is denoted with a 't'.

The following options of constructing representative vectors were tested.

1. Word sentences passed to the doc2vec models to infer their vector
2. Extracted vectors of each word in the word sentences which were then averaged or summed to obtain a single vector
3. Modified the original word sentences configuration from target-what-'all how', to a repeating sequence of target-what-how-target-what-how and so on.

In t1 and t3, the sentences were passed to the doc2vec model(s) for inference. This step is not required for vectors in t2, since they are already in numeric form. 

Inference was drawn by concatenating the vectors of dbow and dm models and as another option, only from the com model, denoted with a 'h'.

## Representative Vector Construction - Second-Level Modifications

In each of the above options, the following modifications were done to arrive at the final vector forming a test iteration in itself (as also described in the [IMPLEMENTATION](./IMPLEMENTATION.md) doc.

1. **Plain Sentences:** The direct vector obtained from the sim of the sim of the target word. 
2. **Polar Sentences:** The plain sentences were bifurcated by positive and negative part-of-speech polarity obtained using nltk 'Sentiment Intensity Analyzer'.
3. **Coed Polar Sentences:** The polar sentences where words are filtered by the coefficient of determination between the target, what and how word for each how word. The coed is obtained using SVD. [Refer to this post for the math behind it.](https://stats.stackexchange.com/questions/239059/similarity-metrics-for-more-than-two-vectors)

## Results

Overall results remain inconclusive. Major impediment is getting past Step 3 & 4 as described in the [IMPLEMENTATION](./IMPLEMENTATION.md) doc. The result of similarity of representative vector to the paragraph vector shows little variation in the numerous iterations of the doc2vec model with an increasing number of epochs and varying window sizes. 

Epoch increments did not show improvement in the variation of the representative vector similarities, even at inference stage.

As a result, the current testing is stuck at Steps 3 & 4 and further implementation is not included in the code, as of yet.

What is, perhaps, most anomalous, is that the com model inferences are returning more close to the desired output than the dbow and dm inferences. If there was just variation in com inference results, it could have been appropriated to random chance. But the results are also returning the target in more cases, which indicates, there is some sort of link. This has been observed in various training runs of the d2v models, with varying epochs, window sizes, etc. Furthermore, when simple dbow model is used, which is the type of the denoted com model, the results are similarly inconclusive to dbow and dm inference iterations. *See the last test under Discussion section.*

However, the math behind the com inferences do not resolve with the definition of the doc2vec neural network. For model robustness, the neural network math must resolve, shouldn't it?

This requires further exploration. The results are left at this point, till further tests. 

## Discussion

### Top-Level 1

This is the basic construction of representative vectors where the target word sims are used to obtain nouns, then each noun sim is used to obtain its related quality. This is then passed to the second level to modify the plain sentence to polar sentences and coed polar sentences.

#### Modification 1 -> t1m1 -> [Sentences](./plain_sents_t1m1.txt)

##### DBOW & DM Inference -> [Results](./plain_res_t1m1.txt)

Notice there is a wide variation in the sentences but no variation in the resultant similarities. This means that the inferred paragraph vector for all the representative vectors is hovering around the same values. As to the why of this is happening, it must have to do with the calculations at the inference stage. According to Mikolov, weights and softmax variables are constant at inference stage, then a wide variation in the words and their combinations should have yielded significantly different values for each representative vector, but the same does not appear to be happening.

##### COM Inference -> [Results](./plain_res_t1m1_h.txt)

There is no variation in the results, again. But interestingly, representative vectors seem to be returning the target in every case. 

#### Modification 2 -> t1m2 -> [Sentences](./polar_sents_t1m2.txt)

##### DBOW & DM Inference -> [Results](./polar_res_t1m2.txt)

Here again the similarity results are hardly any different except for in one case. There is no way the positive and negative representative vectors could have been same. It may be that the vector size (i.e. sentence length) is too small and it is stuck at a minimum, but the result is the same as in t1m1 where the vector size was anything but small.

##### COM Inference -> [Results](./polar_res_t1m2_h.txt)

In this case, not only is there no variation, there is no variation between positive and negative vectors as well. It continues to return the target in every case.

#### Modification 3 -> t1m3 -> [Sentences](./coed_sents_t1m3.txt) 

##### DBOW & DM Inference -> [Results](./coed_res_t1m3.txt)

Theoretically, there should be little difference in the polar and coed polar sentences. The selection of words is expected to remain the same, but the sequence can change depending on the coed ranks.

##### COM Inference -> [Results](./coed_res_t1m3_h.txt)

Same as in m2 modifications.

### Top-Level 2

There is an established practice of concatenation and averaging or summing the word vectors. Le & Mikolov, in the original doc2vec paper, also refer to averaging the numeric vectors. There is no argument that averaging the vector is distinctly different from inferring it through the doc2vec model. The entire premise of the paragraph vector is that it stands as a store of memory of all the words in that paragraph. It is not simply the sum of the word vectors, instead, it is a standalone vector that acts upon the loss function in combination with the word vectors. At the backpropragation stage, the two are separated and then optimized severally. But since their action on the loss function can be applied through concatenation, summing or averaging operations, then where averaging or summing operations are performed, the paragraph vector could be expressed in some form as a function of the average or sum of the word vectors. 

While that function is not defined in this implementation, but since there is a link, it should reflect some weak similarity.

This requires further exploration and, as of now, even though the results show desired output, they cannot be relied upon.

The sentences in each case are the same as in Top-Level 1, but they are not included here since the actual construction is a numeric vector, not words.

#### Modification 1 -> t2m1 -> [Results](./plain_res_t2m1.txt)

We see a wide variation, some results are similar as expected, but most are varied.

#### Modification 2 -> t2m2 -> [Results](./polar_res_t2m2.txt)

Surprisingly, the results in this case are not varying by as much as in plain sentences. There is some variation which might turn into more variation with a larger number of representative vectors. But for the limited number of examples in this case, the variation is not significant. Further, where the positive sentiment is returning the target tag, the stock indicator is negative and vice versa for negative sentiment.

#### Modification 3 -> t2m3 -> [Results](./coed_res_t2m3.txt)

Results are pretty much the same as in t2m2.

### Top-Level 3

From the low variation above and the vectors not hitting the target, there is an apparent issue with the construction of the representative vector. Not returning the target tag could be because the target word is not well-represented in the representative vector. Another issue is that, since the idea is to shortlist factors, at inference stage when the window moves over the target vector, it will automatically move out of the context of the target word and its 'what word'. Then a repeating sequence of target-what-how should arguably resolve that issue. This is tested in this iteration.

#### Modification 1 -> t3m1 -> [Sentences](./plain_sents_t3m1.txt)

##### DBOW & DM Inference -> [Results](./plain_res_t3m1.txt)

Notice now that the sentence is much larger than in previous iterations (t1 and t2). However, there is no difference in the results, it keeps returning the same 2 or 3 paras again and again.

##### COM Inference -> [Results](./plain_res_t3m1_h.txt)

The results now are strikingly close to the desired output. Notice that there is variation and the target is returned in more cases.

#### Modification 2 -> t3m2 -> [Sentences](./polar_sents_t3m2.txt)

##### DBOW & DM Inference -> [Results](./polar_res_t3m2.txt)

There is no difference in results than the previous attempts.

##### COM Inference -> [Results](./polar_res_t3m2_h.txt)

In this case the variation is maintained and the target is returned in more cases. But notice that there is little variation between positive and negative sentiments and the stock prediction is also inaccurate.

#### Modification 3 -> t3m3 -> [Sentences](./coed_sents_t3m3.txt)

##### DBOW & DM Inference -> [Results](./coed_res_t3m3.txt)

Same result as t3m2, in this iteration.

##### COM Inference -> [Results](./coed_res_t3m3_h.txt) -> **EUREKA**

The results are pretty much the same as in the previous iteration with COM Inference (=t3m2_h). But notice Sentiment # 13 - *hanging by a thread here!* - it is exactly what is desired. 

The representative vector # 13 in the coed t3m3 sentences (linked above) shows the what word = 'tariff'. This word is not found in any of the tagged articles (article # 45 and 109 in the [corpus](./final_cor.json), count difference is due to corpus starting at 1 and list starting at 0) in the results referred above. However, the articles do reflect the sentiment of the representative vectors. But without representation of the keyword of the representative vector in the article, the result may be spurious. 

A further review of the corpus showed that the word 'tariff' was indeed used instead of prices in some cases or used along with 'price', which is what the tagged articles referred to. Knowing from local market context though, the word 'tariff' is more appropriately referring to electricity or power tariffs rather than oil product prices, but the latter usage has occured at other places in the corpus. Similarity output of 'tariff' is also included below. Notice 'prices' ranks well below the closest similarity with a 0.108 value - *a bit of a stretch to be assuming tariff to mean prices*. 

*('longterm', 0.19426275789737701), ('nrl', 0.17534714937210083), ('side', 0.17302948236465454), ('legal', 0.16806122660636902), ('hubc', 0.16394047439098358), ('approved', 0.16013264656066895), ('moreover', 0.14411970973014832), ('reduction', 0.13753478229045868), ('areas', 0.13250970840454102), ('balance', 0.12658251821994781), ('way', 0.1254926472902298), ('world', 0.12494612485170364), ('pso', 0.12324541807174683), ('cargo', 0.12316817045211792), ('electricity', 0.12174724787473679), ('analysis', 0.11986259371042252), ('take', 0.1186106950044632), ('authorities', 0.11523223668336868), ('audit', 0.11519815772771835), ('units', 0.11501447856426239), ('given', 0.11372625827789307), ('strategic', 0.11033876985311508), ('prices', 0.10796241462230682), ('income', 0.10787000507116318), ('industry', 0.1072005107998848), ('buying', 0.10657591372728348), ('project', 0.10639717429876328), ('year', 0.1055941954255104), ('availability', 0.10542090237140656), ('such', 0.10342872142791748), ('due', 0.1023109033703804), ('make', 0.10197199136018753), ('not', 0.1010182648897171), ('get', 0.1007743626832962), ('shares', 0.10015401989221573), ('companies', 0.09947503358125687), ('improve', 0.09939855337142944), ('large', 0.09881886094808578), ('growth', 0.09843935072422028), ('notice', 0.09719810634851456), ('level', 0.09688393026590347), ('refinery', 0.09606178104877472), ('condensate', 0.09454871714115143), ('key', 0.09434084594249725), ('fuel', 0.09336520731449127), ('estimates', 0.09309454262256622), ('services', 0.09222614765167236), ('cabinet', 0.09186358004808426), ('down', 0.09024740010499954), ('court', 0.09016848355531693)*

