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

from requests.exceptions import HTTPError

target_url = [
# TV list
'https://movie.douban.com/j/search_subjects?type=tv&tag=%E7%83%AD%E9%97%A8&page_limit=50&page_start=0',
'https://movie.douban.com/j/search_subjects?type=tv&tag=%E7%83%AD%E9%97%A8&page_limit=50&page_start=50',
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

class DataCrawler(object):
    """docstring for DataCrawler"""

    __version__ = '1.0'

    def __init__(self, url: str = None) -> None:
        super(DataCrawler, self).__init__()
        self.url = url

    def getRestApi(self) -> dict:
        """
        For GET the Restful API json response.
        Slight difference with get other html page is it returns a dict not an entire html.
        """
        _json = {}
        print(self.__version__)
        selected_header = {'User-Agent': random.choice(headers)}
        print(f'User-Agent re-direct to: {selected_header["User-Agent"]}')
        
        try:
            response = requests.get(self.url,headers=selected_header)
            response.raise_for_status()
            _json = json.loads(response.text)
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            print('Success!')

        return _json

    @staticmethod
    def getHtmlSession(surl: str = None) -> None:
        selected_header = {'User-Agent': random.choice(headers)}
        session = HTMLSession()
        _response = session.get(surl,headers=selected_header)

        return _response

    def getItemList(self) -> list:
        '''
        This method is to get the Tv or Movie URL list.
        This method is app-specific, for other website, it may change the attributes to get desired response.
        '''
        _json_list = self.getRestApi()["subjects"]
        return [item["url"] for item in _json_list]

    def pageCrawl(self) -> None:
        '''
        Redirect to home page of each movie or tv
        get base info: 电影，电影主演，上映日期等
        get comment detail: user, rate, time, gender, location
        get ...
        Write data into sqlite3 database
        '''
        # get base info
        url_list = self.getItemList()
        for surl in url_list:
            print('---------------------')

            sr = self.getHtmlSession(surl)
            _info = sr.html.find('#info',first=True)
            _info_list = _info.text.split('\n')

            _base_info = {}
            for x in _info_list:
                if ':' in x:
                    key = x.split(':')[0].strip()
                    value = x.split(':')[1].strip()
                    _base_info[key]=value
            
            if _base_info:
                for k,v in enumerate(_base_info):
                    print(f'{v}: {_base_info[v]}')

if __name__ == '__main__':
    spider = DataCrawler(url=target_url[0])
    spider.pageCrawl()







