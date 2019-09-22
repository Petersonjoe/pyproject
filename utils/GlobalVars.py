# -*- coding: utf-8 -*-
#############################################
# @Author: jlei1
# @Date:   2018-07-07
# @Last Modified By:   jlei1
# @Last Modified Time: 2018-07-20
#############################################

from distutils.log import warn as printf
import os, sys
''' Pathon的path与运行时文件位置绑定，很恶心，需要注意这一点
	os 模块的常用方法
	========================================================================================
	os.sep可以取代操作系统特定的路径分隔符。windows下为 “\\”
	os.name字符串指示你正在使用的平台。比如对于Windows，它是'nt'，而对于Linux/Unix用户，它是'posix'。
	os.getcwd()函数得到当前工作目录，即当前Python脚本工作的目录路径。
	os.getenv()获取一个环境变量，如果没有返回none
	os.putenv(key, value)设置一个环境变量值
	os.listdir(path)返回指定目录下的所有文件和目录名。
	os.remove(path)函数用来删除一个文件。
	os.system(command)函数用来运行shell命令。
	os.linesep字符串给出当前平台使用的行终止符。例如，Windows使用'\r\n'，Linux使用'\n'而Mac使用'\r'。
	os.curdir:返回当前目录（'.')
	os.chdir(dirname):改变工作目录到dirname
	========================================================================================
	os.path常用方法：
	os.path.isfile()和os.path.isdir()函数分别检验给出的路径是一个文件还是目录
	os.path.exists()函数用来检验给出的路径是否真地存在
	os.path.getsize(name):获得文件大小，如果name是目录返回0L
	os.path.abspath(name):获得绝对路径
	os.path.normpath(path):规范path字符串形式
	os.path.split(path) ：将path分割成目录和文件名二元组返回。
	os.path.splitext():分离文件名与扩展名
	os.path.join(path,name):连接目录与文件名或目录;使用“\”连接
	os.path.basename(path):返回文件名
	os.path.dirname(path):返回文件路径
	os.path.pardir: 当前目录的上一级目录
'''
from .ReadConfig import DecodeConfig

# 注意：这里不要使用任何OS模块相关的函数，因为会导致人“入口依赖”问题
# 例如，par_dir = os.getcwd().replace('\\','/')
# 如果调用的入口文件不在同一个层级，将会返回不同的文件路径
# 如果需要绝对路径，请使用魔术方法：__file__
# 以该文件为参照，获取项目根目录的绝对路径
CUR_ABS_DIR = os.path.split(__file__)[0]
PAR_ABS_DIR = '/'.join(CUR_ABS_DIR.split("\\")[0:-1])
PROJ_ROOT_DIR = PAR_ABS_DIR

# 获取stm的url列表
config_path = PROJ_ROOT_DIR + '/conf/'
config_name = 'global'
config = DecodeConfig()
url_file_loc = config.getConfig(filepath=config_path, filename=config_name)
URL_LIST = config.getCSV(filepath=PROJ_ROOT_DIR + url_file_loc['input_dirs']['stm'],filename=url_file_loc['input_files']['stm'])

# output 目录
OTPT_DIR = PROJ_ROOT_DIR + '/output/'






