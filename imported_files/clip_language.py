#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 15:20:57 2018

@author: florian
"""

import pandas as pd

from sql_engine import *
from language import language_table

# read the data
path = '../../../data/db2018imdb/languages.csv'
df = pd.read_csv(path)

# get the definition of the language table
dfl = language_table()

print('Langauge: ', df.head())

# replace all language strings with the corresponding id (EXPENSIVE)
#df['Language'] = df['Language'].str.encode('utf-8')  # encode strings as unicode for accents etc.
df['Language'] = df.Language.str.lower()

df['Language'] = df['Language'].replace(dfl['LANGUAGE'].tolist(), dfl['LANGUAGE_ID'].tolist())

# rename columns
df.columns = ['CLIP_ID', 'LANGUAGE_ID']  # use clip_id as genre_id here

df.drop_duplicates(inplace=True)
df.dropna(subset=['LANGUAGE_ID'], inplace=True)

pd.to_numeric(df['LANGUAGE_ID'], errors='coerce', downcast='integer')
df['LANGUAGE_ID'] = df['LANGUAGE_ID'].astype(int)

print('The final data shape is: \n', df.head())

# insert data into the DB
import_into_db(df, 'clip_language')
