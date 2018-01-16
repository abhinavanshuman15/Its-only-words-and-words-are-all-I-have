import pickle
import sys,os
import gensim,logging,string

did=sys.argv[1]
did=str(did)

model_fname = "models/model_80_20_"+did+"_dbow.model"
model = gensim.models.doc2vec.Doc2Vec.load(model_fname)

test_dataset = pickle.load(open('dataset/80_20_test_'+did+'.pickle','rb'))

print("Data loaded...")

check_n = 1


conf_mat = {}

conf_mat['R&B']             = {}
conf_mat['Country']         = {}
conf_mat['Rap']             = {}
conf_mat['Reggae']          = {}
conf_mat['Religious']          = {}
conf_mat['Metal']          = {}

for genre in conf_mat:
    conf_mat[genre]['R&B'] = 0
    conf_mat[genre]['Country'] = 0
    conf_mat[genre]['Rap'] = 0
    conf_mat[genre]['Reggae'] = 0
    conf_mat[genre]['Religious'] = 0
    conf_mat[genre]['Metal'] = 0

total = 0
correct = 0
n = len(test_dataset)
i = 0

for trackId in test_dataset:
	genre = test_dataset[trackId]['genre']
	test_genre = 'GENRE_'+genre
	lyrics = test_dataset[trackId]['lyrics']
	lyrics = lyrics.lower()
	lyrics = lyrics.translate(str.maketrans('','',string.punctuation))
	newvec = model.infer_vector(lyrics.split())
	op = model.docvecs.most_similar([newvec],topn=check_n)

	prediction = op[0][0]
	
	for op_pred in op:
		if op_pred[0] == test_genre:
			correct += 1
			prediction = op_pred[0]
			break
	total += 1
	conf_mat[genre][prediction[6:]] += 1

	if i%100 == 0:
		print(i,"/",n,":",genre,"=>",prediction[6:],"\t",correct,"/",total)
	i += 1

print("")	
print("Accuracy :",(correct/total))

pickle.dump( conf_mat, open('confusion_matrix/conf_mat_'+did+'.pickle' , 'wb') )

for genre in ['R&B','Country','Rap','Reggae','Religious','Metal']:
    for opgenre in ['R&B','Country','Rap','Reggae','Religious','Metal']:
        print(conf_mat[genre][opgenre],end=',')
    print("")
