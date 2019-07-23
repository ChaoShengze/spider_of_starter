#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib.request
from lxml import etree
import redis
import websocket

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
        print("scboy get:" + len(selector))

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
    url = baseUrl + "forum-161-1.html"
    
    # 获取网页内容
    response = urllib.request.urlopen(url)

    # 获取状态码，200表示成功
    if response.getcode() == 200:
        txt = response.read()
        # 使用xpath来筛选信息
        html = etree.HTML(txt, etree.HTMLParser())
        selector = html.xpath("/html/body/div[5]/div/div[3]/div[3]/div[4]/form/table/tbody/tr/th/a")
        print("neotv get:" + len(selector))

        # 遍历以整理相关信息
        for t in selector:
            href = t.attrib['href']
            if href:
                if t.text != None:
                    dict_forum[t.text] = baseUrl + href
                else:
                    dict_forum[t[0].text] = baseUrl + href

# 数据写入 Redis
def writeRedis():
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    for data in dict_forum:
        r.set(data, dict_forum[data])

# 第一步，获取scboy论坛信息
getScboy()
# 第二步，获取NeoTV论坛信息
getNeoTV()

#print(dict_forum)

# 第三步，将之前获得的数据存入Redis
writeRedis()