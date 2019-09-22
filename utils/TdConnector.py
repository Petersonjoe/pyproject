# -*- coding: utf-8 -*-
#############################################
# @Author: jlei1
# @Date:   2019-08-18
# @Last Modified By:   jlei1
# @Last Modified Time: 2019-09-10
#############################################

from distutils.log import warn as printf

import teradata
import pandas as pd

udaExec = teradata.UdaExec(appName="test", version="1.0", logConsole=False)

class TdConnector(object):
	"""
	TdConnector
		Create a instance: connector = TdConnector(host, user, pwd)
	    Methods:
	        connect: a property that connect to a TD instance
	        querySql(): a method will return a pandas dataframe
	"""
	_drivername = 'Teradata Database ODBC Driver 16.20'
	_connected = None
	_query = None

	def __init__(self, host: str = None, username: str = None, password: str = None) -> None:
		super(TdConnector, self).__init__()
		self.host = host
		self.username = username
		self.password = password
		
	@property
	def connect(self):
		try:
			_connect = udaExec.connect(
									method="odbc",
									system=self.host,
									username=self.username,
									password=self.password,
									driver=self._drivername
								)
		except Exception as e:
			print("FATAL ERROR: TD connection FAILED!")
			raise e
		self._connected = _connect

		return 0

	def querySql(self):
		if self._query is None:
			print("""WARNING: Please set the sql query for executing.
					          Examples: connector = TdConnector(host, user, pwd)
					                    connector._query = "select * from tablename"
				  """)
			return 0

		_df = pd.read_sql(self._query, self._connected)

		return _df


# if __name__ == '__main__':
# 	connector = TdConnector(host, username, password)
# 	connector.connect
# 	connector._query = """
# 				SELECT ColumnName, 
# 					   ColumnType,
# 					   ColumnLength,
# 					   DecimalTotalDigits,
# 					   DecimalFractionalDigits
# 				  FROM dbc.COLUMNS
# 				 WHERE databasename='GDW_TABLES' 
# 				   AND TABLENAME='PYMT_MTHD_TYPE_LKP';
# 			"""
# 	r_data = connector.querySql()

# 	print(r_data)

