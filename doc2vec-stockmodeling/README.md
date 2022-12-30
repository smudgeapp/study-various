# DOC2VEC (gensim) for News Analysis to make Stock Predictions

Doc2Vec implementation for news analysis to make stock predictions is not a novel idea. There are numerous implementations for doing so, using various doc2vec libraries, other than gensim.

This particular implementation, extends the same concept to make a more generalized version that can be applied in a wider context than that limited by the initial training corpus.

*Naming convention in this readme was developed at the time of writing the readme, NOT the code, so the naming convention may not be reflected in the code. The convention was developed to promote ease-of-reading this readme only.*

## Basic Implementation of Doc2Vec for News Analysis to make Stock Predictions (= Basic Model)

The basic implementation is done as per the following steps.

1. Train model to obtain paragraph vectors for the desired corpus.
2. Generate a tagging of paragraphs (news item) against stock price indicator (price change, average change, moving average, etc.)
3. Run a logistic regression of the paragraph vectors against the stock price indicator.
4. **Resultant** output is an equation that takes paragraph vectors as inputs and outputs a stock price indicator.
5. Then new paragraph vectors can be *inferred* from the existing doc2vec model and input in the log-reg model to obtain stock price predictions.

## Generalization

Whereas under the provided scheme we can only infer the, preferred, stock indicator from a specific set of news (i.e. paragraph vectors), **it would be more useful, if instead we could identify a set of factors that affect the particular stock as indicated through the news**.

In this case, then, we would not be limited to a particular type of news and its paragraph vector as indicated by the doc2vec model, and the subsequent log-reg one. Instead, we would have a set of factors that influence the stock price which, theoretically, should be more robust when making stock price predictions. 

Such a model would also make for a wider implementation, since the news items can vary by events, writer's style, editorial preferences, and a host of other factors. But the factors that affect a stock price can reasonably be expected to remain consistent across such variations.

For instance, in this particular implementation, oil and gas sector companies were selected. Then factors affecting PSO (Pakistan State Oil) could be oil prices, oil supply, refinery production, foreign exchange rates, dues of the company, dues against the company, taxes, petroleum poicy and so on. These factors could be captured through words like oil, gas, receivables, dollar, federal, petroleum, policy and so on. While these words could be written by different writers in different sub-contexts, combinations, spellings and abbreviations, where we can identify a news item to pertain to a particular company, the key words can be expected to remain consistent.

## Hypothesis for Generalizing

Now then, if we could obtain a vector that represents all the key factors affecting the particular stock, and our inferred paragraph vectors, at prediction stage, could be measured against such representative vectors, then the model would not only be able to predict the stock indicator but also provide valuable information regarding what factors influenced the stock prediction.

## Implementation (= Generalized Stock Model)

This is divided into 6 basic steps. Items under each step can vary depending upon specific implementation.

1. Obtain trained vectors, for paragraphs and words, of a doc2vec model.
2. Develop vectors for factors that represent companies included in the corpus (= representative vectors).
3. Tag the paragraph vectors against the representative vectors.
4. Tag the representative vectors against stock indicators. 
5. Predict the representative vector from inferred vector.
6. Predict the stock indicator from representative vector.

### STEP 1: Obtain trained vectors, for paragraphs and words, of a doc2vec model

Gensim provides a quite easy-to-use implementation of doc2vec in python. This has been used in this implementation.

There are certain important preprocessing considerations.

1. Since we are going to develop vectors (the representative vector) of key words (factors), it is important to eliminate all proper nouns from the corpus, other than the company name itself. Some proper nouns may still be relevant and depending upon specific company may have to be kept.
2. Company name may be spelled differently or different abbreviations may have been used. For instance, in the case of PSO, the name had variations, PSO, Pakistan State Oil and Pakistan State Oil Company. All such variations had to be replaced with a common term. 

Other preprocessing pertains to general corpus preprocessing, removing numbers, punctuation, caps, etc.

### STEP 2: Develop Representative Vectors

From above, we now know that we have to develop vectors that represent key factors affecting the stock. We do this by first obtaining nouns that appear in the target company name's context, and then obtain adjectives, verbs and adverbs that appear in the noun's context. That is, nouns would represent "what" factors affect the company and verbs, adjectives and adverbs would describe "how" that factor was affected, was it positive or negative. 

In order to achieve this, 

1. Obtain word similarity for the target company name.

*Note: Word similarity essentially shows words with similar features to the target word. For instance, PSO is a proper noun. So its similarity should return other company names with the highest value (cosine or other, depending on the simialirity measure). But as we move down this list, it will start to show words that most closely appear in the context of PSO. It is quite reasonable to assume that words that appear more closely in PSO's context, are the factors that affect its stock performance, since such words are related to items usually written in the context of company in the news corpus.* 
 
 2. The similarity words will contain nouns and verbs 