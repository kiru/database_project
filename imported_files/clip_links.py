#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 15:20:57 2018

@author: florian
"""

import pandas as pd

from sql_engine import get_engine

# read the data
path = '../../../data/db2018imdb/clip_links.csv'
df = pd.read_csv(path)
df.drop_duplicates(inplace=True)

# rename columns
df['CLIPLINK_ID'] = list(range(0, df.shape[0]))

df.columns = ['CLIP_FROM_ID', 'CLIP_TO_ID', 'LINK_TYPE', 'CLIPLINK_ID']  # use clip_id as genre_id here

# create engine and connect
engine = get_engine()
engine.connect()
# insert data into the DB
print('The final data shape is: ', df.shape)

df.to_sql('CLIPLINKS', engine, if_exists='append', index=False, chunksize=10000)
