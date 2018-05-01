#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 15:20:57 2018

@author: florian
"""

import numpy as np
import pandas as pd

from sql_engine import get_engine
from person import person_table


def maxlength(df,colstr):
    lengths=df[colstr].str.len()
    maxlen=lengths.sort_values(ascending=False).iloc[0]
    print('Maximum length of ',colstr,' is ',maxlen)


print('read the data...') #(explicitly name columns because it inserts NaN where column number is not consistent)
path='../../../data/db2018imdb/biographies.csv'
df = pd.read_csv(path, names=['Name','RealName','Nickname','DateAndPlaceOfBirth',
'Height','Biography','Biographer','DateAndCauseOfDeath','Spouse','Trivia','BiographicalBooks',
'PersonalQuotes','Salary','Trademark','WhereAreTheyNow'],skiprows=1)

#get the definition of the person table
print('Get the person name-id relation...')
dfp=person_table()

#replace all language strings with the corresponding id (EXPENSIVE)
print('Replace person name with id...')
df['Name']=df['Name'].str.encode('utf-8') #encode strings as unicode for accents etc.
df['Name']=df['Name'].replace(dfp['FULLNAME'].tolist(),dfp['PERSON_ID'].tolist())

print('extract birth date and write to new column...')
df['BIRTH_DATE']=df['DateAndPlaceOfBirth']
(rows,columns)=df.shape
for row in range(rows):
    df['BIRTH_DATE'][row]=pd.to_datetime(df['BIRTH_DATE'][row], format='%d %B %Y', errors='ignore', exact=False)
    df['BIRTH_DATE'][row]=pd.to_datetime(df['BIRTH_DATE'][row], format='%B %Y', errors='ignore', exact=False)
    df['BIRTH_DATE'][row]=pd.to_datetime(df['BIRTH_DATE'][row], format='%Y', errors='coerce', exact=False)
#remove date from place of birth
df['DateAndPlaceOfBirth']=df['DateAndPlaceOfBirth'].str.replace('(.*\d\d\d\d)','').str.encode('utf-8')

print('extract death date and write to new column...')
df['DEATH_DATE']=df['DateAndCauseOfDeath']
(rows,columns)=df.shape
for row in range(rows):
    df['DEATH_DATE'][row]=pd.to_datetime(df['DEATH_DATE'][row], format='%d %B %Y', errors='ignore', exact=False)
    df['DEATH_DATE'][row]=pd.to_datetime(df['DEATH_DATE'][row], format='%B %Y', errors='ignore', exact=False)
    df['DEATH_DATE'][row]=pd.to_datetime(df['DEATH_DATE'][row], format='%Y', errors='coerce', exact=False)
#remove date from place of birth
df['DateAndCauseOfDeath']=df['DateAndCauseOfDeath'].str.replace('(.*\d\d\d\d)','').str.encode('utf-8')

print('encode utf-8...')
df['Biography']=df['Biography'].str.replace('(.*\d\d\d\d)','').str.encode('utf-8')
df['Trivia']=df['Trivia'].str.replace('(.*\d\d\d\d)','').str.encode('utf-8')
df['PersonalQuotes']=df['PersonalQuotes'].str.replace('(.*\d\d\d\d)','').str.encode('utf-8')
df['Salary']=df['Salary'].str.replace('(.*\d\d\d\d)','').str.encode('utf-8')
df['Trademark']=df['Trademark'].str.replace('(.*\d\d\d\d)','').str.encode('utf-8')
df['WhereAreTheyNow']=df['WhereAreTheyNow'].str.replace('(.*\d\d\d\d)','').str.encode('utf-8')

print('Rename columns...')
df.columns=['PERSON_ID','REALNAME','NICKNAME','BIRTH_PLACE',
'HEIGHT','BIOGRAPHY','BIOGRAPHER','DEATH_CAUSE','Spouse',
'TRIVIA','BiographicalBooks','PERSONALQUOTES','SALARY','TRADEMARK','WHERENOW',
'BIRTH_DATE','DEATH_DATE']

#get maximum lengths of strings
maxlength(df,'REALNAME')
maxlength(df,'NICKNAME')
maxlength(df,'BIRTH_PLACE')
maxlength(df,'BIOGRAPHY')
maxlength(df,'BIOGRAPHER')
maxlength(df,'DEATH_CAUSE')
maxlength(df,'TRIVIA')
maxlength(df,'PERSONALQUOTES')
maxlength(df,'SALARY')
maxlength(df,'TRADEMARK')
maxlength(df,'WHERENOW')

print('convert height from feet,inch into cm')
feet=pd.to_numeric(df['HEIGHT'].str.extract('(.*(?=\'))'),errors='coerce',downcast='float')
itmp=df['HEIGHT'].str.extract('\'\s(..)') 
inch=pd.to_numeric(itmp.str.replace('"',''),errors='coerce',downcast='float')
halfinch=pd.to_numeric(df['HEIGHT'].str.extract('(.(?=/))'),errors='coerce',downcast='float')
cm=pd.to_numeric(df['HEIGHT'].str.extract('(.*(?=cm))'),errors='coerce',downcast='float')
height=cm.fillna(0)+feet.fillna(0)*30.48+(inch.fillna(0)+0.5*halfinch.fillna(0))*2.54
df['HEIGHT']=height.replace(0,np.nan)

#add index
df['BIOGRAPHY_ID']=df.index

dfselect=df[['PERSON_ID','REALNAME','NICKNAME','BIRTH_PLACE',
'HEIGHT','BIOGRAPHY','BIOGRAPHER','DEATH_CAUSE',
'TRIVIA','PERSONALQUOTES','SALARY','TRADEMARK','WHERENOW',
'BIRTH_DATE','DEATH_DATE','BIOGRAPHY_ID']]

#create engine and connect
engine=get_engine()
engine.connect()
#insert data into the DB
dfselect.iloc[0:1].to_sql('BIOGRAPHY', engine, if_exists='append',index=False)