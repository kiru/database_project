#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 15:20:57 2018

@author: florian
"""

import pandas as pd


from sql_engine import *


def genre_table():
    # read the data
    genre_path = '../../../data/db2018imdb/genres.csv'
    df = pd.read_csv(genre_path)

    # query about the relation
    (rows, cols) = df.shape
    print(df.columns)
    print(df.dtypes)
    print(df.shape)

    # select only unique entries
    dfu = df.drop_duplicates(subset=['Genre'], keep='first')
    print(dfu.shape)

    # reset the index and put it into ClipId
    dfi = dfu.reset_index(drop=True)
    dfi['ClipId'] = dfi.index

    # rename columns
    dfi.columns = ['GENRE_ID', 'GENRE']  # use clip_id as genre_id here
    print(dfi)

    return dfi


def main():
    # get table
    df = genre_table()

    #df.to_sql("GENRE", engine, if_exists='append', index=False)
    import_into_db(df, 'genre')

if __name__ == "__main__":
    main()
