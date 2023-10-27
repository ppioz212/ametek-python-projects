import csv
import pandas as pd
import datetime as dt
import re
import numpy as np
import os

def thickness_edit(text):
    text = str(text).replace('"','')
    return text
def commcode_edit(row):
    if row['COMMODITY_CODE'] == 'CSM':
        count = 0
        text = row['DESCRIPTION']
        for i, word in enumerate(text.split()):
            if '.' in word:
                count = i
                break
        return ' '.join(text.split()[:count])
    else:
        return row['COMMODITY_CODE']
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

mill_list = ['F FOIL MILL #1','F FOIL MILL #2','F FOIL MILL GRP','M 12 MILL #1','M 12 MILL #2','M 12 MILL GRP','M 14 MILL','M Z-HIGH MILL']
with open('S:/Automated Reports/VISUAL - Work Order Operations Data.csv','r',encoding="utf-8") as wo_input, open('S:/Automated Reports/VISUAL - Work Order Part Requirement.csv','r',encoding="utf-8") as wo_part_input:
    df = pd.read_csv(wo_input,low_memory=False)
    df = df[df['WORKORDER_TYPE']=='M']
    df.drop('WORKORDER_TYPE', axis=1, inplace=True)
    
    df1 = pd.read_csv('S:/Automated Reports/VISUAL - Parts Specification.csv',usecols = lambda x:x not in ['Part_Specifications','Customer_Spec','CSM_'])
    df1 = df1.replace('®','')
    df1 = df1.replace(np.nan,'')
    df1.set_index('PART_ID',inplace=True)
    df1['COMMODITY_CODE'] = df1['COMMODITY_CODE'].map(alloy_edit)
    df1['COMMODITY_CODE'] = df1.apply(lambda row:commcode_edit(row), axis=1)
    df1.dropna(inplace=True)

    df2 = pd.read_csv(wo_part_input,usecols=['WORKORDER_TYPE','WORKORDER_BASE_ID','WORKORDER_LOT_ID','Start_Part_ID','End_Part_ID'],low_memory=False)
    df2 = df2[df2['WORKORDER_TYPE']=='M']
    df2.drop('WORKORDER_TYPE', axis=1, inplace=True)
    df2.dropna(subset=['Start_Part_ID'], inplace=True)
    df2.drop_duplicates(subset=['WORKORDER_BASE_ID','WORKORDER_LOT_ID'], inplace=True)

    df = df.merge(df2,on=['WORKORDER_BASE_ID','WORKORDER_LOT_ID'])
    df['Start Thickness'] = df['Start_Part_ID'].map(df1['Thickness'])
    df['Start Width'] = df['Start_Part_ID'].map(df1['Width'])
    df['Final Thickness'] = df['End_Part_ID'].map(df1['Thickness'])
    df['Final Width'] = df['End_Part_ID'].map(df1['Width'])    
    df['Start Thickness'] = df['Start Thickness'].map(thickness_edit)
    df['Final Thickness'] = df['Final Thickness'].map(thickness_edit)
    df['Alloy'] = df['End_Part_ID'].map(df1['COMMODITY_CODE'])
    df['Customer'] = df['End_Part_ID'].map(df1['Customer'])
    df['Alloy'] = df['Alloy'].map(alloy_edit)
    df.to_csv('J:/Tech services/Masters Ops Data.csv', encoding="utf-8", index=False)