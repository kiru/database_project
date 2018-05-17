#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 15:20:57 2018

@author: florian
"""

import pandas as pd

from sql_engine import *
from country import country_table

# read the data
path = '../../../data/db2018imdb/running_times.csv'
df = pd.read_csv(path)

# get the definition of the country table
dfl = country_table()

# replace all country strings with the corresponding id (EXPENSIVE)
df['ReleaseCountry'] = df['ReleaseCountry'].replace(dfl['COUNTRYNAME'].tolist(), dfl['COUNTRY_ID'].tolist())

# rename columns
df.columns = ['CLIP_ID', 'COUNTRY_ID', 'RUNNING_TIME']

# enforce numeric type
df['COUNTRY_ID'] = pd.to_numeric(df['COUNTRY_ID'], errors='coerce')
df['RUNNING_TIME'] = pd.to_numeric(df['RUNNING_TIME'], errors='coerce')

df.drop_duplicates(inplace=True, subset=['COUNTRY_ID', 'CLIP_ID'])
df.dropna(subset=['COUNTRY_ID'], inplace=True)

# Convert to number
pd.to_numeric(df['COUNTRY_ID'], errors='coerce', downcast='integer')
df['COUNTRY_ID'] = df['COUNTRY_ID'].astype(int)

# create engine and connect
import_into_db(df, 'runs')
