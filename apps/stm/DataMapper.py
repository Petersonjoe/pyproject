# -*- coding: utf-8 -*-
#############################################
# @Author: jlei1
# @Date:   2018-07-09
# @Last Modified By:   jlei1
# @Last Modified Time: 2018-07-20
#############################################

from distutils.log import warn as printf

import os, sys
if '../' not in sys.path:
	sys.path.insert(0, '../')
from utils.ReadConfig import DecodeConfig 
from utils.GlobalVars import PROJ_ROOT_DIR

'''TBL_ROW_IX is a template variable of EXCEL row value dependency. 
   This variable is a dict stores the (index, row_variable) pair,
   which can be used in TemplateOperation module.
   
   Index is the key of dict which denotes the column number of this row.
   Row_variable is the value of dict which pass the variable name for the 
   specific row value or the dependency between different row values.

   e.g., 
   :the key-value pair `2: 'src_col_name'` 
   which means the 2nd col of this row will be populated with the value of
   variable `src_col_name` evaluated in the TemplateOperation module.

   :the key-value pair `7:"'Y' if src_col_name in tbl_pks else 'N'"` 
   which means the 7th col of this row, populated with the value of a logical 
   expression which involves two row_variables `src_col_name` and `tbl_pks`.

   :the key-value pair `12: 'self.__checkAbbr__(src_col_name)'`
   which means the 12th col of this row, evaluated with the return value of 
   a function defined in a class object of the TemplateOperation module.

   All variables listed in the dict values should be defined in the class 
   calling TBL_ROW_IX.

   Also, other row template can be defined like TBL_ROW_IX. The key effort is
   to realize a class where it is called.s
'''
TBL_ROW_IX = {
	1 : 'tbl_name',
	2 : 'src_col_name',
	3 : 'tbl_desc',
	4 : 'src_col_desc',
	5 : 'src_col_type',
	6 : 'null_or_not',
	7 : "'Y' if src_col_name in tbl_pks else None",
	11: 'sa + self.__checkAbbr__(tbl_name)',
	12: 'self.__checkAbbr__(src_col_name)',
	14: 'tbl_desc',
	15: 'src_col_desc',
	16: 'self.__mapTdDataType__(src_col_type)',
	17: 'self.__mapSpDataType__(src_col_type)',
	18: 'null_or_not',
	19: "'Y' if src_col_name in tbl_pks else None",
	21: 'tgt_dflt_value',
	22: 'self.__formatDate__(src_col_type)',
	24: 'self.__checkCharSet__(src_col_type)'
}

'''readAbbrList will return the Abbr mapping list to shorten the table name and
   column name.

   The readAbbrList method can be customized with input, csv, json, or config
   files. Currently, using the method getCSV from DecodeConfig so that the 
   abbreviation list can be maintained by a configurable CSV file.
'''
def readAbbrList(csv_dir: str = '/conf/', csv_name: str = 'abbr_dict') -> dict:
	'''Return a dict stores the key-value as:
		{'Orignal_Name': 'Abbr_Name'}
	'''
	_abbr_list = {}
	csv_dir = PROJ_ROOT_DIR + csv_dir
	assert os.path.exists(csv_dir + csv_name + '.csv') is True, \
		   'Error: abbr_dict.csv does not exists!\n'

	abbr_config = DecodeConfig()
	csv_data = abbr_config.getCSV(csv_dir, csv_name)
	for row in csv_data:
		if not (row[0] in _abbr_list.keys()):
			_abbr_list[row[0]] = row[1].replace('\n','')
	
	return _abbr_list

ABBR_DICT = readAbbrList()

'''Oracle to Teradata type mapper AND
   Oracle to Spark-sql data type mapper
'''
ORA_2_TD = {
	"VARCHAR2": "VARCHAR",
	"NUMBER": "DECIMAL",
	"BLOB": "VARCHAR(4000)",
	"DATE": "TIMESTAMP(0)",
	"LONG": "VARCHAR(4000)"
}

ORA_2_SP = {
	"VARCHAR2": "STRING",
	"NUMBER": "DECIMAL", # maybe int, bigint, tinyint or so
	"BLOB": "STRING",
	"DATE": "TIMESTAMP",
	"LONG": "STRING"
}

'''Date format mapper
'''
DATE_FORMAT = {
	"DATE": "YYYY-MM-DD",
	"TIME(0)": "HH:MI:SS",
	"TIMESTAMP(0)": "YYYY-MM-DDbHH:MI:SS"
}


'''Add more DataMapper Variable after this comment.
'''
