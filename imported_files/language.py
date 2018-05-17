#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 15:20:57 2018

@author: florian
"""

import pandas as pd
import re

from sql_engine import *


def capt(x):
    # Capture word between parantheses
    m = re.search(r"(?<=\()(.*?)(\sversion)?(\sonly)?(?=\))", x)
    if m:
        return m.group(1)
    else:
        return x


def language_table():
    # read the data
    genre_path = '../../../data/db2018imdb/languages.csv'
    df = pd.read_csv(genre_path)

    # query about the relation
    (rows, cols) = df.shape
    print(df.columns)
    print(df.dtypes)
    print(df.shape)

    # select only unique entries
    dfu = df.drop_duplicates(subset=['Language'], keep='first')

    dfu['Language'] = dfu.Language.str.lower()
    dfu['Language'] = dfu['Language'].astype('str')
    #dfu['Language'] = dfu['Language'].apply(capt).str.encode('utf-8')

    languages = pd.Series(sorted(dfu.Language.unique()))
    # dfu['Language']=dfu['Language'].str.encode('utf-8') #encode strings as unicode for accents etc.
    # reset the index and put it into ClipId
    id = languages.reset_index(drop=True)
    # dfi['ClipId']=dfi.index
    dfi = pd.DataFrame({'LANGUAGE_ID': id.index, 'LANGUAGE': languages})

    # find the maximum length of language
    lengths = df['Language'].str.len()
    maxlen = lengths.sort_values(ascending=False).iloc[0]
    print('Maximum length of title is ', maxlen)

    # rename columns
    # dfi.columns=['LANGUAGE_ID','LANGUAGE'] #use clip_id as genre_id here
    print(dfi)

    return dfi


def main():
    # get table
    df = language_table()
    # insert data into the DB
    #df.to_sql('LANGUAGE', engine, if_exists='append', index=False, chunksize=1)
    import_into_db(df, 'language')


if __name__ == "__main__":
    main()
