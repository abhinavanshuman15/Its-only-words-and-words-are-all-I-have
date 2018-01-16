import pickle,sys,gensim,operator
import logging,os

program = os.path.basename(sys.argv[0])
logger = logging.getLogger(program)

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
logging.root.setLevel(level=logging.INFO)
logger.info("running %s" % ' '.join(sys.argv))


did = sys.argv[2]
did = str(did)

intid_2_trackid = pickle.load(open('../intId_2_trackId.pickle','rb'))

k = int(sys.argv[1])

f = open('top_50_similar_songs_'+did+'.txt','r')

dataset = pickle.load(open('song_vectors_for_genre_dataset_'+did+'.pickle','rb'))
train_dataset = dataset['train']
test_dataset = dataset['test']

test_dataset = pickle.load(open('../dataset/80_20_test_'+did+'.pickle','rb'))
train_dataset = pickle.load(open('../dataset/80_20_train_'+did+'.pickle','rb'))

dataset = {}
for trackID in train_dataset:
	dataset[trackID]= {}
	dataset[trackID]=train_dataset[trackID]
for trackID in test_dataset:
	dataset[trackID]= {}
	dataset[trackID]=test_dataset[trackID]


genre_list = ['Metal','Country','Religious','Rap','R&B','Reggae']

conf_mat = {}

correct = 0
i = 0

logger.info("Start")
for genre in genre_list:
	conf_mat[genre] = {}

for genre in conf_mat:
	for genre_1 in conf_mat:
		conf_mat[genre][genre_1] = 0

for line in f:
	songId, tmp = line.split('=>')
	cur_trackId = intid_2_trackid[int(songId)]

	tmp = tmp.split(',')
	similar_songs = []
	for t in tmp:
		try:
			song,sim = t.split(':')
			similar_songs.append( (intid_2_trackid[int(song)], float(sim)) )
		except ValueError:
			pass

	sim_dict = {}
	for x in range(k):
		sim_trackId = similar_songs[x][0]
		sim_genre = dataset[sim_trackId]['genre']

		if sim_genre not in sim_dict:
			sim_dict[sim_genre] = 0

		sim_dict[sim_genre] += similar_songs[x][1]

	
	sorted_sim_dict = sorted(sim_dict.items(), key=operator.itemgetter(1), reverse=True)
	predicted_genre = sorted_sim_dict[0][0]
	actual_genre = dataset[cur_trackId]['genre']
	if predicted_genre == actual_genre:
		correct += 1
	
	conf_mat[actual_genre][predicted_genre] += 1

	i += 1
	print(i,end='\r')

print("Accuracy :",correct/i)
pickle.dump(conf_mat,open('confusion_matrix/conf_mat_genre_knn_'+str(k)+'_'+did+'.pickle','wb'))

logger.info("Done")

