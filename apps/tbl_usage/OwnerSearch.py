# -*- coding: utf-8 -*-
#############################################
# @Author: jlei1
# @Date:   2018-12-20
# @Last Modified By:   jlei1
# @Last Modified Time: 2019-09-22
#############################################
import os, sys
if '../../' not in sys.path:
	sys.path.insert(0, '../../')
from utils.ReadConfig import DecodeConfig
from utils.GlobalVars import PROJ_ROOT_DIR
import requests, json
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

input_path = PROJ_ROOT_DIR + '/input/tbl_usage/'
input_file = 'batch'
output_path = PROJ_ROOT_DIR + '/output/tbl_usage/'
output_file = 'batch_owner_email_list.csv'
#print(input_path)

config = DecodeConfig()
batch_list = config.getCSV(filepath=input_path, filename=input_file)
#print(batch_list)

def searchByBatch(batch: str=None) -> list:

def write2csv(filepath: str=output_path, filename: str=output_file, data: list=None) -> None:

def ownerSearch(searchlist: list=batch_list) -> None:

if __name__ == '__main__':
