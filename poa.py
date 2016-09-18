# -*- coding: utf-8 -*-
import urllib2
import sys
import re
from readability import Document
import html2text
import time
import os
import pymongo

#设置编码为utf-8
reload(sys)
sys.setdefaultencoding( "utf-8" )

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent }
base_url="http://news.baidu.com/ns?word={school}&pn={number}&rn=20"

school_list=['上海交通大学','同济大学','复旦大学','华东师范大学','上海大学','华东理工大学','东华大学','上海财经大学','上海外国语大学','华东政法大学','上海师范大学','上海理工大学','上海海事大学','上海海洋大学','上海中医药大学','上海体育学院','上海音乐学院','上海戏剧学院','上海对外经贸大学','上海电机学院','上海工程技术大学','上海科技大学','大连海事大学','武汉理工大学','广西航运学院','武汉交通科技大学','集美大学','南通海校','中国海洋大学']

for school in school_list:
    os.mkdir(school)
    count=0
    for i in range(0,401,20):
        url=base_url.format(school=school,number=i)
        print url
        time.sleep(4)
        try:
            request=urllib2.Request(url,headers=headers)
            html=urllib2.urlopen(request).read()
            re_result=r'<div class="result" .*?>(.*?)</div>'
            re_href=r'<a href="(.*?)"'
            result=re.findall(re_result,html,re.S|re.M)
            for detail in result:
                href=re.findall(re_href,detail,re.S|re.M)[0]
                time.sleep(1)
                try:
                    html=urllib2.urlopen(href,timeout=5).read()
                    readable_article = Document(html).summary()
                    result=html2text.html2text(readable_article)
                    print "processing...."
                    with open(school+"/"+str(count)+".txt","w") as f:
                        f.write(result)
                    count=count+1
                except Exception,e:
                    print e

        except urllib2.HTTPError,e:
            print e.reason