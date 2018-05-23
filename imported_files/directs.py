#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 15:20:57 2018

@author: florian
"""

import pandas as pd

from sql_engine import *
from person import person_table, replace_name_id

def main():
    # read the data
    path = '../../../data/db2018imdb/directors.csv'
    df = pd.read_csv(path)
    print('Size of the "directs" table after import: ', df.shape)

    # get the definition of the language table
    print('Get the person name-id relation...')
    # dfp=person_table()
    dfp = pd.read_csv('PERSON.csv', encoding='utf-8')

    #df=df.iloc[0:10]

    # replace all language strings with the corresponding id (EXPENSIVE)
    print("start replacing person name with id.")

    nameSeries = pd.Series(dfp['PERSON_ID'].values, index=dfp['FULLNAME'])
    df['FullName'] = df['FullName'].map(nameSeries)
    print("done replacing person name with id")

    print('Split entries with multi-clip data...')
    print('Split ClipIds...')
    ids = df['ClipIds'].str.split('|', expand=True).stack()
    print('Split Roles...')
    roles = df['Roles'].str.split('|', expand=True).stack()
    print('Split AddInfos...')
    info = df['AddInfos'].str.split('|', expand=True).stack()
    dfsplit = pd.DataFrame(dict(ClipIds=ids, Roles=roles, AddInfos=info))
    print('Attach index...')
    dfsplit['FullName'] = dfsplit.index.labels[0]
    print('Map FullName...')
    dfsplit['FullName'] = dfsplit['FullName'].map(pd.Series(df['FullName']))

    #dfsplit = pd.concat([pd.Series(row['FullName'],
    #                               [row['ClipIds'].split('|'),
    #                                row['Roles'].split('|'),
    #                                row['AddInfos'].split('|')]) for _, row in df.iterrows()]).reset_index()
    
    print('Rename columns...')
    dfsplit.columns = ['ADDITIONAL_INFO', 'CLIP_ID', 'ROLE', 'PERSON_ID']
    
    print('Remove []-characters...')
    dfsplit['CLIP_ID'] = dfsplit['CLIP_ID'].map(lambda x: x.lstrip('[').rstrip(']'))
    dfsplit['ROLE'] = dfsplit['ROLE'].map(lambda x: x.lstrip('[').rstrip(']'))
    dfsplit['ADDITIONAL_INFO'] = dfsplit['ADDITIONAL_INFO'].map(lambda x: x.lstrip('[').rstrip(']'))
    
    # convert the integers to numbers
    pd.to_numeric(dfsplit['CLIP_ID'], errors='coerce', downcast='integer')
    dfsplit['CLIP_ID'] = dfsplit['CLIP_ID'].astype('int64')
    
    # give size of strings
    rlengths = dfsplit['ROLE'].str.len()
    alengths = dfsplit['ADDITIONAL_INFO'].str.len()
    
    maxlenr = rlengths.sort_values(ascending=False).iloc[0]
    maxlena = alengths.sort_values(ascending=False).iloc[0]
    print('Maximum length of role is ', maxlenr)
    print('Maximum length of additional info is ', maxlena)

    # rename columns
    dfsplit.rename(columns={'FullName': 'PERSON_ID'}, inplace=True)
    dfsplit.drop_duplicates(inplace=True, subset=['PERSON_ID', 'CLIP_ID', 'ROLE'])
    print('Final data: \n\n', df.head)

    #dfsplit.to_csv('DIRECTS.csv', index=False, encoding='utf-8')
    import_into_db(dfsplit, 'directs');

if __name__ == "__main__":
    main()
