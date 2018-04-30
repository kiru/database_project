#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 15:20:57 2018

@author: florian
"""

import pandas as pd

from sql_engine import get_engine

def clip_table():
    #read the data
    genre_path='../../../data/db2018imdb/clips.csv'
    df = pd.read_csv(genre_path)
    
    #query about the relation
    (rows,cols)=df.shape
    print(df.columns)
    print(df.dtypes)
    print('The full data shape is: ',df.shape)
    
    #CLEANING
    #########
    #There is one duplicate  in all attributes but with different Ids (keep it!):
    #719315/719344  Jane's Journey    2010.0      NaN
    df_dup=df[df.duplicated(subset=['ClipTitle','ClipYear','ClipType'],keep=False)]
    df_dup.sort_values(by=['ClipTitle'],ascending=False)
    #TITLE: 
    #We accept all forms of titles except NaNs, but there are no
    print('Amount of NaNs in ClipTitle: ',df[df['ClipTitle'].isnull()].shape)
    df['ClipTitle']=df['ClipTitle'].str.encode('utf-8') #encode strings as unicode for accents etc.
    lengths=df['ClipTitle'].str.len()
    maxlen=lengths.sort_values(ascending=False).iloc[0]
    print('Maximum length of title is ',maxlen)
    #YEAR: 
    print('Amount of NaNs in ClipYear: ',df[df['ClipYear'].isnull()].shape)
    df_year=df.drop_duplicates(subset=['ClipYear'],keep='first')
    df_ys=df_year.sort_values(by=['ClipYear'],ascending=False)
    #covers 1888-2016, contains NaN: print(df_ys['ClipYear'])
    #TYPE: 
    print('Amount of NaNs in ClipType: ',df[df['ClipType'].isnull()].shape)
    df_type=df.drop_duplicates(subset=['ClipType'],keep='first')
    df_ts=df_type.sort_values(by=['ClipType'],ascending=False)
    #covers VG,V,TV,SE and NaN: print(df_ts['ClipType'])
    
    # NaNs are correctly transformed into NULL -> No need to manipulate the clips further
    
    #rename columns
    df.columns=['CLIP_ID','CLIP_TITLE','CLIP_YEAR','CLIP_TYPE']
    
    return df
    
def main():
    #get table
    df=clip_table()
    #create engine and connect
    #engine=get_engine()
    #engine.connect()
    #insert data into the DB
    print('The final data shape is: ',df.shape)
    #print('Part I...')
    #df.iloc[0:500000].to_sql('CLIP', engine, if_exists='append',index=False)
    #print('Part II...')
    #df.iloc[500000:1000000].to_sql('CLIP', engine, if_exists='append',index=False)
    #print('Part III...')
    #df.iloc[1000000:1500000].to_sql('CLIP', engine, if_exists='append',index=False)
    #print('Part IV...')
    #df.iloc[1500000:1736161].to_sql('CLIP', engine, if_exists='append',index=False)

    df.to_csv('clip.csv', index=False)
    
if __name__ == "__main__":
    main()
