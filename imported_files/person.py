#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 15:20:57 2018

@author: florian
"""

import pandas as pd

from sql_engine import get_engine

def person_table():
    #read the data
    path='../../../data/db2018imdb/actors.csv'
    df1 = pd.read_csv(path)
    path='../../../data/db2018imdb/directors.csv'
    df2 = pd.read_csv(path)
    path='../../../data/db2018imdb/producers.csv'
    df3 = pd.read_csv(path)
    path='../../../data/db2018imdb/writers.csv'
    df4 = pd.read_csv(path)
    
    dfall=df1['FullName'].append(df2['FullName'].append(df3['FullName'].append(df4['FullName'])))
    print('Size of all person data combined: ',dfall.shape)
    
    #select only unique entries
    dfu=dfall.drop_duplicates(keep='first')
    print('Size of unique person data: ',dfu.shape)
    
    #sort relation, encode as utf-8, find longest string
    dfs=dfu.sort_values(ascending=True).str.encode('utf-8')
    lengths=dfs.str.len()
    maxlen=lengths.sort_values(ascending=False).iloc[0]
    print('Maximum length of fullname is ',maxlen)
    
    #reset the index and put it into ClipId
    dfi=dfs.reset_index(drop=True)
    df = pd.DataFrame(data={'PERSON_ID':dfi.index,'FULLNAME':dfs})
    
    return df

def main():
    #create engine and connect
    engine=get_engine()
    engine.connect()
    #insert data into the DB
    df.iloc[0:1].to_sql('PERSON', engine, if_exists='append',index=False)

if __name__ == "__main__":
    main()