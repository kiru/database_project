# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd

from sql_engine import get_engine


rating_path='../../../data/db2018imdb/ratings.csv'
df = pd.read_csv(rating_path)

#query about the relation
(rows,cols)=df.shape
print(df.columns)
print(df.dtypes)
print(df.shape)

#sort relation
#dfs=df.sort_values(by=['Rank','Votes'],ascending=False)
dfs=df

#rename columns and add rating_id
dfs.columns=['CLIP_ID','VOTES','RANK']
dfs['RATING_ID']=dfs.index
print(dfs)

#create engine and connect
engine=get_engine()
engine.connect()
#insert data into the DB
dfs.to_sql("CLIP_RATING", engine, if_exists='append',index=False)