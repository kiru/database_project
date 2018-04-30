#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 15:20:57 2018

@author: florian
"""

import pandas as pd

from sql_engine import get_engine


#read the data
path='../../../data/db2018imdb/clip_links.csv'
df = pd.read_csv(path)

#rename columns
df.columns=['CLIP_FROM_ID','CLIP_TO_ID','LINK_TYPE'] #use clip_id as genre_id here

#create engine and connect
engine=get_engine()
engine.connect()
#insert data into the DB
print('The final data shape is: ',df.shape)
print('Part I...')
df.iloc[0:500000].to_sql('CLIPLINKS', engine, if_exists='append',index=False)
print('Part II...')
df.iloc[500000:921024].to_sql('CLIPLINKS', engine, if_exists='append',index=False)