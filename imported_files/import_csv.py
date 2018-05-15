#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 15:20:57 2018

@author: florian
"""

from joblib import Parallel, delayed

import pandas as pd
import sys

from sql_engine import get_engine, get_engine_for_oracle, chunkify


def main():
    # get table
    df = pd.read_csv(sys.argv[1])

    # create engine and connect
    engine = get_engine()
    engine.connect()

    # insert data into the DB
    print('The final data shape is: ', df.shape)

    print('insert into database')
    df.to_sql(sys.argv[2], engine, if_exists='append', index=False, chunksize=1)


if __name__ == "__main__":
    main()
