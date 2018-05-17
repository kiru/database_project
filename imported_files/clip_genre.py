#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 15:20:57 2018

@author: florian
"""

import pandas as pd

from sql_engine import get_engine
from genre import genre_table

# read the data
path = '../../../data/db2018imdb/genres.csv'
df = pd.read_csv(path)

# get the definition of the genre table
dfl = genre_table()

df.drop_duplicates(inplace=True)

# replace all language strings with the corresponding id (EXPENSIVE)
df['Genre'] = df['Genre'].replace(dfl['GENRE'].tolist(), dfl['GENRE_ID'].tolist())

# rename columns
df.columns = ['CLIP_ID', 'GENRE_ID']  # use clip_id as genre_id here

# create engine and connect
engine = get_engine()
engine.connect()
# insert data into the DB
df.to_sql('CLIP_GENRE', engine, if_exists='append', index=False)
