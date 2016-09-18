# -*- coding: utf-8 -*-

import sys
import os
from sklearn.datasets.base import Bunch
import cPickle as pickle
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

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

path="test_word_bag/test_set.dat"
bunch=readbunchobj(path)

testspace=Bunch(target_name=bunch.target_name,label=bunch.label,filenames=bunch.filenames,tdm=[],vocabulary={})

trainbunch=readbunchobj("train_word_bag/tfdifspace.dat")

vectorizer=TfidfVectorizer(stop_words=stpwrdlst,sublinear_tf=True,max_df=0.5,vocabulary=trainbunch.vocabulary)
transformer=TfidfTransformer()

testspace.tdm=vectorizer.fit_transform(bunch.contents)
testspace.vocabulary=trainbunch.vocabulary

space_path="test_word_bag/testspace.dat"
writebunchobj(space_path,testspace)


