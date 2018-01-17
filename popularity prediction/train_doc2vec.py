import pickle
import sys,os,string,codecs,pickle
import gensim,logging
import multiprocessing

program = os.path.basename(sys.argv[0])
logger = logging.getLogger(program)

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
logging.root.setLevel(level=logging.INFO)
logger.info("running %s" % ' '.join(sys.argv))

did = sys.argv[2]
did = str(did)

genre_name = sys.argv[3]
genre_name = str(genre_name)

logger.info("Dataset Id : "+did)
logger.info("Loaded : 80_20_"+genre_name+"_rating_train_"+did+".pickle")

class MySentences(object):
    def __init__(self, datasetName):
        self.datasetName = datasetName

    def __iter__(self):

        dataset = pickle.load(open("dataset/80_20_"+genre_name+"_rating_train_"+did+".pickle" , "rb"))
        for trackId in dataset:
            lyrics      = dataset[trackId]['lyrics']
            rating_label = str(dataset[trackId]['rating'])
            rating_label = rating_label
            lyrics = lyrics.lower()
            lyrics = lyrics.translate(str.maketrans('','',string.punctuation))
            song = gensim.models.doc2vec.LabeledSentence(words=lyrics.split(), tags=[rating_label])
            yield song


sentences = MySentences('')

print("training model")

if sys.argv[1] == 'dm':
    model = gensim.models.Doc2Vec (sentences,size = 300, window = 5, workers = multiprocessing.cpu_count(), min_count = 5, iter = 20, dm=1)
elif sys.argv[1] == 'dbow':
    model = gensim.models.Doc2Vec (sentences,size = 300, window = 5, workers = multiprocessing.cpu_count() ,min_count = 5, iter = 20, dm=0)

print("")
print("saving model")
model.save('models/model_80_20_'+genre_name+'_rating_'+did+'_dbow.model')

