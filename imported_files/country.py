#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 15:20:57 2018

@author: florian
"""

import pandas as pd

from sql_engine import get_engine

def country_table():
    #read the data
    genre_path='../../../data/db2018imdb/countries.csv'
    df = pd.read_csv(genre_path)

    #query about the relation
    (rows,cols)=df.shape
    print(df.columns)
    print(df.dtypes)
    print(df.shape)

    #select only unique entries
    dfu=df.drop_duplicates(subset=['CountryName'],keep='first')
    print(dfu.shape)

    #reset the index and put it into ClipId
    dfi=dfu.reset_index(drop=True)
    dfi['ClipId']=dfi.index

    #rename columns
    dfi.columns=['COUNTRY_ID','COUNTRYNAME'] #use clip_id as genre_id here
    print(dfi)

    return dfi

def main():
def main():
    #get table
    df=country_table()
    #create engine and connect
    engine=get_engine()
    engine.connect()
    #insert data into the DB
    df.to_sql('COUNTRY', engine, if_exists='append',index=False)

if __name__ == "__main__":
    main()
