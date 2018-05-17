#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 15:20:57 2018

@author: florian
"""

from joblib import Parallel, delayed

import pandas as pd
import sys

from sql_engine import *



def main():
    # get table
    csv = '../csv/%s.csv' % sys.argv[1]
    df = pd.read_csv(csv, encoding='utf-8')
    import_csv(csv, df, sys.argv[1])


if __name__ == "__main__":
    main()
