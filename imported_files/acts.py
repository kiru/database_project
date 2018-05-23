#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 15:20:57 2018

@author: florian
"""

import numpy as np
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
path = '../../../data/db2018imdb/actors.csv'
df = pd.read_csv(path)
print('Size of the "acts" table after import: ', df.shape)

# get the definition of the language table
print('Get the person name-id relation...')
# dfp=person_table()
dfp = pd.read_csv('PERSON.csv')

# replace all language strings with the corresponding id (EXPENSIVE)
print('Replace person name with id...')

nameSeries = pd.Series(dfp['PERSON_ID'].values, index=dfp['FULLNAME'])
df['FullName'] = df['FullName'].map(nameSeries)

print('Split entries with multi-clip data...')
new_rows = []
df.apply(splitListToRows, axis=1, args=(new_rows, ['ClipIds', 'Chars', 'OrdersCredit', 'AddInfos']))
dfsplit = pd.DataFrame(new_rows)

print('Rename columns...')
dfsplit.columns = ['ADDITIONAL_INFO', 'CHARACTER', 'CLIP_ID', 'PERSON_ID','ORDERS_CREDIT']

print('Remove []-characters...')

dfsplit['CLIP_ID'] = dfsplit['CLIP_ID'].map(lambda x: x.lstrip('[').rstrip(']'))
dfsplit['CHARACTER'] = dfsplit['CHARACTER'].map(lambda x: x.lstrip('[').rstrip(']'))
dfsplit['ORDERS_CREDIT'] = dfsplit['ORDERS_CREDIT'].map(lambda x: x.lstrip('[').rstrip(']'))
dfsplit['ADDITIONAL_INFO'] = dfsplit['ADDITIONAL_INFO'].map(lambda x: x.lstrip('[').rstrip(']'))

# convert the integers to numbers
pd.to_numeric(dfsplit['CLIP_ID'], errors='coerce', downcast='integer')
dfsplit['ORDERS_CREDIT'] = dfsplit['ORDERS_CREDIT'].replace('', np.nan, regex=True)
pd.to_numeric(dfsplit['ORDERS_CREDIT'], errors='coerce', downcast='float')
dfsplit['CLIP_ID'] = dfsplit['CLIP_ID'].astype('int64')
dfsplit['ORDERS_CREDIT'] = dfsplit['ORDERS_CREDIT'].astype('float')

# give size of strings
clengths = dfsplit['CHARACTER'].str.len()
alengths = dfsplit['ADDITIONAL_INFO'].str.len()
maxlenc = clengths.sort_values(ascending=False).iloc[0]
maxlena = alengths.sort_values(ascending=False).iloc[0]
print('Maximum length of character is ', maxlenc)
print('Maximum length of additional info is ', maxlena)

dfsplit.rename(columns={'FullName': 'PERSON_ID'}, inplace=True)
dfsplit.drop_duplicates(inplace=True, subset=['PERSON_ID', 'CLIP_ID', 'CHARACTER'])

# TODO KIRU: I'm not sure if this is correct, and how many we get rid of
dfsplit.dropna(subset=['CHARACTER'], inplace=True)

import_into_db(dfsplit, 'acts')
