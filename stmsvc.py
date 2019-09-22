# -*- coding: utf-8 -*-
#############################################
# @Author: jlei1
# @Date:   2018-06-26 21:29:51
# @Last Modified By:   jlei1
# @Last Modified Time: 2019-09-22
#############################################
import os, sys
from distutils.log import warn as printf
from apps.stm.TemplateOperation import setTemplate
from apps.stm.TemplateOperation import TemplateOperations
from apps.tbl_usage.OwnerSearch import ownerSearch
from apps.td_ops.GenQueryFiles import genTblFiles, genViwFiles
from utils.GlobalVars import URL_LIST, OTPT_DIR

usage_message = '''
\nUsage: python {f_name} func_name para_list
\nfunc_name
\tstm        generate stm file and then review with DA
\ttbl_usage  check batch owner email list
\ttd_ops     extract Teradata meta data to generate dml/sql/ddl files
\nexample
\tpython {f_name} stm pymt
\tpython {f_name} tbl_usage
\tpython {f_name} td_ops
\nNote: output usually can be found in directory ./output/func_name/
'''

def cleanTmpFolder(tPth: str = OTPT_DIR, subFolderName: str = None) -> None:
	
	tmp_path = tPth + subFolderName
	if (not subFolderName) or (not os.path.exists(tmp_path)):
		print('\t*** Warn: directory or file not exists! ***\n')
		return
	else:
		_ = [os.remove(tmp_path + fp) for fp in os.listdir(tmp_path)]	
	return

def getStmXls(replTmpl: bool = False, SA: str = None) -> None:
	assert (SA is not None),'*** Warn: SA does not set! ***\n'

	if replTmpl:
		setTemplate(replaceOld=True)

	for url in URL_LIST:
		tmpl_obj = TemplateOperations()
		tmpl_obj.tmplWrite(url=url[0], sa=SA)

	return

def usage(name: str = None) -> None:
	print(usage_message.format(f_name=name))


if __name__ == '__main__':

	_file_name = sys.argv[0].split('\\')[-1]
	
	if len(sys.argv) <= 1:
		usage(_file_name)
	else:
		func_name = sys.argv[1].lower()
		
		if func_name.lower() == 'stm':
			try:
				sa_name = sys.argv[2].lower()
				cleanTmpFolder(subFolderName=func_name+'/tmp/')
				getStmXls(SA=sa_name)
			except Exception as e:
				usage(_file_name)
				raise e
			
		elif func_name.lower() == 'tbl_usage':
			try:
				ownerSearch()
			except Exception as e:
				usage(_file_name)
				raise e
		
		elif func_name.lower() == 'td_ops':
			try:
				generateQueryFiles()
			except Exception as e:
				raise e

# import pdb; pdb.set_trace()
# ownerSearch()