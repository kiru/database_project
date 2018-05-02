#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 15:20:57 2018

@author: florian
"""

import pandas as pd
import re

from sql_engine import get_engine


def capt(x, reg=r"(?<=\')(.*?)(?=\')", ret=None):
    # Capture word between parantheses
    m = re.search(reg, x)
    if m:
        return m.group(1)
    elif ret:
        return ret
    else:
        return x


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
    path='../../../data/db2018imdb/biographies.csv'
    df5 = pd.read_csv(path, names=['FullName','RealName','Nickname','DateAndPlaceOfBirth',
    'Height','Biography','Biographer','DateAndCauseOfDeath','Spouse','Trivia','BiographicalBooks',
    'PersonalQuotes','Salary','Trademark','WhereAreTheyNow'],skiprows=1)
    
    print('Split spouse data...')
    #TODO: consider only the name in ' ' 
    df5['Spouse']=df5['Spouse'].fillna('[]')
    dfspouse=pd.concat([pd.Series(row['FullName'],
                                  row['Spouse'].split('|')) for _, row in df5.iterrows()]).reset_index()

    # print("AHAHSDF",dfspouse.head())
    dfspouse['index'] = dfspouse['index'].map(lambda x: x.lstrip('[').rstrip(']'))
    # print("SPOUSE\n",dfspouse['index'])

    # Get just the name
    dfspouse['index'] = dfspouse['index'].str.replace(r"\'\?\'", r"\'unknown'")
    dfspouse['index'] = dfspouse['index'].apply(lambda x: capt(x))

    print('Combine all persons...')
    dfall=df1['FullName'].append(df2['FullName'].append(df3['FullName'].append(df4['FullName'].append(df5['FullName']).append(dfspouse['index']))))
    print('Size of all person data combined: ',dfall.shape)
    # print("dd\n", dfall)
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
    df=person_table()
    #create engine and connect
    engine=get_engine()
    engine.connect()
    #insert data into the DB
#    df.iloc[0:1].to_sql('PERSON', engine, if_exists='append',index=False)

if __name__ == "__main__":
    main()