# -*- coding: utf-8 -*-

import sys
from sklearn.datasets.base import Bunch
import cPickle as pickle
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from pymongo import MongoClient

conn=MongoClient('localhost',27017)
db = conn.news
poa_db=conn.poa

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

stopword_path="/home/yao/Project/Python/Root/train_word_bag/hlt_stop_words.txt"
stpwrdlst=readfile(stopword_path).splitlines()

trainpath="/home/yao/Project/Python/Root/poa_word_bag/tfdifspace.dat"
train_set=readbunchobj(trainpath)



trainbunch=readbunchobj("/home/yao/Project/Python/Root/poa_word_bag/tfdifspace.dat")

vectorizer=TfidfVectorizer(stop_words=stpwrdlst,sublinear_tf=True,max_df=0.5,vocabulary=trainbunch.vocabulary)
transformer=TfidfTransformer()

#贝页斯分类器训练
clf = MultinomialNB(alpha=0.001).fit(train_set.tdm,train_set.label)

school_list = {"上海交通大学":"sjtu",'同济大学':'tongji','复旦大学':'fudan','华东师范大学':'ecnu','上海大学':'shu','华东理工大学':'ecust','东华大学':'dhu','上海财经大学':'shufe','上海外国语大学':'shisu','华东政法大学':'ecupl','上海师范大学':'shnu','上海理工大学':'usst','上海海事大学':'smu','上海海洋大学':'shou','上海中医药大学':'shutcm','上海体育学院':'sus','上海音乐学院':'shcmusic','上海戏剧学院':'sta','上海对外经贸大学':'shift','上海电机学院':'sdju','上海工程技术大学':'sues','上海科技大学':'shanghaitech','大连海事大学':'dlmu','武汉理工大学':'whut','集美大学':'jmu','中国海洋大学':'ouc'}

for school in school_list:
    print school
    en_school=school_list[school]
    coll_school=db[en_school]
    coll_poa=poa_db['school']
    activity,entrance,social, study = 0, 0, 0, 0
    for news in coll_school.find():
        content=[]
        content.append(news['body'])
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
            result={"school":school,"title":news['title'],"url":news['url'],"classification":expct_cate,"date":news['date']}
            coll_poa.insert(result)

    data={"school":school,"activity":activity,"entrance":entrance,"social":social,"study":study}

    poa_db.data.insert(data)
