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

def do_date(date):
    # format documentation: https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
    if (pd.isnull(date)):
        return date

    converted = pd.to_datetime(date, format='%d %B %Y', errors='coerce', exact=False)

    if (pd.isnull(converted)):
        converted = pd.to_datetime(date, format='%B %Y', errors='coerce', exact=False)

    if(pd.isnull(converted)):
        converted = pd.to_datetime(date, format='%Y', errors='coerce', exact=False)

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

def maxlength(df, colstr):
    lengths = df[colstr].str.len()
    maxlen = lengths.sort_values(ascending=False).iloc[0]
    print('Maximum length of ', colstr, ' is ', maxlen)


def biography_table(spouse=False):
    print('read the data...')  # (explicitly name columns because it inserts NaN where column number is not consistent)
    path = '../../../data/db2018imdb/biographies.csv'
    df = pd.read_csv(path, names=['Name', 'RealName', 'Nickname', 'DateAndPlaceOfBirth',
                                  'Height', 'Biography', 'Biographer', 'DateAndCauseOfDeath', 'Spouse', 'Trivia',
                                  'BiographicalBooks',
                                  'PersonalQuotes', 'Salary', 'Trademark', 'WhereAreTheyNow'], skiprows=1)


    if not spouse:
        # get the definition of the person table
        # print('Get the person name-id relation...')
        # dfp=person_table()
        print('Get the person name-id relation...')
        dfp = pd.read_csv('PERSON.csv')

        # replace all language strings with the corresponding id (EXPENSIVE)
        print('Replace person name with id...')
        #df['Name'] = df['Name'].str.encode('utf-8')  # encode strings as unicode for accents etc.
        # df['Name']=df['Name'].replace(dfp['FULLNAME'].tolist(),dfp['PERSON_ID'].tolist())
        nameSeries = pd.Series(dfp['PERSON_ID'].values, index=dfp['FULLNAME'])
        df['PERSON_ID'] = df['Name'].map(nameSeries)

        print('extract birth date and write to new column...')
        df['BIRTH_DATE'] = df['DateAndPlaceOfBirth']
        # enforce date type
        df['BIRTH_DATE'] = lookup(df['BIRTH_DATE'])
        # (rows, columns) = df.shape
        # for row in range(rows):
        #     df['BIRTH_DATE'][row] = pd.to_datetime(df['BIRTH_DATE'][row], format='%d %B %Y', errors='ignore', exact=False)
        #     df['BIRTH_DATE'][row] = pd.to_datetime(df['BIRTH_DATE'][row], format='%B %Y', errors='ignore', exact=False)
        #     df['BIRTH_DATE'][row] = pd.to_datetime(df['BIRTH_DATE'][row], format='%Y', errors='coerce', exact=False)
        # remove date from place of birth
        df['DateAndPlaceOfBirth'] = df['DateAndPlaceOfBirth'].str.replace('(.*\d\d\d\d)', '')

        print('extract death date and write to new column...')
        df['DEATH_DATE'] = df['DateAndCauseOfDeath']
        # enforce date type
        df['DEATH_DATE'] = lookup(df['DEATH_DATE'])
        # (rows, columns) = df.shape
        # for row in range(rows):
        #     df['DEATH_DATE'][row] = pd.to_datetime(df['DEATH_DATE'][row], format='%d %B %Y', errors='ignore',
        #                                            exact=False)
        #     df['DEATH_DATE'][row] = pd.to_datetime(df['DEATH_DATE'][row], format='%B %Y', errors='ignore', exact=False)
        #     df['DEATH_DATE'][row] = pd.to_datetime(df['DEATH_DATE'][row], format='%Y', errors='coerce', exact=False)
        # remove date from place of birth
        df['DateAndCauseOfDeath'] = df['DateAndCauseOfDeath'].str.replace('(.*\d\d\d\d)', '')

        # print('encode utf-8...')
        # df['Biography'] = df['Biography'].str.replace('(.*\d\d\d\d)', '').str.encode('utf-8')
        # df['Trivia'] = df['Trivia'].str.replace('(.*\d\d\d\d)', '').str.encode('utf-8')
        # df['PersonalQuotes'] = df['PersonalQuotes'].str.replace('(.*\d\d\d\d)', '').str.encode('utf-8')
        # df['Salary'] = df['Salary'].str.replace('(.*\d\d\d\d)', '').str.encode('utf-8')
        # df['Trademark'] = df['Trademark'].str.replace('(.*\d\d\d\d)', '').str.encode('utf-8')
        # df['WhereAreTheyNow'] = df['WhereAreTheyNow'].str.replace('(.*\d\d\d\d)', '').str.encode('utf-8')

        print('Rename columns...')
        df.columns = ['FULLNAME', 'REALNAME', 'NICKNAME', 'BIRTH_PLACE',
                      'HEIGHT', 'BIOGRAPHY', 'BIOGRAPHER', 'DEATH_CAUSE', 'Spouse',
                      'TRIVIA', 'BiographicalBooks', 'PERSONALQUOTES', 'SALARY', 'TRADEMARK', 'WHERENOW',
                      'PERSON_ID','BIRTH_DATE', 'DEATH_DATE']

        # get maximum lengths of strings
        maxlength(df, 'REALNAME')
        maxlength(df, 'NICKNAME')
        maxlength(df, 'BIRTH_PLACE')
        maxlength(df, 'BIOGRAPHY')
        maxlength(df, 'BIOGRAPHER')
        maxlength(df, 'DEATH_CAUSE')
        maxlength(df, 'TRIVIA')
        maxlength(df, 'PERSONALQUOTES')
        maxlength(df, 'SALARY')
        maxlength(df, 'TRADEMARK')
        maxlength(df, 'WHERENOW')

        print('convert height from feet,inch into cm')
        feet = pd.to_numeric(df['HEIGHT'].str.extract('(.*(?=\'))'), errors='coerce', downcast='float')
        itmp = df['HEIGHT'].str.extract('\'\s(..)')
        inch = pd.to_numeric(itmp.str.replace('"', ''), errors='coerce', downcast='float')
        halfinch = pd.to_numeric(df['HEIGHT'].str.extract('(.(?=/))'), errors='coerce', downcast='float')
        cm = pd.to_numeric(df['HEIGHT'].str.extract('(.*(?=cm))'), errors='coerce', downcast='float')
        height = cm.fillna(0) + feet.fillna(0) * 30.48 + (inch.fillna(0) + 0.5 * halfinch.fillna(0)) * 2.54
        df['HEIGHT'] = height.replace(0, np.nan)

        df['NICKNAME']=df['NICKNAME'].str.split('|')

    else:
        print('Rename columns...')
        df.columns = ['FULLNAME', 'REALNAME', 'NICKNAME', 'BIRTH_PLACE',
                      'HEIGHT', 'BIOGRAPHY', 'BIOGRAPHER', 'DEATH_CAUSE', 'Spouse',
                      'TRIVIA', 'BiographicalBooks', 'PERSONALQUOTES', 'SALARY', 'TRADEMARK', 'WHERENOW']
    # add index
    df['BIOGRAPHY_ID'] = df.index

    if spouse:
        return df

    else:
        dfselect = df[['PERSON_ID', 'REALNAME', 'NICKNAME', 'BIRTH_PLACE',
                       'HEIGHT', 'BIOGRAPHY', 'BIOGRAPHER', 'DEATH_CAUSE',
                       'TRIVIA', 'PERSONALQUOTES', 'SALARY', 'TRADEMARK', 'WHERENOW',
                       'BIRTH_DATE', 'DEATH_DATE', 'BIOGRAPHY_ID']]
        return dfselect


def main():
    df = biography_table()
    import_into_db(df, 'biography')


if __name__ == "__main__":
    main()
