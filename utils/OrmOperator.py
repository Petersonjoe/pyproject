#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------#
# @Date    : 2019-11-05 22:20:49
# @Author  : jlei1 (jilei191@163.com)
# @Link    : github.com/Petersonjoe
#-------------------------------------------#

import sys
if '../../' not in sys.path:
	sys.path.insert(0, '../../')

print(sys.stdout.encoding)

# reassign the encode for strings
import codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

# Here should return a session that created by session maker
# then in app.douban.MovieDb, create Movie related data tables
# in app.douban.TvDb, create tv related data tables
# in app.douban.User, create user related data tables