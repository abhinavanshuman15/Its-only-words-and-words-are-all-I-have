# Its-only-words-and-words-are-all-I-have

## Description:
This project uses distributed representation of documents approach to perform music mining tasks. As part of music mining task we are working on two tasks: prediction of genre and prediction of popularity of English songs based on lyrics (NLP). Using distributed representation models we gets embedding for each songs as well as embedding of each genre and popularity class.
We use cosine-similarity between songs embedding as well as genre embedding to predict its genre. We also experimented with classical models like SVM, RandomForest, KNN using the generated songs embeddings.  

## Requirements:
1. Python 3.6
2. gensim 2.2.0
3. numpy 1.12.1
4. panda 0.20.1
5. scipy 0.19.0
6. scikit-learn 0.18.1

## Architecture:
Our architecture diagram is as below.

<p align="center">
  <img width="640" height="200" src="Architecture/docvec.png">
</p>
