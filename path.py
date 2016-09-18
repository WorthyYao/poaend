#coding=utf-8
from pymongo import MongoClient
import os

conn=MongoClient('localhost',27017)
db=conn.poa



path="poa/"
catelist=os.listdir(path)
for mydir in catelist:
    data1={"school":mydir,"activity":45}
    data2={"school":mydir,"activity":45}
    data3={"school":mydir,"activity":45}
    data4={"school":mydir,"activity":45}

    db.data.insert(data1)
    db.data.insert(data2)
    db.data.insert(data3)
    db.data.insert(data4)