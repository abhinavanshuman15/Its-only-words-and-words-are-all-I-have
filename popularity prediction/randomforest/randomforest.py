import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle,sys
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 


did = sys.argv[1]
did = str(did)

genre_name = sys.argv[2]
genre_name = str(genre_name)

sample_song_dataset = pickle.load(open('song_vectors_for_'+genre_name+'_dataset_'+did+'.pickle','rb'))
train=pickle.load(open("../dataset/80_20_"+genre_name+"_rating_train_"+did+".pickle","rb"))
test= pickle.load(open("../dataset/80_20_"+genre_name+"_rating_test_"+did+".pickle","rb"))
id_detail= pickle.load(open(genre_name+"id_detail_"+did+".pickle","rb"))
count =0
ab=np.random.rand(len(sample_song_dataset['train']),300)
label = np.chararray(len(sample_song_dataset['train']),itemsize=9)
label[:]=''

for songId in sample_song_dataset['train']:
	j=0
	for feature in sample_song_dataset['train'][songId]['vector']:
		ab[count][j]=feature		
		j += 1
	label[count]=train[id_detail[count]]['rating']
	count +=1

clf = RandomForestClassifier(n_estimators=50)
clf.fit(ab,label)

print("Total Count:"+str(count)+"  Original Count:"+str(len(sample_song_dataset['train'])))

type_list = ['Low','High']
conf_mat = {}
for type in type_list:
	conf_mat[type] = {}
	for type1 in type_list:
		conf_mat[type][type1] = 0

total = 0
correct = 0
n = len(test)
i = 0

temp= np.random.rand(1,300)
for songId in sample_song_dataset['test']:
	j=0
	for feature in sample_song_dataset['test'][songId]['vector']:
		temp[0][j]=feature
		j +=1
	rating = test[id_detail[count]]['rating']
	predicted = (clf.predict(temp[0])[0]).decode('utf-8')
	if rating==predicted:
		correct += 1
	conf_mat[rating][predicted] +=1
	count +=1
	total += 1
	if i%100 == 0:
		print(i,"/",n,":",rating,"=>",predicted,"\t",correct,"/",total)
	i += 1

print("")	
print("Accuracy :",(correct/total))

pickle.dump( conf_mat, open('confusion_matrix/'+genre_name+'conf_mat_'+did+'.pickle' , 'wb') )

for rating in type_list:
    for oprating in type_list:
        print(conf_mat[rating][oprating],end=',')
    print("")

