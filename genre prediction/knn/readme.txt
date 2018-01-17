create.py is used to create the vector embeddings for each songs using trained model.
pickle_to_CSV.py is used for converting embeddings from pickle to CSV format separately for train and test data.
top_K_sim_songs_extractor.py finds the id of k most similar songs for each songs in test.
knn_classification.py applies KNN algorithm on the similar songs to predict genre of a song.
f1_score_knn.py calculates f1 score.
