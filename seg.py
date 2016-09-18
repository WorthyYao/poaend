# -*- coding: utf-8 -*-

import sys
import os
import jieba

reload(sys)
sys.setdefaultencoding( "utf-8" )


def savefile(savepath,content):
    fp=open(savepath,"wb")
    fp.write(content)
    fp.close()

def readfile(path):
    fp=open(path,"rb")
    content=fp.read()
    fp.close()
    return content


corpus_path="poa_corpus_train/"
seg_path="poa_corpus_seg/"

catelist=os.listdir(corpus_path)


for mydir in catelist:
    class_path=corpus_path+mydir+"/"
    seg_dir=seg_path+mydir+"/"
    if not os.path.exists(seg_dir):
        os.makedirs(seg_dir)
    file_list=os.listdir(class_path)
    for file_path in file_list:
        fullname=class_path+file_path
        content=readfile(fullname).strip()
        content=content.replace("\r\n","").strip()
        content_seg=jieba.cut(content)
        savefile(seg_dir+file_path," ".join((content_seg)))

print "The Chinese Seg Finished"



