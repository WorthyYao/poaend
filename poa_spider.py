#coding=utf-8
import urllib2
import sys
import re
from readability import Document
import html2text
import time
from pymongo import MongoClient
from bs4 import BeautifulSoup

#设置默认编码为utf-8
reload(sys)
sys.setdefaultencoding( "utf-8" )

#连接数据库
conn=MongoClient('localhost',27017)
db = conn.news

#设置用户代理
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent }

#初始网页
base_url="http://news.baidu.com/ns?word={school}&pn={number}&rn=20"

school_list={"上海交通大学":"sjtu",'同济大学':'tongji','复旦大学':'fudan','华东师范大学':'ecnu','上海大学':'shu','华东理工大学':'ecust','东华大学':'dhu','上海财经大学':'shufe','上海外国语大学':'shisu','华东政法大学':'ecupl','上海师范大学':'shnu','上海理工大学':'usst','上海海事大学':'smu','上海海洋大学':'shou','上海中医药大学':'shutcm','上海体育学院':'sus','上海音乐学院':'shcmusic','上海戏剧学院':'sta','上海对外经贸大学':'shift','上海电机学院':'sdju','上海工程技术大学':'sues','上海科技大学':'shanghaitech','大连海事大学':'dlmu','武汉理工大学':'whut','集美大学':'jmu','中国海洋大学':'ouc'}

for school in school_list:
    en_school=school_list[school]
    coll=db[en_school]
    for i in range(0,1,20):
        url=base_url.format(school=school,number=i)
        print url
        time.sleep(4)
        try:
            request=urllib2.Request(url,headers=headers)
            html=urllib2.urlopen(request).read()
            re_result=r'<h3 class="c-title">(.*?)<span class="c-info">'
            re_href=r'<a href="(.*?)"'
            re_date=r'<p class="c-author">.*?&nbsp;&nbsp;(.*?)</p>'
            result=re.findall(re_result,html,re.S|re.M)
            for detail in result:
                href=re.findall(re_href,detail,re.S|re.M)[0]
                date=re.findall(re_date,detail,re.S|re.M)[0]
                time.sleep(1)
                try:
                    html=urllib2.urlopen(href,timeout=5).read()
                    soup=BeautifulSoup(html,"lxml")
                    readable_article = Document(html).summary()
                    result=html2text.html2text(readable_article)
                    print "processing...."
                    print soup.title.string
                    single_new={"title":soup.title.string,"url":href,"body":result,"date":date}
                    coll.insert(single_new)
                except Exception,e:
                    print e

        except urllib2.HTTPError,e:
            print e.reason

