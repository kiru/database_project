#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 15:20:57 2018

@author: florian
"""

import pandas as pd

from sql_engine import get_engine, get_engine_for_oracle

def language_table():
    #read the data
    genre_path='../../../data/db2018imdb/languages.csv'
    df = pd.read_csv(genre_path)
    
    #query about the relation
    (rows,cols)=df.shape
    print(df.columns)
    print(df.dtypes)
    print(df.shape)
    
    #select only unique entries
    dfu=df.drop_duplicates(subset=['Language'],keep='first')
    dfu['Language']=dfu['Language'].str.encode('utf-8') #encode strings as unicode for accents etc.
    print(dfu.shape)
    
    #reset the index and put it into ClipId
    dfi=dfu.reset_index(drop=True)
    dfi['ClipId']=dfi.index
    
    #find the maximum length of language
    lengths=df['Language'].str.len()
    maxlen=lengths.sort_values(ascending=False).iloc[0]
    print('Maximum length of title is ',maxlen)
    
    #rename columns
    dfi.columns=['LANGUAGE_ID','LANGUAGE'] #use clip_id as genre_id here
    print(dfi)
    
    return dfi
    
def main():
    #get table
    df=language_table()
    #create engine and connect
    engine=get_engine()
    engine.connect()
    #insert data into the DB
    df.to_sql('LANGUAGE', engine, if_exists='append',index=False)

if __name__ == "__main__":
    main()