import pickle,sys,gensim
import logging,os

program = os.path.basename(sys.argv[0])
logger = logging.getLogger(program)

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
logging.root.setLevel(level=logging.INFO)
logger.info("running %s" % ' '.join(sys.argv))



did = sys.argv[1]
did = str(did)

genre_name = sys.argv[2]
genre_name = str(genre_name)


dataset 	 = pickle.load(open("../dataset/80_20_"+genre_name+"_rating_train_"+did+".pickle" , "rb"))
dataset_test = pickle.load(open("../dataset/80_20_"+genre_name+"_rating_test_"+did+".pickle" , "rb"))

trackId_2_intId = pickle.load(open("../trackId_2_intId.pickle" , "rb"))


model = gensim.models.doc2vec.Doc2Vec.load('../models/model_80_20_'+genre_name+'_rating_'+did+'_dbow.model')

logger.info("datasets loaded...")

op_dataset = {}

op_dataset['train'] = {}
op_dataset['test'] = {}

i = 0

for trackId in dataset:
	lyrics = dataset[trackId]['lyrics']
	rating= dataset[trackId]['rating']
	intId = trackId_2_intId[trackId]
	vec = model.infer_vector(lyrics.split())
	op_dataset['train'][intId] = {}
	op_dataset['train'][intId]['rating'] = rating
	op_dataset['train'][intId]['vector'] = vec
	i += 1
	print(i,end='\r')

for trackId in dataset_test:
	lyrics = dataset_test[trackId]['lyrics']
	rating = dataset_test[trackId]['rating']
	intId = trackId_2_intId[trackId]
	vec = model.infer_vector(lyrics.split())
	op_dataset['test'][intId] = {}
	op_dataset['test'][intId]['rating'] = rating
	op_dataset['test'][intId]['vector'] = vec
	
	i += 1
	print(i,end='\r')

print('\nwriting...')
pickle.dump(op_dataset, open(genre_name+'song_vectors_dataset_'+did+'.pickle','wb'))
logger.info("Done")
