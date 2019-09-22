# # -*- coding: utf-8 -*-
# #############################################
# # @Author: jlei1
# # @Date:   2018-06-26 20:47:25
# # @Last Modified By:   jlei1
# # @Last Modified Time: 2019-09-22
# # @Description: STYLE: single quote in function header, otherwise, double quote
# #############################################

# from distutils.log import warn as printf
import os, sys

if './' not in sys.path:
	sys.path.insert(0,'./')

# from utils.ReadConfig import DecodeConfig



# ###################################################################################
# # below is a sample test of merge cells with style
# from openpyxl.styles import Border, Side, PatternFill, Font, GradientFill, Alignment
# from openpyxl import Workbook

# def style_range(ws, cell_range, border=Border(), fill=None, font=None, alignment=None):
#     """
#     Apply styles to a range of cells as if they were a single cell.

#     :param ws:  Excel worksheet instance
#     :param range: An excel range to style (e.g. A1:F20)
#     :param border: An openpyxl Border
#     :param fill: An openpyxl PatternFill or GradientFill
#     :param font: An openpyxl Font object
#     """

#     top = Border(top=border.top)
#     left = Border(left=border.left)
#     right = Border(right=border.right)
#     bottom = Border(bottom=border.bottom)

#     first_cell = ws[cell_range.split(":")[0]]
#     if alignment:
#         ws.merge_cells(cell_range)
#         first_cell.alignment = alignment

#     rows = ws[cell_range]
#     if font:
#         first_cell.font = font

#     for cell in rows[0]:
#         cell.border = cell.border + top
#     for cell in rows[-1]:
#         cell.border = cell.border + bottom

#     for row in rows:
#         l = row[0]
#         r = row[-1]
#         l.border = l.border + left
#         r.border = r.border + right
#         if fill:
#             for c in row:
#                 c.fill = fill

# wb = Workbook()
# ws = wb.active
# my_cell = ws['B2']
# my_cell.value = "My Cell"
# thin = Side(border_style="thin", color="000000")
# double = Side(border_style="double", color="ff0000")

# border = Border(top=double, left=thin, right=thin, bottom=double)
# fill = PatternFill("solid", fgColor="DDDDDD")
# fill = GradientFill(stop=("000000", "FFFFFF"))
# font = Font(b=True, color="FF0000")
# al = Alignment(horizontal="center", vertical="center")

# style_range(ws, 'B2:F4', border=border, fill=fill, font=font, alignment=al)
# wb.save("styled.xlsx")


# ###################################################################################

print(__file__.split('\\')[-1])

import unittest
import numpy as np
import pandas as pd
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)

from utils.ReadConfig import DecodeConfig
from utils.GlobalVars import PROJ_ROOT_DIR
from utils.TdConnector import TdConnector
from apps.td_ops.TdDataType import DATA_TYPE_MAPPER

cfg_path = PROJ_ROOT_DIR + "/conf/"
cfg_file = "global"
pii_file = "mozart_pii.csv"
config = DecodeConfig()
td_cfg = config.getConfig(cfg_path,cfg_file)
host = td_cfg["td_config"]["host"]
username = td_cfg["td_config"]["username"]
password = td_cfg["td_config"]["password"]

def test_hd_meta_data():
	# get hd metadata
	metadata = pd.read_csv("./data/td_ops/database.table_name.metadata.csv",
		                sep=";",
		                header=None, 
		                names=["ColumnName", "ColumnType"])
	print(metadata)

	# get td metadata
	conn = TdConnector(host, username, password)
	conn.connect

	conn._query = """
					SELECT ColumnName, 
					       ColumnType,
					       ColumnLength,
					       DecimalTotalDigits,
					       DecimalFractionalDigits
					  FROM dbc.COLUMNS
					 WHERE DATABASENAME='gdw_tables' 
					   AND TABLENAME='dw_ems_cart_hist';
				"""
	r_data = conn.querySql()

	# NaN/Null value clearing
	c = r_data.select_dtypes(np.number).columns
	r_data[c] = r_data[c].fillna(0)
	r_data = r_data.fillna("")

	# "AT": ["TIME", "timestamp"],
	# "PT": ["PERIOD(TIME)", None],
	# "PZ": ["PERIOD(TIME WITH TIME ZONE)", None],
	td_time_cols = r_data[r_data.ColumnType == "AT"]
	time_cols = [i.strip().lower() for i in time_cols.tolist()]

def test_pii_flag():
	pii_data = pd.read_csv(cfg_path+pii_file, sep=",", header=0)
	print(pii_data)
	pii_cnt = pii_data.loc[(pii_data.table_name=="table_name") & (pii_data.column_name=="column_name")]
	print(len(pii_col_list))


if __name__ == '__main__':
	# test_hd_meta_data()
	test_pii_flag()


