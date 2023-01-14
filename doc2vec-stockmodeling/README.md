# DOC2VEC (gensim) for News Analysis to make Stock Predictions

Doc2Vec implementation for news analysis to make stock predictions is not new. There are numerous implementations for doing so, using various doc2vec libraries, other than gensim.

This particular implementation, extends the same concept to make a more generalized version that can be applied in a wider context than that limited by the initial training corpus.

*Naming convention in this readme was developed at the time of writing the readme, NOT the code, so the naming convention may not be reflected in the code. The convention was developed to promote ease-of-reading this readme only.*

## Basic Implementation of Doc2Vec for News Analysis to make Stock Predictions (= Basic Model)

The basic implementation is done as per the following steps.

1. Train model to obtain paragraph vectors for the desired corpus.
2. Generate a tagging of paragraphs (news item) against stock price indicator (price change, average change, moving average, etc.)
3. Run a logistic regression of the paragraph vectors against the stock price indicator.
4. Resultant output is an equation that takes paragraph vectors as inputs and outputs a stock price indicator.
5. Then new paragraph vectors can be *inferred* from the existing doc2vec model and input in the log-reg model to obtain stock price predictions.

## Generalization

Whereas under the Basic Model, the vector of a news item, to predict the preferred stock indicator, can be inferred by using a specific set of news only (i.e. paragraph vectors), **it would be more useful, if instead a set of factors could be identified that affect the particular stock as indicated through the news**.

In this case, then, the model would not be limited to a particular type of news - its paragraph vector as indicated by the doc2vec model, and the subsequent log-reg one. Instead, the predictions would be based on a set of factors that influence the stock price which, theoretically, should be more robust when making stock price predictions. 

Such a model would also make for a wider implementation, since the news items can vary by events, writer's style, editorial preferences, and a host of other factors. But the factors that affect a stock price can reasonably be expected to remain consistent across such variations.

For instance, in this particular implementation, oil and gas sector companies were selected. Then factors affecting PSO (Pakistan State Oil) could be oil prices, oil supply, refinery production, foreign exchange rates, dues of the company, dues against the company, taxes, petroleum policy and so on. These factors could be captured through words like oil, gas, receivables, dollar, federal, petroleum, policy and so on. While these words could be written by different writers in different sub-contexts, combinations, spellings and abbreviations, where a news item can be identified to pertain to a particular company, the key words can be expected to remain consistent.

## Hypothesis for Generalizing

Now then, if a vector could be obtained that represents all the key factors affecting the particular stock, and the inferred paragraph vectors, at prediction stage, could be measured against such representative vectors, then the model would not only be able to predict the stock indicator but also provide valuable information regarding what factors influenced the stock prediction.

## Implementation (= Generalized Stock Model)

This is divided into 6 basic steps. Items under each step can vary depending upon specific implementation.

1. Obtain trained vectors, for paragraphs and words, of a doc2vec model.
2. Develop vectors for factors that represent companies included in the corpus (= representative vectors).
3. Tag the paragraph vectors against the representative vectors.
4. Tag the representative vectors against stock indicators. 
5. Predict the representative vector from inferred vector.
6. Predict the stock indicator from representative vector.

For full details of the implementation refer to [IMPLEMENTATION](./IMPLEMENTATION.md) doc.

## [Test Results](./TESTRESULTS_JAN23.md)

Overall results remain inconclusive. Major impediment is getting past Step 3 & 4 as described in the [IMPLEMENTATION](./IMPLEMENTATION.md) doc. The result of similarity of representative vector to the paragraph vector shows little variation in the numerous iterations of the doc2vec model with an increasing number of epochs and varying window sizes. 

Epoch increments did not show improvement in the variation of the representative vector similarities, even at inference stage.

As a result, the current testing is stuck at Steps 3 & 4 and further implementation is not included in the code, as of yet.

What is, perhaps, most anomalous, is that the combined (=com) model inferences are returning more close to the desired output than the dbow and dm concatenated inferences. If there was just variation in com inference results, it could have been appropriated to random chance. But the results are also returning the target in more cases, which indicates, there is some sort of link. This has been observed in various training runs of the d2v models, with varying epochs, window sizes, etc. Furthermore, when simple dbow model is used, which is the type of the denoted com model, the results are similarly inconclusive to dbow and dm inference iterations. [See the last test under Discussion section.](./TESTRESULTS_JAN23.md)

However, the math behind the com inferences do not resolve with the definition of the doc2vec neural network. For model robustness, the neural network math must resolve, shouldn't it?

This requires further exploration. The results are left at this point, till further tests. 

## Instructions

Its plain Python code, just run it through terminal or IDLE. Get dependencies as applicable. Other references are included in the code.
