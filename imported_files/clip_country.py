#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 15:20:57 2018

@author: florian
"""

import pandas as pd

from sql_engine import *
from country import country_table

def main():
    # read the data
    path = '../../../data/db2018imdb/countries.csv'
    df = pd.read_csv(path)

    # get the definition of the country table
    dfl = country_table()

    # replace all country strings with the corresponding id (EXPENSIVE)
    df['CountryName'] = df['CountryName'].replace(dfl['COUNTRYNAME'].tolist(), dfl['COUNTRY_ID'].tolist())

    # rename columns
    df.columns = ['CLIP_ID', 'COUNTRY_ID']
    df.drop_duplicates(inplace=True)

    print('The final data shape is: \n', df.head())
    import_into_db(df, 'clip_country');

if __name__ == "__main__":
    main()
