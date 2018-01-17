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

genre_name = sys.argv[3]
genre_name = str(genre_name)

f = open(genre_name+'top_'+str(k)+'_similar_songs_'+did+'.txt','r')

dataset = pickle.load(open(genre_name+'song_vectors_dataset_'+did+'.pickle','rb'))
train_dataset = dataset['train']
test_dataset = dataset['test']

test_dataset = pickle.load(open('../dataset/80_20_'+genre_name+'_rating_test_'+did+'.pickle','rb'))
train_dataset = pickle.load(open('../dataset/80_20_'+genre_name+'_rating_train_'+did+'.pickle','rb'))

dataset = {}
for trackID in train_dataset:
	dataset[trackID]= {}
	dataset[trackID]=train_dataset[trackID]
for trackID in test_dataset:
	dataset[trackID]= {}
	dataset[trackID]=test_dataset[trackID]


type_list = ['Low','High']

conf_mat = {}

correct = 0
i = 0

logger.info("Start")
for rating in type_list:
	conf_mat[rating] = {}

for rating in conf_mat:
	for rating_1 in conf_mat:
		conf_mat[rating][rating_1] = 0

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
		sim_rating = dataset[sim_trackId]['rating']

		if sim_rating not in sim_dict:
			sim_dict[sim_rating] = 0

		sim_dict[sim_rating] += similar_songs[x][1]

	sorted_sim_dict = sorted(sim_dict.items(), key=operator.itemgetter(1), reverse=True)
	predicted_rating = sorted_sim_dict[0][0]
	actual_rating = dataset[cur_trackId]['rating']
	if predicted_rating == actual_rating:
		correct += 1

	conf_mat[actual_rating][predicted_rating] += 1

	i += 1
	print(i,end='\r')

print("Accuracy :",correct/i)
pickle.dump(conf_mat,open('confusion_matrix/'+genre_name+'conf_mat_'+str(k)+'_'+did+'.pickle','wb'))

logger.info("Done")

