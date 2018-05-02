#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 15:20:57 2018

@author: florian
"""

import pandas as pd

from sql_engine import get_engine
from person import person_table,replace_name_id


#read the data
path='../../../data/db2018imdb/directors.csv'
df = pd.read_csv(path)
print('Size of the "directs" table after import: ', df.shape)

#get the definition of the language table
print('Get the person name-id relation...')
dfp=person_table()

#replace all language strings with the corresponding id (EXPENSIVE)
print('Replace person name with id...')
df['FullName']=df['FullName'].str.encode('utf-8') #encode strings as unicode for accents etc.
#df['FullName']=df['FullName'].replace(dfp['FULLNAME'].tolist(),dfp['PERSON_ID'].tolist())
df=df.sort_values(by=['FullName'],ascending=True) #sort the values by name to make replace work
df['FullName']=replace_name_id(df['FullName'],dfp['FULLNAME'].tolist(),dfp['PERSON_ID'].tolist())

print('Split entries with multi-clip data...')
dfsplit=pd.concat([pd.Series(row['FullName'],
                               [row['ClipIds'].split('|'),
                                row['Roles'].split('|'),
                                row['AddInfos'].split('|')]) for _, row in df.iterrows()]).reset_index()
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
dfsplit.to_sql('DIRECTS', engine, if_exists='append',index=False)
