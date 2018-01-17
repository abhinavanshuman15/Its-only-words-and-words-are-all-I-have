import pickle
import sys


did = sys.argv[2]
did = str(did)

k = int(sys.argv[1])

genre_name = sys.argv[3]
genre_name = str(genre_name)

conf_mat= pickle.load(open('confusion_matrix/'+genre_name+'conf_mat_'+str(k)+'_'+did+'.pickle','rb'))
quality_list = ['Low','High']
print ("Confusion Matrix")
for i in quality_list:
	for j in quality_list:
		print(conf_mat[i][j],end="\t")
	print(i)
sum=0
sum1=0
avg=0
w_avg=0
score={}
count = 0
file=open("results/"+genre_name+"_result_"+str(k)+"_"+did+"_"+".xls","w")

print("Row_Sum  Col_Sum Precision \t\t Recall \t\t F_score \t\t Tag" )
for i in conf_mat:
	sum=0
	sum1=0
	
	for j in conf_mat[i]:
		#print(conf_mat[i][j],end="\t")
		sum=sum+conf_mat[i][j]
		
		sum1=sum1+conf_mat[j][i]
	try:
		prec=conf_mat[i][i]/sum
	except ZeroDivisionError:
		prec = 0
	try:	
		recall=conf_mat[i][i]/sum1
	except ZeroDivisionError:
		recall = 0
	try:
		f=(2*prec*recall)/(prec+recall)	
	except ZeroDivisionError:
		f = 0
	avg=avg+f
	score[i]=f
	count += sum 
	w_avg=w_avg+f*sum
	print("%s \t %s \t %s \t %s \t %s \t %s"  % (sum,sum1,prec,recall,f,i))



for i in quality_list:
	print(score[i])
	file.write(i+"\t"+str(score[i])+"\n")
file.write("\n \n Average:\t"+str(avg/len(quality_list)))
file.write("\n Weighted Average:\t"+str(w_avg/count)+"\n\n\n")	
print("Avg=%s" %(avg/len(quality_list)))
print("Weighted Average=" ,str(w_avg/count))
