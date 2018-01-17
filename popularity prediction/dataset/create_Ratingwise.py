import pickle,random,sys

genre_name = sys.argv[2]
genre_name = str(genre_name)

dataset_rating_wise = pickle.load(open(genre_name+"_rating_list.pickle","rb"))

opdataset_train = {}
opdataset_test = {}

did = sys.argv[1]
did = str(did)


i = 0
count = {}

for rating in dataset_rating_wise:
	count[rating] = len(dataset_rating_wise[rating])
	print (rating,"  ",len(dataset_rating_wise[rating]))

for rating in dataset_rating_wise:
	
	song_list = dataset_rating_wise[rating]
	random.shuffle(song_list)
	shuffled_song_list = song_list

	n = len(shuffled_song_list)
	if rating == 4:
		n = count[1]+count[2]+count[3] - count[5]
	train_n = int((n*4)/5)
	if rating == 1 or rating == 2 or rating == 3:
		rating = 'Low'
	if rating == 4 or rating == 5:
		rating = 'High'

	for song in shuffled_song_list[0:train_n]:
		trackId = song['trackId']
		lyrics = song['lyrics']
		
		opdataset_train[trackId] = {}
		opdataset_train[trackId]['rating'] = rating
		opdataset_train[trackId]['lyrics'] = lyrics

	for song in shuffled_song_list[train_n:n]:
		trackId = song['trackId']
		lyrics = song['lyrics']
		opdataset_test[trackId] = {}
		opdataset_test[trackId]['rating'] = rating
		opdataset_test[trackId]['lyrics'] = lyrics

	i += 1
	print('rating :',i,end='\r')

temp_data=list(opdataset_train.keys())
random.shuffle(temp_data)
opdataset_train1 = {}
for track in temp_data:
	opdataset_train1[track]=opdataset_train[track]

test=list(opdataset_test.keys())
random.shuffle(test)
opdataset_test1 = {}
for track in test:
	opdataset_test1[track]=opdataset_test[track]


pickle.dump(opdataset_train1,open("80_20_"+genre_name+"_rating_train_"+did+".pickle" , "wb"))
pickle.dump(opdataset_test1,open("80_20_"+genre_name+"_rating_test_"+did+".pickle" , "wb"))

