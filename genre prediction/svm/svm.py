import numpy as np
from sklearn.svm import SVC
import pickle,sys
import warnings
from sklearn.ensemble import GradientBoostingClassifier
warnings.filterwarnings("ignore", category=DeprecationWarning) 


did = sys.argv[1]
did = str(did)

genre_list = ['R&B','Country','Rap','Reggae','Religious','Metal']
sample_song_dataset = pickle.load(open('song_vectors_for_genre_dataset_'+did+'.pickle','rb'))
train=pickle.load(open("../dataset/80_20_train_"+did+".pickle","rb"))
test= pickle.load(open("../dataset/80_20_test_"+did+".pickle","rb"))
id_detail= pickle.load(open("id_detail_"+did+".pickle","rb"))
count =0
ab=np.random.rand(len(sample_song_dataset['train']),300)
label = np.chararray(len(sample_song_dataset['train']),itemsize=9)
label[:]=''

for songId in sample_song_dataset['train']:
	j=0
	for feature in sample_song_dataset['train'][songId]['vector']:
		ab[count][j]=feature		
		j += 1
	label[count]=train[id_detail[count]]['genre']
	count +=1

clf = SVC(random_state=10)
clf.fit(ab,label)


print("Total Count:"+str(count)+"  Original Count:"+str(len(sample_song_dataset['train'])))


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
n = len(test)
i = 0

temp= np.random.rand(1,300)
for songId in sample_song_dataset['test']:
	j=0
	for feature in sample_song_dataset['test'][songId]['vector']:
		temp[0][j]=feature
		j +=1
	genre = test[id_detail[count]]['genre']
	predicted = (clf.predict(temp[0])[0]).decode('utf-8')
	if genre==predicted:
		correct += 1
	
	conf_mat[genre][predicted] +=1
	count +=1
	total += 1
	if i%100 == 0:
		print(i,"/",n,":",genre,"=>",predicted,"\t",correct,"/",total)
	i += 1

print("")	
print("Accuracy :",(correct/total))

pickle.dump( conf_mat, open('confusion_matrix/conf_mat_'+did+'.pickle' , 'wb') )

for genre in ['R&B','Country','Rap','Reggae','Religious','Metal']:
    for opgenre in ['R&B','Country','Rap','Reggae','Religious','Metal']:
        print(conf_mat[genre][opgenre],end=',')
    print("")

