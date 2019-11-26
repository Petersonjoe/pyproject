#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------#
# @Date    : 2019-11-03 10:55:10
# @Author  : jlei1 (jilei191@163.com)
# @Link    : github.com/Petersonjoe
#-------------------------------------------#



import sys
if '../../' not in sys.path:
    sys.path.insert(0, '../../')

print(sys.stdout.encoding)

# reassign the encode for strings
import codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

import requests
import random
import json
from requests_html import HTMLSession

target_url = [
# TV list
'https://movie.douban.com/j/search_subjects?type=tv&tag=%E7%83%AD%E9%97%A8&page_limit=50&page_start=0',
# Movie list
'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&page_limit=50&page_start=0'
]

# to declare a random header for the 403 error that prevents spider
headers = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11",
    "Opera/9.25 (Windows NT 5.1; U; en)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12",
    "Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9",
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
]

selected_header = {'User-Agent': random.choice(headers)}
print(f'User-Agent re-direct to: {selected_header["User-Agent"]}')


#-------------- douban URL element --------------#
# note that, modern web browser always show you the ccs selector when you inspecting elements of a web page
from requests.exceptions import HTTPError
spider_session = HTMLSession()

url = 'https://movie.douban.com/subject/30401122/'
response = spider_session.get(url,headers=selected_header)

#-------------- base info --------------#
# base info selection
tv_id = url.split('/')[-2]  # tv id
tv_header = response.html.find('div#content>h1')  # title
tv_info = response.html.find('#info',first=True)  # dimension info
info_list = tv_info.text.split('\n')

# base info assembling
def info_split(item: str = None) -> list:
    if ':' in item:
        key = item.split(':')[0].strip()
        value = item.split(':')[1].strip()
        return [key, value]
    else:
        return None

base_info = {}
base_info["剧名"] = tv_header[0].text.strip()
for x in info_list:
    if info_split(x):
        base_info[info_split(x)[0]]=info_split(x)[1]

print(base_info["剧名"])
print(base_info["导演"])
print(base_info["编剧"])
print(base_info["主演"])
print(base_info["类型"])
print(base_info["制片国家/地区"])
print(base_info["语言"])
print(base_info["首播"])

#-------------- rating summary --------------#
# rating summary info selection
rating_summ = {
    "rat_lvl": [], # 5 star -- 1 star
    "rat_pct": []  # 5* val -- 1* val
}
rating_num = response.html.find('strong.ll.rating_num')  # summary rating number
print(float(rating_num[0].text))
rating_pp = response.html.find('a.rating_people>span')  # number of rating people
print(int(rating_pp[0].text))
rating_dist = response.html.find('div.ratings-on-weight')  # rating distribution
raw_dist = rating_dist[0].text.split('\n')
for index, value in enumerate(raw_dist):
    print(index, value)
    if (index % 3) == 0:
        rating_summ["rat_lvl"].append(value)
    elif (index % 3) == 1:
        rating_summ["rat_pct"].append(value)
    else:
        pass

print(rating_summ)

#-------------- comment section --------------#
# get the url for comment section
cmt_url = response.html.find('div.mod-hd h2 span.pl a')
print(cmt_url[0])
print(cmt_url[0].attrs["href"])


spider_session.close()


