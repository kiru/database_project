#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 15:20:57 2018

@author: florian
"""

import numpy as np
import pandas as pd

from sql_engine import *
from person import person_table

def splitListToRows(row, row_accumulator, target_columns):

    rd = zip(*(row[c].split('|') for c in target_columns))

    for s in rd:
        new_row = row.to_dict()

        for c, v in zip(target_columns, s):
            new_row[c] = v

        row_accumulator.append(new_row)

def maxlength(df, colstr):
    lengths = df[colstr].str.len()
    maxlen = lengths.sort_values(ascending=False).iloc[0]
    print('Maximum length of ', colstr, ' is ', maxlen)

def biography_table():
    print('read the data...')  # (explicitly name columns because it inserts NaN where column number is not consistent)
    path = '../../../data/db2018imdb/biographies.csv'
    df = pd.read_csv(path, names=['Name', 'RealName', 'Nickname', 'DateAndPlaceOfBirth',
                                  'Height', 'Biography', 'Biographer', 'DateAndCauseOfDeath', 'Spouse', 'Trivia',
                                  'BiographicalBooks',
                                  'PersonalQuotes', 'Salary', 'Trademark', 'WhereAreTheyNow'], skiprows=1,quoting=3)

    # add index
    dfb = pd.DataFrame(data={'BIOGRAPHY_ID': df.index, 'TITLE': df['BiographicalBooks'].fillna('NaN')})

    print('Split entries with multi-clip data...')
    new_rows = []
    dfb.apply(splitListToRows, axis=1, args=(new_rows, ['TITLE']))
    dfsplit = pd.DataFrame(new_rows)
    dfsplit['TITLE'] = dfsplit['TITLE'].map(lambda x: x.lstrip('[').rstrip(']'))

    dfu = dfsplit.drop_duplicates(subset=['TITLE'], keep='first')

    # get maximum lengths of strings
    maxlength(dfu, 'TITLE')
    dfi = dfu.reset_index(drop=True)
    dfi['BOOK_ID'] = dfi.index

    return dfi


def main():
    df = biography_table()
    import_into_db(df, 'biographicalbooks')


if __name__ == "__main__":
    main()
