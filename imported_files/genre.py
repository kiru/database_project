#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 15:20:57 2018

@author: florian
"""

import numpy as np
import pandas as pd
from sqlalchemy import create_engine

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
engine.connect()

#read the data
genre_path='../../../data/db2018imdb/genres.csv'
df = pd.read_csv(genre_path)

#query about the relation
(rows,cols)=df.shape
print(df.columns)
print(df.dtypes)
print(df.shape)

#select only unique entries
dfu=df.drop_duplicates(subset=['Genre'],keep='first')
print(dfu.shape)

#reset the index and put it into ClipId
dfi=dfunique.reset_index(drop=True)
dfi['ClipId']=dfi.index

#rename columns
dfi.columns=['GENRE_ID','GENRE'] #use clip_id as genre_id here
print(dfi)

#insert the sorted data into the DB
dfi.to_sql("GENRE", engine, if_exists='append',index=False)