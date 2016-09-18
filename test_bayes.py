#coding=utf-8
import sys
import os
from sklearn.datasets.base import Bunch
import cPickle as pickle
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from pymongo import MongoClient

conn=MongoClient('localhost',27017)
db=conn.poa

reload(sys)
sys.setdefaultencoding( "utf-8" )



def readbunchobj(path):
    file_obj=open(path,"rb")
    bunch=pickle.load(file_obj)

    file_obj.close()
    return bunch

def writebunchobj(path,bunchobj):
    file_obj=open(path,"wb")
    pickle.dump(bunchobj,file_obj)
    file_obj.close()

def readfile(path):
    fp=open(path,"rb")
    content=fp.read()
    fp.close()
    return content

stopword_path="train_word_bag/hlt_stop_words.txt"
stpwrdlst=readfile(stopword_path).splitlines()

trainpath="poa_word_bag/tfdifspace.dat"
train_set=readbunchobj(trainpath)



trainbunch=readbunchobj("poa_word_bag/tfdifspace.dat")

vectorizer=TfidfVectorizer(stop_words=stpwrdlst,sublinear_tf=True,max_df=0.5,vocabulary=trainbunch.vocabulary)
transformer=TfidfTransformer()

clf=MultinomialNB(alpha=0.001).fit(train_set.tdm,train_set.label)

testpath="poa/"
catelist=os.listdir(testpath)

for mydir in catelist:
    seg_dir=testpath+mydir+"/"

    file_list=os.listdir(seg_dir)
    activity,entrance,social,study=0,0,0,0
    for file_path in file_list:
        content=[]
        fullname=seg_dir+file_path
        content.append(readfile(fullname).strip())
        tdm=vectorizer.fit_transform(content)

        predicted=clf.predict(tdm)

        for expct_cate in predicted:
            if expct_cate=="activity":
                activity=activity+1
            elif expct_cate=="entrance":
                entrance=entrance+1
            elif expct_cate=="social":
                social=social+1
            else:
                study=study+1

    data1={"school":mydir,"activity":activity}
    data2={"school":mydir,"entrance":entrance}
    data3={"school":mydir,"social":social}
    data4={"school":mydir,"study":study}

    db.data.insert(data1)
    db.data.insert(data2)
    db.data.insert(data3)
    db.data.insert(data4)
    print mydir