#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 15:20:57 2018

@author: florian
"""


from sqlalchemy import create_engine
#import cx_Oracle

##oracle connection
#ip = 'diassrv2.epfl.ch'
#port = 1521
#SID = 'orcldias'
#dsn_tns = cx_Oracle.makedsn(ip, port, SID)
#db = cx_Oracle.connect('DB2018_G17', 'DB2018_G17', dsn_tns)

def get_engine():
    #sqlalchemy engine for connection
    oracle_connection_string = 'oracle+cx_oracle://{username}:{password}@{hostname}:{port}/{database}'
    engine = create_engine(
        oracle_connection_string.format(
            username='DB2018_G17',
            password='DB2018_G17',
            hostname='diassrv2.epfl.ch',
            port='1521',
            database='orcldias',
        )
    )
    return engine


