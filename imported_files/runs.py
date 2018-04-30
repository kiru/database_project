#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 15:20:57 2018

@author: florian
"""

import pandas as pd

from sql_engine import get_engine
from country import country_table


#read the data
path='../../../data/db2018imdb/running_times.csv'
df = pd.read_csv(path)

#get the definition of the country table
dfl=country_table()

#replace all country strings with the corresponding id (EXPENSIVE)
df['ReleaseCountry']=df['ReleaseCountry'].replace(dfl['COUNTRYNAME'].tolist(),dfl['COUNTRY_ID'].tolist())

#rename columns
df.columns=['CLIP_ID','COUNTRY_ID','RUNNING_TIME']

#enforce numeric type
df['COUNTRY_ID']=pd.to_numeric(df['COUNTRY_ID'], errors='coerce')
df['RUNNING_TIME']=pd.to_numeric(df['RUNNING_TIME'], errors='coerce')

#create engine and connect
engine=get_engine()
engine.connect()
#insert data into the DB
df.iloc[0:1].to_sql('RUNS', engine, if_exists='append',index=False)
