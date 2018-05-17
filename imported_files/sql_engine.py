#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 15:20:57 2018

@author: florian
"""

from sqlalchemy import create_engine
import logging

import os

os.environ["NLS_LANG"] = ".UTF8"


# import cx_Oracle

##oracle connection
# ip = 'diassrv2.epfl.ch'
# port = 1521
# SID = 'orcldias'
# dsn_tns = cx_Oracle.makedsn(ip, port, SID)
# db = cx_Oracle.connect('DB2018_G17', 'DB2018_G17', dsn_tns)

def get_engine():
    return get_psql()


def get_psql():
    return create_engine('postgresql://db:db@db.kiru.io/db')


def get_engine_for_oracle():
    # sqlalchemy engine for connection
    # so that we see the sql statements
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    engine = create_engine(
        get_oracle_connection()
    )
    return engine


def get_engine_for_oracle_own():
    # sqlalchemy engine for connection
    # so that we see the sql statements
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    engine = create_engine(
        get_oracle_connection_own()
    )
    return engine


def get_engine_for_oracle_localhost():
    # sqlalchemy engine for connection
    # so that we see the sql statements
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    engine = create_engine(
        'oracle+cx_oracle://{username}:{password}@{hostname}:{port}/{database}'.format(
            username='system',
            password='oracle',
            hostname='localhost',
            port='49161',
            database='xe',
        ))
    return engine


def get_oracle_connection():
    oracle_connection_string = 'oracle+cx_oracle://{username}:{password}@{hostname}:{port}/{database}'
    return oracle_connection_string.format(
        username='DB2018_G17',
        password='DB2018_G17',
        hostname='diassrv2.epfl.ch',
        port='1521',
        database='orcldias',
    )


def get_oracle_connection_own():
    oracle_connection_string = 'oracle+cx_oracle://{username}:{password}@{hostname}:{port}/{database}'
    return oracle_connection_string.format(
        username='db',
        password='db',
        hostname='db.kiru.io',
        port='49161',
        database='XE',
    )


def chunkify(lst, n):
    return [lst[i::n] for i in range(n)]
