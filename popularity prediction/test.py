import pickle
import sys,os,string
import gensim,logging

did = sys.argv[1]
did = str(did)

genre_name = sys.argv[2]
genre_name = str(genre_name)


model_fname = "models/model_80_20_"+genre_name+"_rating_"+did+"_dbow.model"
model = gensim.models.doc2vec.Doc2Vec.load(model_fname)

test_dataset = pickle.load(open('dataset/80_20_'+genre_name+'_rating_test_'+did+'.pickle','rb'))

print("Data loaded...")

check_n = 1



conf_mat = {}
conf_mat['Low'] = {}
conf_mat['High'] = {}



for rating in conf_mat:
    conf_mat[rating]['Low'] = 0
    conf_mat[rating]['High'] = 0
    
    

total = 0
correct = 0
n = len(test_dataset)
i = 0

for trackId in test_dataset:
	
	rating = test_dataset[trackId]['rating']
	test_rating = str(rating)
	lyrics = test_dataset[trackId]['lyrics']
	lyrics = lyrics.lower()
	lyrics = lyrics.translate(str.maketrans('','',string.punctuation))
	newvec = model.infer_vector(lyrics.split())
	op = model.docvecs.most_similar([newvec],topn=check_n)

	prediction = op[0][0]
	
	for op_pred in op:
		if op_pred[0] == test_rating:
			correct += 1
			prediction = op_pred[0]
			break
	total += 1

	conf_mat[test_rating][prediction] += 1

	if i%100 == 0:
		print(i,"/",n,":",rating,"=>",prediction,"\t",correct,"/",total)
	i += 1

print("")	
print("Accuracy :",(correct/total))

pickle.dump( conf_mat, open('confusion_matrix/conf_mat_'+genre_name+'_'+did+'.pickle' , 'wb') )

for rating in ['Low','High']:
    for oprating in ['Low','High']:
        print(conf_mat[rating][oprating],end=',')
    print("")
