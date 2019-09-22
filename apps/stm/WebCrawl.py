# -*- coding: utf-8 -*-
#############################################
# @Author: jlei1
# @Date:   2018-07-02
# @Last Modified By:   jlei1
# @Last Modified Time: 2018-12-21
#############################################

from distutils.log import warn as printf
from bs4 import BeautifulSoup
import urllib3, requests, re
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# add the parent folder to path
# import os, sys
# if '../' not in sys.path:
# 	sys.path.insert(0, '../')
# from conf.urls import URLS

# url = URLS[0]

class SiteTable(object):
	"""
	SiteTable class receives a url point to a stm table in dmaas.
	:Instantiate a SiteTable object
		example: st = SiteTable(url)
				 st.requestInit()
	:A SiteTable object has 4 basic properties
		- table name: e.g., st.name
		- table description or purpose: e.g., st.desc
		- table's primary keys: e.g., st.pks
		- table's structure data: e.g., st.structure
	"""
	# .*?\) stands for matching arbitrary character once met the fisrt ')'
	__patterns__ = {
		"tbl_name": 'Table\s(.*)',
		"tbl_desc": 'Purpose of \w+:\s(.*)\s{2}(.*)',
		"tbl_structure": '\s{1,9}([^\f\n\r\t\v]+)[\f\n\r\t\v]+',
		"tbl_pk": '(.*)PRIMARY\s+KEY\s+\((.*?)\)'   
	}

	__request__ = None
	__soup__ = None

	def __init__(self, url: str) -> None:
		super(SiteTable, self).__init__()
		self.url = url
		
	def __checkInit__(self) -> bool:
		if self.__request__ is None \
			or self.__soup__ is None:
			return False
		else:
			return True

	def requestInit(self) -> None:
		if self.__request__ is None \
			or self.__soup__ is None:
			self.__request__ = requests.get(self.url, verify=False)
			self.__soup__ = BeautifulSoup(self.__request__.text,"html.parser")
		else:
			printf('*** Warn: replicated request was dismissed! ***\n')

	@property
	def name(self) -> str:
		if not self.__checkInit__():
			printf('*** Error: Web reqeust initialization missed! ***')
			return

		tbl_title = re.search(
						self.__patterns__["tbl_name"],
						self.__soup__.find('h2').get_text()
					)
		_name = tbl_title.group(1)
		return _name
	
	@property
	def desc(self) -> str:
		if not self.__checkInit__():
			printf('*** Error: Web reqeust initialization missed! ***')
			return

		cmt = self.__soup__.find_all('table', 'Form')  # tag = 'table', class = 'Form'
		cmt_text = cmt[0].find_all('p')[1].get_text()
		try:  # for those cmt begin with 'Purpose of blabla: '
			_desc = re.search(
					self.__patterns__["tbl_desc"],
					cmt_text
				).group(1)
		except AttributeError:
			try:  # for those cmt not begin with 'Purpose of blabla: '
				_desc = re.search(
					'(.*?)\s{2}(.*)',
					cmt_text
				).group(1)
			except AttributeError:  # for those 'NULL' cmt
				printf('*** Warn: This table has no description on webpage. ***')
				_desc = None
		
		return _desc
	
	@property
	def pks(self) -> list:
		'''
		: table.pks will return a list contains all primary keys
		'''
		if not self.__checkInit__():
			printf('*** Error: Web reqeust initialization missed! ***')
			return

		ddl_content = self.__soup__.find_all('table','Text')[1]
		key_list = re.search(
						  self.__patterns__["tbl_pk"],
						  ddl_content.get_text(),
						  re.I|re.M|re.S
					  ).group(2)
		if ',' in key_list:
			key_list = key_list.split(',')
			key_list = [x.strip() for x in key_list]
		_pks = key_list
		return _pks

	@property
	def structure(self) -> dict:
		if not self.__checkInit__():
			printf('*** Error: Web reqeust initialization missed! ***')
			return
		
		_structure = {}
		# recursively validate if the raw context is the table structure
		raw_tables = self.__soup__.find_all('table','Grid')
		for raw_content in raw_tables:
			tst_trs = raw_content.find_all('tr')
			tst_hd = [
			          re.search(
			          	self.__patterns__["tbl_structure"],
			          	x.get_text()).group(1) 
			            for x in tst_trs[0].find_all('td')
			         ]
			if 'Data Type' in tst_hd:
				trs = tst_trs
				break

		count = 0
		for tr in trs:
			if count == 0:
				if not ("headers" in _structure):
					_structure["headers"] = []
				header = [
						  re.search(
							  self.__patterns__["tbl_structure"],
							  x.get_text()
						  ).group(1) 
						  for x in tr.find_all('td')
						 ]
				_structure["headers"] = header
			else:
				if not ("rows" in _structure):
					_structure["rows"] = []
				
				row = [
					   re.search(
					   	   self.__patterns__["tbl_structure"],
					   	   x.get_text()
					   ).group(1) 
					   for x in tr.find_all('td')
					  ]
				_structure["rows"].append(row)
			count += 1
		return _structure

# if __name__ == '__main__':
# 	a = SiteTable(url)
# 	a.requestInit()
# 	printf(a.name)
# 	import pdb; pdb.set_trace()
# 	printf(a.desc)
# 	printf(a.pks)
# 	printf(a.structure)
