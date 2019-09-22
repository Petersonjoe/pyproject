# -*- coding: utf-8 -*-
#############################################
# @Author: jlei1
# @Date:   2019-08-27
# @Last Modified By:   jlei1
# @Last Modified Time: 2019-08-27
#############################################

from distutils.log import warn as printf

import sys, os

if '../' not in sys.path:
	sys.path.insert(0,'../')

from utils.AppRegister import register

DATA_TYPE_MAPPER = register()



