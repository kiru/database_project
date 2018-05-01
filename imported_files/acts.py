#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 15:20:57 2018

@author: florian
"""

import numpy as np
import pandas as pd

from sql_engine import get_engine
from person import person_table


#read the data
path='../../../data/db2018imdb/actors.csv'
df = pd.read_csv(path)

#get the definition of the language table
print('Get the person name-id relation...')
dfp=person_table()

#replace all language strings with the corresponding id (EXPENSIVE)
print('Replace person name with id...')
df['FullName']=df['FullName'].str.encode('utf-8') #encode strings as unicode for accents etc.
df['FullName']=df['FullName'].replace(dfp['FULLNAME'].tolist(), dfp['PERSON_ID'].tolist())

print('Split entries with multi-clip data...')
dfsplit=pd.concat([pd.Series(row['FullName'],
                               [row['ClipIds'].split('|'),
                                row['Chars'].split('|'),
                                row['OrdersCredit'].split('|'),
                                row['AddInfos'].split('|')]) for _, row in df.iterrows()]).reset_index()
print('Rename columns...')
dfsplit.columns=['CLIP_ID','CHARACTER','ORDERS_CREDIT','ADDITIONAL_INFO','PERSON_ID']

print('Remove []-characters...')
dfsplit['CLIP_ID'] = dfsplit['CLIP_ID'].map(lambda x: x.lstrip('[').rstrip(']'))
dfsplit['CHARACTER'] = dfsplit['CHARACTER'].map(lambda x: x.lstrip('[').rstrip(']')).str.encode('utf-8')
dfsplit['ORDERS_CREDIT'] = dfsplit['ORDERS_CREDIT'].map(lambda x: x.lstrip('[').rstrip(']'))
dfsplit['ADDITIONAL_INFO'] = dfsplit['ADDITIONAL_INFO'].map(lambda x: x.lstrip('[').rstrip(']')).str.encode('utf-8')

#convert the integers to numbers
pd.to_numeric(dfsplit['CLIP_ID'],errors='coerce',downcast='integer')
dfsplit['ORDERS_CREDIT'] = dfsplit['ORDERS_CREDIT'].replace('', np.nan, regex=True)
pd.to_numeric(dfsplit['ORDERS_CREDIT'],errors='coerce',downcast='float')
dfsplit['CLIP_ID']=dfsplit['CLIP_ID'].astype('int64')
dfsplit['ORDERS_CREDIT']=dfsplit['ORDERS_CREDIT'].astype('float')

#give size of strings
clengths=dfsplit['CHARACTER'].str.len()
alengths=dfsplit['ADDITIONAL_INFO'].str.len()
maxlenc=clengths.sort_values(ascending=False).iloc[0]
maxlena=alengths.sort_values(ascending=False).iloc[0]
print('Maximum length of character is ',maxlenc)
print('Maximum length of additional info is ',maxlena)


#create engine and connect
engine=get_engine()
engine.connect()
#insert data into the DB
dfsplit.to_sql('ACTS', engine, if_exists='append',index=False,chunksize=1000)