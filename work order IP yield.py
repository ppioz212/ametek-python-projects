import csv
import pandas as pd
import datetime as dt
import re
import numpy as np
import os

def thickness_edit(text):
    text = str(text).replace('"','')
    return text
def WObaseID_edit(text):
    return str(text)
def commcode_edit(row):
    if row['Commodity Code'] == 'CSM':
        count = 0
        text = row['Description']
        for i, word in enumerate(text.split()):
            if '.' in word:
                count = i
                break
        return ' '.join(text.split()[:count])
    else:
        return row['Commodity Code']
def alloy_edit(text):
    try:
        text = str(text).upper().strip()
        alloy_list = {'TI-GR1':'TI-GR 1','.':'','®':''}
        for mist in alloy_list:
            text = text.replace(mist,alloy_list[mist])
    except:
        pass
    return text
def alloy_finaledit(row):
    if row['Alloy Temp'] == 'NAN':
        return row['Alloy']
    else:
        return row['Alloy Temp']
def wo_edit(text):
    text = str(text).upper().strip()
    return text
def SP_edit(text):
    text = str(text).strip()
    return text
    
df = pd.read_excel('BB IP Yield Baseline 2022.xlsx')

df1 = pd.read_csv('Work Order Data.csv',usecols=['Type','Base ID','Part ID'])
df1 = df1[df1['Type']=='W']
df1['Base ID']=df1['Base ID'].map(wo_edit)

df2 = pd.read_csv('Part number data.csv',usecols=['Part ID','Customer','Commodity Code','Description','Thickness','Width'])
df2['Commodity Code'] = df2.apply(lambda row:commcode_edit(row), axis=1)
merge_df = pd.merge(df1,df2,left_on=['Part ID'],right_on=['Part ID'],how='left')
merge_df = merge_df.set_index('Base ID')
merge_df = merge_df.loc[~merge_df.index.duplicated(keep='first')]

df['WORKORDER_BASE_ID'] = df['WORKORDER_BASE_ID'].map(WObaseID_edit)
df['PART_ID'] = df['WORKORDER_BASE_ID'].map(merge_df['Part ID'])
df = df[(df['PART_ID'] =='794470')| (df['PART_ID'] == int(794470))]
df['Start Part'] = df['Start Part'].map(SP_edit)
df['Thickness'] = df['Start Part'].map(df2.set_index('Part ID')['Thickness'])
df['Thickness'] = df['Thickness'].map(thickness_edit)
df['Width'] = df['Start Part'].map(df2.set_index('Part ID')['Width'])
df.to_excel('BB IP Yield Baseline 2022 edit.xlsx', encoding="utf-8", index=False)