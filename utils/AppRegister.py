# -*- coding: utf-8 -*-
#############################################
# @Author: jlei1
# @Date:   2019-04-25
# @Last Modified By:   jlei1
# @Last Modified Time: 2019-08-27
#############################################

import sys
if '../' not in sys.path:
	sys.path.insert(0,'../')

from conf.app_list import APP_LIST
from importlib import import_module

def register(module_name: str = None):
	if module_name is None:
		return

	_imported_module = import_module(module_name)

	return _imported_module

