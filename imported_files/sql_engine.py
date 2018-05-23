#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 15:20:57 2018

@author: florian
"""

from sqlalchemy import create_engine
import psycopg2 as psycopg2
import logging


def get_engine():
    return get_psql()


def get_psql():
    return create_engine(get_psql_connection())


def get_psql_connection():
    return 'postgresql://db:db@db.kiru.io/db'


def chunkify(lst, n):
    return [lst[i::n] for i in range(n)]


def import_into_db(df, table):
    csv = '../csv/%s.csv' % table
    df.to_csv(path_or_buf=csv, index=False, encoding='utf-8', na_rep='None')
    #import_csv(csv, df, table)


def import_csv(csv, df, table):
    con = psycopg2.connect(get_psql_connection())
    cur = con.cursor()
    f = open(csv)
    next(f)  # skpi header
    cur.copy_from(f, table, columns=tuple(df.columns.values), sep=",", null='None')
    con.commit()
