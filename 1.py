# -*- coding: utf-8 -*-
import requests
import os
import string
from bs4 import BeautifulSoup
from lxml import etree
import sys


reload(sys)
sys.setdefaultencoding('utf-8')
isProxyNeeded = False


class AllData:
    def __init__(self):
        self.m_chapters = []

    def add_chapter(self, chapter):
        self.m_chapters.append(chapter)

class Chapter:
    def __init__(self, name= "", address = ""):
        self.m_name = name
        self.m_address = address

    def setName(self, name):
        self.m_name = name

    def setAddress(self, address):
        self.m_address = address


class NetWorkSetting:
    def __init__(self):
        self.proxy = {
            "http": 'http://10.144.1.10:8080',
            "https": 'https://10.144.1.10:8080'}
        self.searchUrl = 'http://tianyibook.com/tianyibook/42/42541/index.html'
        self.prefixUrl = 'http://tianyibook.com/tianyibook/42/42541/'
        self.myHeaders = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
            'Referer': 'http://tianyibook.com'}
        self.savePath = "dahuangmanshen"


#1. get result for key word search
print "1, get chapter list source"
wmp = AllData()
setting = NetWorkSetting()
session = requests.Session()

if isProxyNeeded:
    result = session.get(setting.searchUrl, headers=setting.myHeaders, proxies=setting.proxy)
else:
    result = session.get(setting.searchUrl, headers=setting.myHeaders)
print result.url, result.status_code

soup = BeautifulSoup(result.content)
index = 1
for link in soup.find_all('a'):
    if link.text.find("第") != -1:
        eachChapter = Chapter()
        chapter_url = setting.prefixUrl + str(link.get('href'))
        eachChapter.setAddress(chapter_url)
        #eachChapter.setName(str(index) + "    " + link.text + ".html")
        eachChapter.setName(str(index) + ".html")
        index += 1
        wmp.add_chapter(eachChapter)

#2, makdir for xiaoshuo
print "2, makdir for xiaoshuo"
if os.path.exists(setting.savePath):
    pass
else:
    os.makedirs(setting.savePath)

#3, get all the chapters for xiaoshuo
print "3, get all the chapters for xiaoshuo"
for chapter in wmp.m_chapters:
    newfilename = setting.savePath + "//" + chapter.m_name
    if os.path.exists(newfilename):
        pass
    else:
        if isProxyNeeded:
            result = session.get(chapter.m_address, headers=setting.myHeaders, proxies=setting.proxy)
        else:
            result = session.get(chapter.m_address, headers=setting.myHeaders)

        if result.status_code == 200:

            f = open(setting.savePath + "//" + chapter.m_name,'w+')
            f.write(result.content)
            f.close()

print "end of now"



