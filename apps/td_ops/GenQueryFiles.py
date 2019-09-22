# -*- coding: utf-8 -*-
#############################################
# @Author: jlei1
# @Date:   2019-08-18
# @Last Modified By:   jlei1
# @Last Modified Time: 2019-09-22
#############################################

import os, sys
if '../../' not in sys.path:
	sys.path.insert(0, '../../')
from utils.ReadConfig import DecodeConfig
from utils.GlobalVars import PROJ_ROOT_DIR
from utils.TdConnector import TdConnector
# from .TdDataType import DATA_TYPE_MAPPER
from TdDataType import DATA_TYPE_MAPPER # for local test

import pandas as pd
import numpy as np

# set input
input_path = PROJ_ROOT_DIR + '/input/td_ops/'
output_path = PROJ_ROOT_DIR + '/output/td_ops/'
tmpl_path = PROJ_ROOT_DIR + '/templates/td_ops/'
cfg_path = PROJ_ROOT_DIR + '/conf/'
data_path = PROJ_ROOT_DIR + '/data/td_ops/'

input_file = ''
input_hd_metadata = ''
gen_tbl_file = ''
gen_dml_file = ''
gen_sel_sql_file = ''
gen_viw_file = ''
output_ddl_file = ''
output_dml_file = ''
output_sel_file = ''
output_viw_file = ''
pii_file = ''

table_list = open(input_path + input_file).readlines()
gen_tbl_tmpl = open(tmpl_path + gen_tbl_file).read()
dml_sql_tmpl = open(tmpl_path + gen_dml_file).read()
sel_sql_tmpl = open(tmpl_path + gen_sel_sql_file).read()
gen_viw_tmpl = open(tmpl_path + gen_viw_file).read()

cfg_file = 'global'
config = DecodeConfig()
td_cfg = config.getConfig(cfg_path,cfg_file)
host = td_cfg["td_config"]["host"]
username = td_cfg["td_config"]["username"]
password = td_cfg["td_config"]["password"]

conn = TdConnector(host, username, password)
conn.connect

os.system("del /F /Q " + output_path + "*")

def genTblFiles() -> None:
	ddl_tbl_file = open(output_path + output_ddl_file, 'w')
	for row in table_list:

		row = row.replace('\n','')
		row = row.split(' ')
		sa,database_name,table_name = row[0],row[1],row[2]
		dml_file = open(output_path + output_dml_file.format(DATABASE_NAME=database_name,TABLE_NAME=table_name), "w")
		sel_file = open(output_path + output_sel_file.format(DATABASE_NAME=database_name,TABLE_NAME=table_name), "w")

		conn._query = """
						SELECT ColumnName, 
						       ColumnType,
						       ColumnLength,
						       DecimalTotalDigits,
						       DecimalFractionalDigits
						  FROM dbc.COLUMNS
						 WHERE DATABASENAME='{db}' 
						   AND TABLENAME='{tbl}';
					  """.format(db=database_name, tbl=table_name)
		r_data = conn.querySql()

		# NaN/Null value clearing
		c = r_data.select_dtypes(np.number).columns
		r_data[c] = r_data[c].fillna(0)
		r_data = r_data.fillna("")

		rows,cols = r_data.shape

		column_list = ''
		column_ddl_list = ''
		for i in range(0, len(r_data)):

			column_list += r_data.iloc[i]["ColumnName"].strip() + ",\n"
			
			if isinstance(r_data.iloc[i]["DecimalTotalDigits"], str):
				dtd_flag = r_data.iloc[i]["DecimalTotalDigits"] != ""

			if isinstance(r_data.iloc[i]["DecimalTotalDigits"], np.number):
				dtd_flag = r_data.iloc[i]["DecimalTotalDigits"] > 0

			if isinstance(r_data.iloc[i]["DecimalFractionalDigits"], str):
				dfd_flag = r_data.iloc[i]["DecimalFractionalDigits"] != ""

			if isinstance(r_data.iloc[i]["DecimalFractionalDigits"], np.number):
				dfd_flag = r_data.iloc[i]["DecimalFractionalDigits"] > 0		

			if isinstance(r_data.iloc[i]["ColumnLength"], str):
				cl_flag = r_data.iloc[i]["ColumnLength"] != ""

			if isinstance(r_data.iloc[i]["ColumnLength"], np.number):
				cl_flag = r_data.iloc[i]["ColumnLength"] > 0

			dcml_flag = r_data.iloc[i]["ColumnType"].strip() == "D"

			if dcml_flag:
				if dfd_flag and dtd_flag:
					row_string = r_data.iloc[i]["ColumnName"].strip() + " " \
					           + DATA_TYPE_MAPPER[r_data.iloc[i]["ColumnType"].strip()][1] \
					           + "(" + str(int(r_data.iloc[i]["DecimalTotalDigits"])).strip() + "," \
					           + str(int(r_data.iloc[i]["DecimalFractionalDigits"])).strip() + "),\n"
				else:
					row_string = r_data.iloc[i]["ColumnName"].strip() + " " \
					           + DATA_TYPE_MAPPER[r_data.iloc[i]["ColumnType"].strip()][1] \
					           + "(" + str(int(r_data.iloc[i]["DecimalTotalDigits"])).strip() + "),\n"
			else:
				row_string = r_data.iloc[i]["ColumnName"].strip() + " " \
				           + DATA_TYPE_MAPPER[r_data.iloc[i]["ColumnType"].strip()][1] + ",\n"

			column_ddl_list += row_string

		column_list = column_list[0:len(column_list)-2]
		column_ddl_list = column_ddl_list[0:len(column_ddl_list)-2]
		filled_ddl_query = gen_tbl_tmpl.format(SA=sa, DATABASE_NAME=database_name, TABLE_NAME=table_name, COLUMN_LIST=column_ddl_list)
		filled_dml_query = dml_sql_tmpl.format(COLUMN_LIST=column_ddl_list)
		filled_sel_query = sel_sql_tmpl.format(COLUMN_LIST=column_list)

		dml_file.write(filled_dml_query + '\n')
		sel_file.write(filled_sel_query + '\n')
		ddl_file.write(filled_ddl_query + '\n')
		ddl_file.write('-----------------------------------------\n\n')

		dml_file.close()
		sel_file.close()

	ddl_tbl_file.close()

def genViwFiles() -> None:
	ddl_viw_file = open(output_path + output_viw_file, "w")
	pii_data = pd.read_csv(cfg_path+pii_file, sep=",", header=0)
	
	for row in table_list:

		row = row.replace('\n','')
		row = row.split(' ')
		sa,database_name,table_name,view_name = row[0],row[1],row[2],row[3]

		# fetch TD column info
		conn._query = """
						SELECT ColumnName, 
						       ColumnType,
						       ColumnLength,
						       DecimalTotalDigits,
						       DecimalFractionalDigits
						  FROM dbc.COLUMNS
						 WHERE DATABASENAME='{db}' 
						   AND TABLENAME='{tbl}';
					  """.format(db=database_name, tbl=table_name)
		r_data = conn.querySql()

		# NaN/Null value clearing
		c = r_data.select_dtypes(np.number).columns
		r_data[c] = r_data[c].fillna(0)
		r_data = r_data.fillna("")

		rows,cols = r_data.shape

		# get the TIME type column list
		time_cols = r_data[r_data.ColumnType == "AT"]
		td_time_cols = [i.strip().lower() for i in time_cols.ColumnName.tolist()]

		# load hadoop column info
		metadata = pd.read_csv(data_path + input_hd_metadata.format(DATABASE_NAME=database_name, TABLE_NAME=table_name),
		            sep=';',
		            header=None, 
		            names=["ColumnName", "ColumnType"])
		# print(metadata)
		hd_col_list = [i.strip().lower() for i in metadata.ColumnName.tolist()]
		
		column_list = ''
		orig_col_list = ''
		for i in range(0, len(metadata)):
			column_name = metadata.iloc[i]["ColumnName"].strip().lower()
			column_type = metadata.iloc[i]["ColumnType"].strip().lower()
			pii_cnt = pii_data.loc[(pii_data.table_name==table_name) & (pii_data.column_name==column_name)]

			if (view_name.lower() == "access_views") and (len(pii_cnt) > 0):
				print(view_name.lower(), len(pii_cnt))
			else:
				orig_col_list += column_name + ",\n"

				if (column_name in td_time_cols) and \
				   (column_name[-3:len(column_name)] == '_tm') and \
				   ((column_name[0:-3] + '_dt') in hd_col_list) and \
				   (column_type == "string"):
					column_list += "cast(concat(" + column_name[0:-3] + "_dt" + ", ' ', " + column_name +") as timestamp) as " + column_name + ",\n"
				else:
					column_list += column_name + ",\n"

		column_list = column_list[0:len(column_list)-2]
		orig_col_list = orig_col_list[0:len(orig_col_list)-2]
		filled_viw_query = gen_viw_tmpl.format(DATABASE_NAME=database_name,TABLE_NAME=table_name, VIEW_NAME=view_name, COLUMN_LIST=column_list, ORIG_COLUMN_LIST=orig_col_list)
		ddl_viw_file.write(filled_viw_query + '\n')
		ddl_viw_file.write('-----------------------------------------\n\n')

	ddl_viw_file.close()


if __name__ == '__main__':
	# import pdb; pdb.set_trace()
	genViwFiles()
