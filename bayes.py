# -*- coding: utf-8 -*-

import sys
import os
from sklearn.datasets.base import Bunch
import cPickle as pickle
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

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


trainpath="train_word_bag/tfdifspace.dat"
train_set=readbunchobj(trainpath)

testpath="test_word_bag/testspace.dat"
test_set=readbunchobj(testpath)


clf=MultinomialNB(alpha=0.001).fit(train_set.tdm,train_set.label)

predicted=clf.predict(test_set.tdm)

total=len(predicted);rate=0
for expct_cate in predicted:
    print expct_cate

