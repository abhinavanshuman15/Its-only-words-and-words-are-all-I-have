import pickle,gensim,random,sys

dataset_genre_wise = pickle.load(open('genre_wise_song_dataset.pickle','rb'))

opdataset_train = {}
opdataset_test = {}

did = sys.argv[1]
did = str(did)

i = 0

for genre in dataset_genre_wise:
	song_list = dataset_genre_wise[genre]
	random.shuffle(song_list)
	shuffled_song_list = song_list

	train_n = 1500

	for song in shuffled_song_list[:train_n]:
		trackId = song['trackId']
		artist = song['artist']
		lyrics = song['lyrics']
		
		opdataset_train[trackId] = {}
		opdataset_train[trackId]['artist'] = artist
		opdataset_train[trackId]['genre'] = genre
		opdataset_train[trackId]['lyrics'] = lyrics

	for song in shuffled_song_list[train_n:1888]:
		trackId = song['trackId']
		artist = song['artist']
		lyrics = song['lyrics']
		
		opdataset_test[trackId] = {}
		opdataset_test[trackId]['artist'] = artist
		opdataset_test[trackId]['genre'] = genre
		opdataset_test[trackId]['lyrics'] = lyrics

	i += 1
	print('genre :',i,end='\r')
temp_data=list(opdataset_train.keys())
random.shuffle(temp_data)
opdataset_train1 = {}

for track in temp_data:
	opdataset_train1[track]=opdataset_train[track]

abc=list(opdataset_test.keys())
random.shuffle(temp_data)
opdataset_test1 = {}
#random.shuffle(opdataset_test)
for track in abc:
	opdataset_test1[track]=opdataset_test[track]

pickle.dump(opdataset_train1,open('80_20_train_'+did+'.pickle','wb'))
pickle.dump(opdataset_test1,open('80_20_test_'+did+'.pickle','wb'))
