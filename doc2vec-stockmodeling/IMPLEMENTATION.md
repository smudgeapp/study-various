# IMPLEMENTATION 

#### TLSDR = too long, still do read ;)

## STEP 1: Obtain trained vectors, for paragraphs and words, of a doc2vec model

Gensim provides a quite easy-to-use implementation of doc2vec in python. This has been used in this implementation.

The corpus tags must include a date, the name of the company the article pertains to and the stock indicator. The model is required to predict the impact on a particular stock after a specific item of news pertaining to it was published. 

*Note: How much time will it take the impact of the news to be reflected in the stock indicator is a separate hypothesis in itself. But to briefly address the issue, for weak to semi-strong form efficient markets, (like Pakistan) it may take 2-3 days. For semi-strong to strong form efficient markets (like USA), the information may already be reflected in the stock at market opening or the same day. There is a critical qualifier to this generalization though. Where the stock is popular and attracts large trader interests, it wouldn't make much difference if the market is weak or strong form efficient. So circling back to the original assertion, the time for the impact to be reflected, is a separate area of study.*

*This means when including the stock indicator tag, it should be spaced from the publishing date of the news article such that the impact of the news is reflected in the indicator. Therefore, including the publishing date is important.*

There are certain important preprocessing considerations.

1. Since vectors (the representative vector) of key words (factors) have to be developed, it is important to eliminate all proper nouns from the corpus, other than the company name itself. Some proper nouns may still be relevant and depending upon specific company may have to be kept.

2. Company name may be spelled differently or different abbreviations may have been used. For instance, in the case of PSO, the name had variations, PSO, Pakistan State Oil and Pakistan State Oil Company in the news corpus. All such variations should be replaced with a common term. 

Other preprocessing pertains to general corpus preprocessing - removing numbers, punctuation, caps, etc.

### STEP 2: Develop Representative Vectors

Under the hypothesis of the Generalized Stock Model, vectors that represent key factors affecting the stock have to be developed. This is done by first obtaining nouns that appear in the target company name's context, and then obtain adjectives, verbs and adverbs that appear in the noun's context. That is, nouns would represent "what" factors affect the company and verbs, adjectives and adverbs would describe "how" that factor was affected, was it positive or negative. 

In order to achieve this, 

1. Obtain word similarity for the target company name.

*Note: Word similarity essentially shows words with similar features to the target word. For instance, PSO is a proper noun. So its similarity should return other company names with the highest value (cosine or other, depending on the simialirity measure). But as we move down this list, it will start to show words that most closely appear in the context of PSO. It is quite reasonable to assume that words that appear more closely in PSO's context, are the factors that affect its stock performance, since such words are related to items usually written in the context of company in the news corpus.* 
 
 2. The similarity words will contain nouns and verbs, so remove all from the similarity output EXCEPT nouns. These are the words that have appeared in the context of the target company name, and since these are nouns, they identify a class of things which are the (assumed and most likely) factors that affect the target company as per the news corpus.
 
 *Note: The "assumed and most likely" qualifier is applied because depending upon the news corpus, these words could have been written in different contexts. For instance, in the case of PSO, where the word 'spot' appears, it is referring to price, that is, 'spot price'. But that spot price could be of crude oil, or any one of the refined oils. At prediction stage the same word could be used in a different context than the one at the training stage. So, with a large number of factors, the affect of these outliers should, theoretically, be eliminated.*
 
 *Another concern is with words, that don't refer to a class of factors, rather are words that are describing an event, for instance 'the increase'. But with nltk 'parts-of-speech' = pos tagging, the one used during testing, and by regular rules of grammar, 'increase' would be categorized as a noun. Clearly, though, it is not a specific factor affecting the target company. Where such words appear, it is important to define its own context as well, which could be another noun. This would mean that representative vectors would have to be nested to some pre-defined level, i.e., nouns categorizing nouns, and then verbs, adverbs and adjectives describing those nouns.*
 
 *The final consideration is the window size used at training stage. If the window size is too large, it is possible that the context of the target company includes words further away from the target word and the similarity measure may not be shortlisting related factors. If the window size is too small, the model may get stuck in mid-tier nouns, like the word 'increase', referred in the para above.*
 
 3. Once the similarity nouns are obtained, run another similarity against each of the output nouns. Filter the noun's similarity output to include only verbs, adverbs and adjectives, as these parts of speech describe the action or the quality of the noun, positive or negative - these are the 'how' parts-of-speech = pos.
 
 *Note: There is an obvious issue in this step. While the 'how' pos can be assumed to be describing the noun, it cannot be reliably assumed that this description is in the context of the target word. For instance, the word 'cash' appears in PSO's similarity. When the 'how' pos is obtained for this noun, the pos could be describing the how of 'cash' in contexts other than PSO.* 
 
 *While the above problem is very real, its incidence does not seem to be significant. When comparing the obtained vector with the corpus, it is found that cash was appearing in the context of the target word and referring to liquidity issues. For instance, cash reserves, cash flow, cash dividends, etc. As a result, a more pertinent problem is that of 'cash' being a mid-tier noun rather than it being out of context.*
 
 *To address the above problem, similarity would be required between the three words, the target, the noun (=factor) and the pos describing the noun. This can be achieved using SVD by passing in the vectors of the 3 words. [For the math behind this solution refer to this post.](https://stats.stackexchange.com/questions/239059/similarity-metrics-for-more-than-two-vectors)*

*Another solution could be to run training for a limited corpus. That is where the target is PSO, the training corpus should include news articles only pertaining to PSO. Then it is less likely (not entirely) that the 'how' pos are out of context.*

4. The result is a set of words that begin with the target word, followed by a noun that describes what affects the target and a set of other pos words desribing how the noun was affected. This output can be used for the next step or it can be bifurcated by positive and negative words.

5. The bifurcation into positive and negative words is required only for the 'how' pos words, the first two words should remain similar in both. This bifurcation should also be valuable at prediction stage. Other than having a list of factors affecting the stock, the model would also reflect if the context was positive or negative. 

*Note: While it is valuable to have the positive or negative information, it adds another layer of test for the model's reliability. Now the accuracy measure would not just test predictions against the content of the article but also have to check if the positive vector returned a gain in the stock indicator. This imposes a stricter standard on the model.*

6. Finally, once the full formed factor representation is obtained, it can be passed to the doc2vec model to infer its *numeric* paragraph vector. 

## STEP 3 & 4: Tagging Representative Vectors to Paragraph Vectors to Stock Indicator

This will form the link between the inferred vector of the *new* news item and the representative vector. Now, the doc2vec model contains the weights for the paragraph vectors from the news corpus, not the representative vectors. So there must be first a link between the representative vectors and the paragraph vectors. But the paragraph vectors are not tagged to the representative vectors. 

1. In order to tag the representative vectors to the paragraph vectors, the similarity output can be obtained between each representative vector and the paragraph vectors in the doc2vec model. This would return a set of factors tagged against particular news and its subsequent impact on the stock price through the corpus tagging as noted in Step # 1.

The result is a set of representative vectors tagged to the paragraph vectors which are tagged to stock indicator. This would complete Steps 3 & 4. The representative vectors should now be tagged to the stock indicator.

*Note: When tagging the representative vectors against paragraph vector tags i.e. stock indicator, the stricter standard noted under Step 2 Point 5 is raised. If the vectors are not bifurcated into positive and negative, the accuracy would only have to measure, if the similarity output paragraph vector refers to a news item of the target company or not. Where vectors have been bifurcated into positive and negative though, the accuracy would also have to measure if a positive vector showed a positive gain in the stock indicator and vice versa.*

2. Once this output is received, it can be put into a log-reg model (paragraph vectors as input and representative vectors+tags from the similarity set as output) or just used as is.

*Note: If this implementation step seems make-shift or forced, consider the following. The purpose is to identify a set of factors', as reflected in a news item, effect on the stock indicator. The representative vector itself, does not carry that information. That information has to be obtained from the actual news item tags. Then if it can be identified which news item (i.e. its paragraph vector) reflects which representative vector, through the similarity measure, the factors most closely represented in the news item are identified. Once it is determined which news item reflects what factors, then the impact, on the stock indicator, of such news is the impact of the factors on the stock indicator.*

## STEP 5 & 6: Predict Stock Indicator from Representative Vector Predicted by Inferred Vector

At prediction stage, the inferred paragraph vector of the *new* news item will be passed to the output of Step 3 & 4. 

1. If a log-reg model has not been created for predicting the representative vector and their associated tags, a similarity measure may be used to obtained the most similar representative vector to the inferred vector for prediction.

2. If a log-reg model is created, the inferred vector may be passed as input to obtain the representative vector and associated tag prediction.

## Some Final Considerations

### Robustness

1. An apparent question is that since representative vector tags are derived from the original paragraph vectors, how do the representative vectors add to the model robustness, since they are just another similar vector. And the information carried in them is already held in the original paragraph vectors - it is actually derived from them. The inferred vector, then, could simply be passed to the doc2vec model similarity measure and the result would be a paragraph vector and its associated tag, the representative vector layer is just superficial.

Looking at Step 5 & 6 though, it is clarified that the prediction is actually based on the representative vector and not the paragraph vector. Note that the representative vector is also inferred from the doc2vec model. Even though its tags are derived from similarity, the word vector information carried in this representative vector is distinctly different from the original paragraph vector. The representative vector is a set of key words that are most closely represented in the paragraph vector. By the original definition of the paragraph vectors then, the representative vector carries the memory of the similar paragraph vector words as limited by the key words contained in the representative vector. So it is possible that the absolute value of the similarity measure is low, but for this purpose, it is only material to assess this value in relation to other representative vectors.

The inferred vector then, at prediction stage, is not assessing similarity to other paragraph vectors but rather the representative vector. As it follows from above, the prediction is the portion of the memory of the *new* news item (i.e. memory in the form of the inferred vector) that is limited by the key words contained in the representative vector.

There is then a direct link between the prediction and the representative vectors.

2. Notwithstanding Point 1 above, another approach could be to train the representative words in another doc2vec model. Then the inferred vector of *new* news item would be obtained from the weights of this new model and, theoretically, the subsequent similarity would be closely representative of the factors contained in the representative words used for training.

However, Steps 3 & 4 would still be required, to ascertain the impact of the representative words on the stock indicator. Note that the representative vectors themselves do not carry any information other than the one assigned to them.

### Model Parameters & Complexity

1. Following the process of developing representative vectors (Step 2) it can be seen that with large corpus, such a process could mean hundreds of such vectors. With a large number of such vectors, it may become difficult to shortlist to a manageable size. With a large number of vectors, it may also get difficult to assign each representative vector to a single paragraph vector and its associated stock indicator consequence. With the option to run training for news corpus of each company, the size problem quickly escalates to impractical (well infeasible, at least) levels.

Several tricks can possibly reduce this load, for instance, moving further away from the target words, the similarity measure gets worse. So a similarity measure range could short-list some items. Tagging words by pos also reduces the size significantly. When tagging against paragraph vectors, most similar or ranged similarity could be used. News corpus could be limited to sectors instead of companies.

2. Another problem is to decide how to create tagging using the similarity measure. Since the similarity measure would return similarity in descending order, it should simply be the largest value. But in cases where the corpus contains multiple companies, what if the highest value is of a company other than the one referred to by the representative vector. In this situation, should the representative vector be eliminated or should the next best option be used? Further what about the case where multiple representative vectors point to the same paragraph vector. Another layer of complexity is when bifurcated vectors do not point to the correct stock indicator consequence. 

While it should not be a problem if a single paragraph vector has multiple representative vectors, since different sets of factors could have a similar consequence. As long as there is sufficient variation in the similarity output, this should not be a bother. However, if the variation is minimal, for instance, the output keeps returning the same one or two paragraph vectors, then it cannot be said that a set of factors is effecting the stock indicator consequence, since there is next to no change from one vector to the other. 

*These issues are further discussed in the [TEST RESULTS](./TESTRESULTS.md) doc.*
