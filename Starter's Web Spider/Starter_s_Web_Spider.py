#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib.request
from lxml import etree
import redis

# 论坛版块总字典
dict_forum = {}

# 获取Scboy论坛首页内容
def getScboy():
    # url相关
    baseUrl = "https://www.scboy.com/"
    url = baseUrl + "?forum-1.htm"

    # 获取网页内容
    response = urllib.request.urlopen(url)

    # 获取状态码，200表示成功
    if response.getcode() == 200:
        txt = response.read()
        # 使用xpath来筛选信息
        html = etree.HTML(txt, etree.HTMLParser())
        selector = html.xpath("/html/body/main/div/div/div[1]/div/div[2]/ul/li/div/div[1]/a[1]")
        print(len(selector))

        # 遍历以整理相关信息
        for t in selector:
            href = t.attrib['href']
            if href:
                if t.text != None:
                    dict_forum[t.text] = baseUrl + href
                else:
                    dict_forum[t[0].text] = baseUrl + href

# 获取163官方的内容
def get163():
    pass

# 获取NeoTV论坛的内容
def getNeoTV():
    # url相关
    baseUrl = "http://bbs.niuyou5.com/"
    url = "http://bbs.niuyou5.com/forum-161-1.html"
    
    # 获取网页内容
    response = urllib.request.urlopen(url)

    # 获取状态码，200表示成功
    if response.getcode() == 200:
        txt = response.read()
        # 使用xpath来筛选信息
        html = etree.HTML(txt, etree.HTMLParser())
        selector = html.xpath("/html/body/div[5]/div/div[3]/div[3]/div[4]/form/table/tbody/tr/th/a")
        print(len(selector))

        # 遍历以整理相关信息
        for t in selector:
            href = t.attrib['href']
            if href:
                if t.text != None:
                    dict_forum[t.text] = baseUrl + href
                else:
                    dict_forum[t[0].text] = baseUrl + href

# sqlite 数据库操作
def databaseWorker():
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    r.set('dict', dict_forum)
    #print(r['name'])
    print(r.get('dict'))  # 取出键name对应的值
    #print(type(r.get('name')))

# 第一步，获取scboy论坛信息
getScboy()
# 第二步，获取NeoTV论坛信息
getNeoTV()

print(dict_forum)
databaseWorker()