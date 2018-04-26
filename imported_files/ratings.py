# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import pandas as pd
#import cx_Oracle
from sqlalchemy import create_engine

##oracle connection
#ip = 'diassrv2.epfl.ch'
#port = 1521
#SID = 'orcldias'
#dsn_tns = cx_Oracle.makedsn(ip, port, SID)
#db = cx_Oracle.connect('DB2018_G17', 'DB2018_G17', dsn_tns)

#sqlalchemy engine
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
engine.connect()


#cursor =db.cursor()
#cursor.execute("SELECT C.country_id, C.countryname FROM country C WHERE C.countryname='Germany' OR C.countryname='Switzerland'")
#tables = cursor.fetchall()

rating_path='../../../data/db2018imdb/ratings.csv'
df = pd.read_csv(rating_path)

#query about the relation
(rows,cols)=df.shape
print(df.columns)
print(df.dtypes)
print(df.shape)

#sort relation
dfs=df.sort_values(by=['Rank','Votes'],ascending=False)

#rename columns and add rating_id
dfs.columns=['CLIP_ID','VOTES','RANK']
dfs['RATING_ID']=dfs.index
print(dfs)

#insert the sorted data into the DB
#dfs.to_sql("CLIP_RATING", engine, if_exists='append',index=False)