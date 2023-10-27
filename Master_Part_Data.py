import csv
import pandas as pd
import datetime as dt
import re
import numpy as np
import os

def thickness_edit(text):
    text = text.replace('"','')
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
def convert_to_text(text):
    text = str(text)
    return text

mill_list = ['F FOIL MILL #1','F FOIL MILL #2','F FOIL MILL GRP','M 12 MILL #1','M 12 MILL #2','M 12 MILL GRP','M 14 MILL','M Z-HIGH MILL']
with open('S:/Automated Reports/VISUAL - Work Order Part Requirement.csv','r',encoding="utf-8") as wo_part_input:
    
    df1 = pd.read_csv('S:/Automated Reports/VISUAL - Parts Specification.csv',usecols = lambda x:x not in ['Part_Specifications','Customer_Spec','CSM_'])
    # df1['PART_ID'] = df1['PART_ID'].map(convert_to_text)
    df1 = df1.replace('®','')
    df1 = df1.replace(np.nan,'')
    df1.set_index('PART_ID',inplace=True)
    df1['COMMODITY_CODE'] = df1['COMMODITY_CODE'].map(alloy_edit)
    df1['COMMODITY_CODE'] = df1.apply(lambda row:commcode_edit(row), axis=1)
    df1.dropna(inplace=True)

    df = pd.read_csv(wo_part_input,usecols=['WORKORDER_TYPE','WORKORDER_BASE_ID','WORKORDER_LOT_ID','Start_Part_ID','End_Part_ID'],low_memory=False)
    df = df[df['WORKORDER_TYPE']=='M']
    df.drop('WORKORDER_TYPE', axis=1, inplace=True)
    df.rename(columns={'End_Part_ID':'Final Part','Start_Part_ID':'Start Part'},inplace=True)
    df.dropna(subset=['Start Part'], inplace=True)
    # df['Start Part'] = df['Start Part'].map(convert_to_text)
    # df['Final Part'] = df['Final Part'].map(convert_to_text)

    df.drop_duplicates(subset=['WORKORDER_BASE_ID','WORKORDER_LOT_ID'], inplace=True)
    
    df['Start Thickness'] = df['Start Part'].map(df1['Thickness'])
    df['Start Width'] = df['Start Part'].map(df1['Width'])
    df['Start Temper'] = df['Start Part'].map(df1['Temper'])
    df['Start Surface Finish'] = df['Start Part'].map(df1['Surface_Finish'])
    df['Start Stock UM'] = df['Start Part'].map(df1['STOCK_UM'])
    df['Start Qty on hand'] = df['Start Part'].map(df1['QTY_ON_HAND'])
    df['Start Qty on order'] = df['Start Part'].map(df1['QTY_ON_ORDER'])
    
    df['Final Thickness'] = df['Final Part'].map(df1['Thickness'])
    df['Final Width'] = df['Final Part'].map(df1['Width'])
    df['Final Temper'] = df['Final Part'].map(df1['Temper'])
    df['Final Surface Finish'] = df['Final Part'].map(df1['Surface_Finish'])
    df['Final Stock UM'] = df['Final Part'].map(df1['STOCK_UM'])
    df['Final Qty on hand'] = df['Final Part'].map(df1['QTY_ON_HAND'])
    df['Final Qty on order'] = df['Final Part'].map(df1['QTY_ON_ORDER'])
    
    df['Product Code'] = df['Final Part'].map(df1['PRODUCT_CODE'])
    df['Customer'] = df['Final Part'].map(df1['Customer'])
    df['Alloy'] = df['Final Part'].map(df1['COMMODITY_CODE'])

    df.to_excel('J:/Production Control/Database/Master Part data.xlsx',encoding='utf-8',  index=False)