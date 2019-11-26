#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------#
# @Date    : 2019-11-10 16:35:47
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


#------------- ORM Test --------------#
#------------- create database engine --------------#
# for different database engine, please reference: https://www.cnblogs.com/lsdb/p/9835894.html
from sqlalchemy.engine import create_engine
engine = create_engine('sqlite:///foo.db?check_same_thread=False',echo=True)

#------------- define data model reflection --------------#
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Television(Base):
    """docstring for Television"""

    __tablename__ = 'dim_douban_tv'
    tv_id = Column(Integer,primary_key=True)
    tv_name = Column(String(512),nullable=False,index=True)
    tv_director = Column(String(512),nullable=True)
    tv_editor = Column(String(512),nullable=True)

    def __repr__(self):
        return f'<Television(tv_id={self.tv_id},tv_name={self.tv_name},tv_director={self.tv_director},tv_editor={self.tv_editor})>'

#------------- create data model --------------#
# show table detail
Television.__table__

# create data table
Base.metadata.create_all(engine)

#------------- CRUD operation --------------#
# create session
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)

# create a session instance
orm_session = Session()

# create a record
tv_sample = Television(
    tv_id=30401122,
    tv_name=
    )














