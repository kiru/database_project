#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 15:20:57 2018

@author: florian
"""

import pandas as pd
import re

from sql_engine import *


def capt(x, reg=r"(?<=\')(.*?)(?=\')", ret=None):
    # Capture word between parantheses
    m = re.search(reg, x)
    if m:
        return m.group(1)
    elif ret:
        return ret
    else:
        return x


def replace_name_id(series, replace_list, value_list):
    # function assumes that series and replaces_list are sorted
    if (len(replace_list) != len(value_list)):
        print('Replace list and value list must be of the same length')
        return -1
    (rows,) = series.shape
    listlen = len(replace_list)
    offset = 0
    for i in range(rows):
        for j in range(listlen - offset):
            jj = j + offset
            if (str(series[i]) == str(replace_list[jj])):
                series[i] = value_list[jj]
                offset = j
                break
    return series


def person_table():
    # read the data
    path = '../../../data/db2018imdb/actors.csv'
    df1 = pd.read_csv(path)
    path = '../../../data/db2018imdb/directors.csv'
    df2 = pd.read_csv(path)
    path = '../../../data/db2018imdb/producers.csv'
    df3 = pd.read_csv(path)
    path = '../../../data/db2018imdb/writers.csv'
    df4 = pd.read_csv(path)
    path = '../../../data/db2018imdb/biographies.csv'
    df5 = pd.read_csv(path, names=['FullName', 'RealName', 'Nickname', 'DateAndPlaceOfBirth',
                                   'Height', 'Biography', 'Biographer', 'DateAndCauseOfDeath', 'Spouse', 'Trivia',
                                   'BiographicalBooks',
                                   'PersonalQuotes', 'Salary', 'Trademark', 'WhereAreTheyNow'], skiprows=1)

    print('Split spouse data...')
    # TODO: consider only the name in ' '
    df5['Spouse'] = df5['Spouse'].fillna('[]')
    dfspouse = pd.concat([pd.Series(row['FullName'],
                                    row['Spouse'].split('|')) for _, row in df5.iterrows()]).reset_index()

    # print("AHAHSDF",dfspouse.head())
    dfspouse['index'] = dfspouse['index'].map(lambda x: x.lstrip('[').rstrip(']'))
    # print("SPOUSE\n",dfspouse['index'])

    # Get just the name
    dfspouse['index'] = dfspouse['index'].str.replace(r"\'\?\'", r"\'unknown'")
    dfspouse['index'] = dfspouse['index'].apply(lambda x: capt(x))

    print('Combine all persons...')
    dfall = df1['FullName'].append(df2['FullName'].append(
        df3['FullName'].append(df4['FullName'].append(df5['FullName']).append(dfspouse['index']))))
    print('Size of all person data combined: ', dfall.shape)
    # print("dd\n", dfall)
    # select only unique entries
    dfu = dfall.drop_duplicates(keep='first')
    print('Size of unique person data: ', dfu.shape)

    # sort relation, encode as utf-8, find longest string
    #dfu = dfu.str.encode('utf-8')
    dfs = dfu.sort_values(ascending=True)
    lengths = dfs.str.len()
    maxlen = lengths.sort_values(ascending=False).iloc[0]
    print('Maximum length of fullname is ', maxlen)

    # reset the index and put it into ClipId
    dfi = dfs.reset_index(drop=True)
    df = pd.DataFrame(data={'PERSON_ID': dfi.index, 'FULLNAME': dfi})

    return df


def main():
    df = person_table()
    df.to_csv('PERSON.csv', index=False, encoding='utf-8')
    #import_into_db(df, 'person');


if __name__ == "__main__":
    main()
