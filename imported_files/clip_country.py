#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 15:20:57 2018

@author: florian
"""

import pandas as pd

from joblib import Parallel, delayed
from sql_engine import get_engine, chunkify
from country import country_table

def processInput(chunk):
    engine=get_engine()
    engine.connect()
    print("Insert next chunk")
    chunk.to_sql('CLIP_COUNTRY', engine, if_exists='append',index=False, chunksize=1)
    engine.dispose()
    return chunk

def main():
    #read the data
    path='../../../data/db2018imdb/countries.csv'
    df = pd.read_csv(path)

    #get the definition of the country table
    dfl=country_table()

    #replace all country strings with the corresponding id (EXPENSIVE)
    df['CountryName']=df['CountryName'].replace(dfl['COUNTRYNAME'].tolist(),dfl['COUNTRY_ID'].tolist())

    #rename columns
    df.columns=['CLIP_ID','COUNTRY_ID']
    df.drop_duplicates(inplace=True)

    print('Import')
    results = Parallel(n_jobs=9)(delayed(processInput)(chunk) for chunk in chunkify(df, 10000))


if __name__ == "__main__":
    main()


