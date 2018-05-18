#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 15:20:57 2018

@author: florian
"""

import pandas as pd

from sql_engine import *
from country import country_table


def do_date(date):
    # format documentation: https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
    if (pd.isnull(date)):
        return date

    converted = pd.to_datetime(date, format='%d %B %Y', errors='coerce')

    if (pd.isnull(converted)):
        converted = pd.to_datetime(date, format='%B %Y', errors='coerce')

    if(pd.isnull(converted)):
        converted = pd.to_datetime(date, format='%Y', errors='coerce')

    print("Convert Date: ", date, " ", converted)
    return converted

def lookup(s):
    """
    This is an extremely fast approach to datetime parsing.
    For large data, the same dates are often repeated. Rather than
    re-parse these, we store all unique dates, parse them, and
    use a lookup to convert all dates.
    """
    print("Bulid dates")
    dates = {date: do_date(date) for date in s.unique()}
    print("Replace dates")
    return s.map(dates)

def main():
    # read the data
    path = '../../../data/db2018imdb/release_dates.csv'
    df = pd.read_csv(path)

    # get the definition of the country table
    dfl = country_table()

    # replace all country strings with the corresponding id (EXPENSIVE)
    nameSeries = pd.Series(dfl['COUNTRY_ID'].values, index=dfl['COUNTRYNAME'])

    df['ReleaseCountry'] = df['ReleaseCountry'].map(nameSeries)

    df.dropna(subset=['ReleaseCountry'], inplace=True)
    df['ReleaseCountry'] = df['ReleaseCountry'].astype('int64')

    # rename columns
    print ("Before: ", df.head)
    df.columns = ['CLIP_ID', 'COUNTRY_ID', 'RELEASE_DATE']
    print ("After: ", df.head)

    # enforce date type
    df['RELEASE_DATE'] = lookup(df['RELEASE_DATE'])

    #TOOD KIRU: not sure if this is a great idea
    df.drop_duplicates(inplace=True, subset=['CLIP_ID', 'COUNTRY_ID'])

    import_into_db(df, 'released')


if __name__ == "__main__":
    main()
