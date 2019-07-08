#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib.request
# from bs4 import BeautifulSoup
from lxml import etree

url = "https://www.scboy.com/?forum-1.htm"
response1 = urllib.request.urlopen(url)
# 获取状态码，200表示成功
if response1.getcode() == 200:
	txt = response1.read()
	html = etree.HTML(txt, etree.HTMLParser())
	selector = html.xpath("/html/body/main/div/div/div[1]/div/div[2]/ul/li/div/div[1]/a[1]")
	print(len(selector))

	for t in selector:
		if t.attrib['href']:
			print(t.attrib['href'])
		else:
			print(t)