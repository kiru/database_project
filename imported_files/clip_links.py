#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 15:20:57 2018

@author: florian
"""

import pandas as pd

from sql_engine import *

# read the data
path = '../../../data/db2018imdb/clip_links.csv'
df = pd.read_csv(path)
df.drop_duplicates(inplace=True)

# rename columns
df['CLIPLINK_ID'] = list(range(0, df.shape[0]))

df.columns = ['CLIP_FROM_ID', 'CLIP_TO_ID', 'LINK_TYPE', 'CLIPLINK_ID']  # use clip_id as genre_id here

# create engine and connect
import_into_db(df, 'cliplinks');
