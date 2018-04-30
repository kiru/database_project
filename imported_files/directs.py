#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 15:20:57 2018

@author: florian
"""

import pandas as pd

from sql_engine import get_engine
from person import person_table


#read the data
path='../../../data/db2018imdb/directors.csv'
df = pd.read_csv(path)

#get the definition of the language table
print('Get the person name-id relation...')
dfp=person_table()

dftmp=df.iloc[0:5]
dfptmp=dfp.iloc[0:1000]

#replace all language strings with the corresponding id (EXPENSIVE)
print('Replace person name with id...')
dftmp['FullName']=dftmp['FullName'].str.encode('utf-8') #encode strings as unicode for accents etc.
dftmp['FullName']=dftmp['FullName'].replace(dfptmp['FULLNAME'].tolist(),dfptmp['PERSON_ID'].tolist())

print('Split entries with multi-clip data...')
dfsplit=pd.concat([pd.Series(row['FullName'],
                               [row['ClipIds'].split('|'),
                                row['Roles'].split('|'),
                                row['AddInfos'].split('|')]) for _, row in dftmp.iterrows()]).reset_index()
print('Rename columns...')
dfsplit.columns=['CLIP_ID','ROLE','ADDITIONAL_INFO','PERSON_ID']

print('Remove []-characters...')
dfsplit['CLIP_ID'] = dfsplit['CLIP_ID'].map(lambda x: x.lstrip('[').rstrip(']'))
dfsplit['ROLE'] = dfsplit['ROLE'].map(lambda x: x.lstrip('[').rstrip(']'))
dfsplit['ADDITIONAL_INFO'] = dfsplit['ADDITIONAL_INFO'].map(lambda x: x.lstrip('[').rstrip(']'))

#convert the integers to numbers
pd.to_numeric(dfsplit['CLIP_ID'],errors='coerce',downcast='integer')
dfsplit['CLIP_ID']=dfsplit['CLIP_ID'].astype('int64')

#give size of strings
rlengths=dfsplit['ROLE'].str.len()
alengths=dfsplit['ADDITIONAL_INFO'].str.len()
maxlenr=rlengths.sort_values(ascending=False).iloc[0]
maxlena=alengths.sort_values(ascending=False).iloc[0]
print('Maximum length of role is ',maxlenr)
print('Maximum length of additional info is ',maxlena)

#create engine and connect
engine=get_engine()
engine.connect()
#insert data into the DB
dfsplit.iloc[0:1].to_sql('DIRECTS', engine, if_exists='append',index=False)
