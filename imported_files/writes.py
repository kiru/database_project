#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 15:20:57 2018

@author: florian
"""

import pandas as pd

from sql_engine import *
from person import person_table, replace_name_id


def splitListToRows(row, row_accumulator, target_columns):

    rd = zip(*(row[c].split('|') for c in target_columns))

    for s in rd:
        new_row = row.to_dict()

        for c, v in zip(target_columns, s):
            new_row[c] = v

        row_accumulator.append(new_row)

# read the data
path = '../../../data/db2018imdb/writers.csv'
df = pd.read_csv(path)
print('Size of the "writes" table after import: ', df.shape)

# get the definition of the language table
print('Get the person name-id relation...')
# dfp=person_table()
dfp = pd.read_csv('PERSON.csv')

# replace all language strings with the corresponding id (EXPENSIVE)
nameSeries = pd.Series(dfp['PERSON_ID'].values, index=dfp['FULLNAME'])
df['FullName'] = df['FullName'].map(nameSeries)

print('Split entries with multi-clip data...')
new_rows = []
df.apply(splitListToRows, axis=1, args=(new_rows, ['ClipIds','WorkTypes','Roles','AddInfos']))
dfsplit = pd.DataFrame(new_rows)

print('Rename columns...')
dfsplit.columns = ['ADDITIONAL_INFO','CLIP_ID', 'PERSON_ID', 'ROLE', 'WORK_TYPE']

print('Remove []-characters...')
dfsplit['CLIP_ID'] = dfsplit['CLIP_ID'].map(lambda x: x.lstrip('[').rstrip(']'))
dfsplit['WORK_TYPE'] = dfsplit['WORK_TYPE'].map(lambda x: x.lstrip('[').rstrip(']'))
dfsplit['ROLE'] = dfsplit['ROLE'].map(lambda x: x.lstrip('[').rstrip(']'))
dfsplit['ADDITIONAL_INFO'] = dfsplit['ADDITIONAL_INFO'].map(lambda x: x.lstrip('[').rstrip(']'))

# convert the integers to numbers
pd.to_numeric(dfsplit['CLIP_ID'], errors='coerce', downcast='integer')
dfsplit['CLIP_ID'] = dfsplit['CLIP_ID'].astype('int64')

# give size of strings
wtlengths = dfsplit['WORK_TYPE'].str.len()
rlengths = dfsplit['ROLE'].str.len()
alengths = dfsplit['ADDITIONAL_INFO'].str.len()
maxlenwt = wtlengths.sort_values(ascending=False).iloc[0]
maxlenr = rlengths.sort_values(ascending=False).iloc[0]
maxlena = alengths.sort_values(ascending=False).iloc[0]
print('Maximum length of work type is ', maxlenwt)
print('Maximum length of role is ', maxlenr)
print('Maximum length of additional info is ', maxlena)

#dfsplit.rename(columns={'FullName': 'PERSON_ID'}, inplace=True)
dfsplit.drop_duplicates(inplace=True, subset=['PERSON_ID', 'CLIP_ID', 'ROLE'])
dfsplit['ROLE'].replace('', 'NA',inplace=True)

import_into_db(dfsplit, 'writes')
