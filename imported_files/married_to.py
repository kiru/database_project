import numpy as np
import pandas as pd
from biography import biography_table
from person import person_table
from person import capt


from sql_engine import get_engine
from person import person_table

dfperson = person_table()
dfbio = biography_table(spouse = True)
df = dfbio[~pd.isnull(dfbio['Spouse'])]

df = df[['BIOGRAPHY_ID', 'FULLNAME', 'Spouse']]
dfmarried=pd.concat([pd.Series(row['BIOGRAPHY_ID'],
                               row['Spouse'].split('|')) for _, row in df.iterrows()]).reset_index()

dfmarried['index'] = dfmarried['index'].map(lambda x: x.lstrip('[').rstrip(']'))
    # print("SPOUSE\n",dfspouse['index'])

    # Get just the name
dfmarried1 = dfmarried.copy()
dfmarried1['index'] = dfmarried1['index'].str.replace(r"\'\?\'", r"\'unknown'")
dfmarried1['index'] = dfmarried1['index'].apply(lambda x: capt(x)).str.encode('utf-8')
dfmarried1.columns = ['FULLNAME', 'BIOGRAPHY_ID']

dfmarried1['DATE'] = dfmarried['index'].apply(lambda x: capt(x, reg = r"(?<=\s\()(.*?)(?=\))", ret = "unknown"))
dfmarried1['MARITAL_STATUS'] = dfmarried['index'].apply(lambda x: capt(x, reg = r"(?<=\)\s\()(.*?)(?=\))", ret = "married/unknown"))
dfmarried1['CHILDREN'] = dfmarried['index'].apply(lambda x: capt(x, reg = r"(?<=\;\s)(.*?)(?=$)", ret = "0/unknown"))


dfmarried2 = dfmarried1.merge(dfperson, left_on = 'FULLNAME', right_on = 'FULLNAME', how = 'left')
dfmarried2 = dfmarried2[['BIOGRAPHY_ID', 'PERSON_ID', 'DATE', 'MARITAL_STATUS', 'CHILDREN']]
print(dfmarried2.head())


#create engine and connect
engine=get_engine()
engine.connect()
#insert data into the DB
#    df.iloc[0:1].to_sql('PERSON', engine, if_exists='append',index=False)
