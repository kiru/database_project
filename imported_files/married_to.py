import numpy as np
import pandas as pd
from biography import biography_table
from person import capt

from sql_engine import get_engine
from person import person_table

from sql_engine import *

dfp = pd.read_csv('PERSON.csv')
dfbio = biography_table(spouse=True)
df = dfbio[~pd.isnull(dfbio['Spouse'])]

df = df[['BIOGRAPHY_ID', 'NAME', 'Spouse']]
dfmarried = pd.concat([pd.Series(row['BIOGRAPHY_ID'],
                                 row['Spouse'].split('|')) for _, row in df.iterrows()]).reset_index()

dfmarried['index'] = dfmarried['index'].map(lambda x: x.lstrip('[').rstrip(']'))
# print("SPOUSE\n",dfspouse['index'])

# Get just the name
dfmarried1 = dfmarried.copy()
dfmarried1['index'] = dfmarried1['index'].str.replace(r"\'\?\'", r"\'unknown'")
dfmarried1['index'] = dfmarried1['index'].apply(lambda x: capt(x))
dfmarried1.columns = ['NAME', 'BIOGRAPHY_ID']

dfmarried1['DATE'] = dfmarried['index'].apply(lambda x: capt(x, reg=r"(?<=\s\()(.*?)(?=\))", ret="unknown"))
dfmarried1['MARITAL_STATUS'] = dfmarried['index'].apply(
    lambda x: capt(x, reg=r"(?<=\)\s\()(.*?)(?=\))", ret="married/unknown"))
dfmarried1['CHILDREN'] = dfmarried['index'].apply(lambda x: capt(x, reg=r"(?<=\;\s)(.*?)(?=$)", ret="0/unknown"))

nameSeries = pd.Series(dfp['PERSON_ID'].values, index=dfp['FULLNAME'])
dfmarried1['PERSON_ID'] = dfmarried1['NAME'].map(nameSeries)
dfmarried1['PERSON_ID'] = dfmarried1['PERSON_ID'].fillna(0).astype('int64')
dfmarried1 = dfmarried1[['BIOGRAPHY_ID', 'PERSON_ID', 'DATE', 'MARITAL_STATUS', 'CHILDREN']]
dfmarried1['MARRIED_ID'] = dfmarried1.index
print(dfmarried1.head())


# insert data into the DB
import_into_db(dfmarried1, 'married_to')
