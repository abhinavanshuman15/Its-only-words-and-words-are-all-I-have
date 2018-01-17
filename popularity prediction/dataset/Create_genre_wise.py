import pickle,random,sys,os

dataset_rating_wise = pickle.load(open("rating_wise_song_list_with_genre.pickle","rb"))

opdataset = {}


did = sys.argv[1]
did = str(did)

i = 0

genre_list = ['Metal','Country','Religious','Rap','R&B','Reggae']
count ={}
genre = {}
for rating in dataset_rating_wise:
	song_list = dataset_rating_wise[rating]
	for song in song_list:
		if song['genre'] not in genre:
			genre[song['genre']] = 0
		
print(genre)
for genre in genre_list:
	count[genre]={1:0,2:0,3:0,4:0,5:0}
	if genre not in opdataset:
		opdataset[genre]= {}
	for rating in dataset_rating_wise:
		opdataset[genre][rating] = []
		song_list = dataset_rating_wise[rating]
		for song in song_list:
			if song['genre']==genre:
				count[genre][rating] += 1
				opdataset[genre][rating].append(song)
		print (rating,"  ",len(dataset_rating_wise[rating]))

print(count)

for genre in opdataset:
	print(genre,len(opdataset[genre]))
	try:
    		os.stat(genre_name)
	except:
    		os.mkdir(genre_name) 
	pickle.dump(opdataset[genre],open(genre_name+"_rating_list.pickle","wb"))

