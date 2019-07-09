#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib.request
from lxml import etree

url = "https://www.scboy.com/?forum-1.htm"
response = urllib.request.urlopen(url)

dict = {}

# 获取状态码，200表示成功
if response.getcode() == 200:
    txt = response.read()
    html = etree.HTML(txt, etree.HTMLParser())
    selector = html.xpath("/html/body/main/div/div/div[1]/div/div[2]/ul/li/div/div[1]/a[1]")
    print(len(selector))

    for t in selector:
        href = t.attrib['href']
        if href:
            if t.text != None:
                dict[t.text] = href
            else:
                dict[t[0].text] = href

    print(dict)