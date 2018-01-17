1.create.py is used to create the vector embeddings for each songs using trained model.
2.pickle_to_CSV.py is used for converting embeddings from pickle to CSV format separately for train and test data.
3.top_K_sim_songs_extractor.py finds the id of k most similar songs for each songs in test.
4.knn_classification.py applies KNN algorithm on the similar songs to predict genre of a song.
5.f1_score_knn.py calculates f1 score.
