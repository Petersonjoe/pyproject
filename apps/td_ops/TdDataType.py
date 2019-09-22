# -*- coding: utf-8 -*-
#############################################
# @Author: jlei1
# @Date:   2019-08-18
# @Last Modified By:   jlei1
# @Last Modified Time: 2019-08-18
#############################################

from distutils.log import warn as printf

# TD_DATA_TYPE is a dict that formatted as:
# Key: the short type name in Teradata
# ValueList: the possible data type in other databases
#            1st element is TD data type fullname
#            2nd element is spark-sql data type, details reference ./spark-sql-data-type-dict.png
#            None means will not convert
#            
# Key    TD type fullname    Spark-sql type
# BF     BYTE                byte

DATA_TYPE_MAPPER = {
	"A1": ["ARRAY", None],
	"AN": ["MULTI-DIMENSIONAL ARRAY", None],
	"AT": ["TIME", "timestamp"],
	"BF": ["BYTE", "byte"],
	"BO": ["BLOB", None],
	"BV": ["VARBYTE", "byte"],
	"CF": ["CHARACTER", "string"],
	"CO": ["CLOB", "string"],
	"CV": ["VARCHAR", "string"],
	"D": ["DECIMAL", "decimal"],
	"DA": ["DATE", "date"],
	"DH": ["INTERVAL DAY TO HOUR", None],
	"DM": ["INTERVAL DAY TO MINUTE", None],
	"DS": ["INTERVAL DAY TO SECOND", None],
	"DY": ["INTERVAL DAY", None],
	"F": ["FLOAT", "Float"],
	"HM": ["INTERVAL HOUR TO MINUTE", None],
	"HS": ["INTERVAL HOUR TO SECOND", None],
	"HR": ["INTERVAL HOUR", None],
	"I": ["INTEGER", "int"],
	"I1": ["BYTEINT", "int"],
	"I2": ["SMALLINT", "int"],
	"I8": ["BIGINT", "long"],
	"JN": ["JSON", None],
	"MI": ["INTERVAL MINUTE", None],
	"MO": ["INTERVAL MONTH", None],
	"MS": ["INTERVAL MINUTE TO SECOND", None],
	"N": ["NUMBER", "decimal"],
	"PD": ["PERIOD(DATE)", None],
	"PM": ["PERIOD(TIMESTAMP WITH TIME ZONE)", None],
	"PS": ["PERIOD(TIMESTAMP)", None],
	"PT": ["PERIOD(TIME)", None],
	"PZ": ["PERIOD(TIME WITH TIME ZONE)", None],
	"SC": ["INTERVAL SECOND", None],
	"SZ": ["TIMESTAMP WITH TIME ZONE", "timestamp"],
	"TS": ["TIMESTAMP", "timestamp"],
	"TZ": ["TIME WITH TIME ZONE", "timestamp"],
	"UT": ["UDT Type", None],
	"XM": ["XML", None],
	"YM": ["INTERVAL YEAR TO MONTH", None],
	"YR": ["INTERVAL YEAR", None],
	"++": ["TD_ANYTYPE", None]
}