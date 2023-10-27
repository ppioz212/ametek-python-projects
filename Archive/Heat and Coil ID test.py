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
    return str(text).strip()
def coil_number(text):
    match = re.findall("(?i)COIL\s{0,3}#?:?\s{0,3}([0-9]{4,5}\S?)",str(text))   
    if len(match)!=0:
        if match[0] == "START":
            return np.nan
        return match[0]
    else:
        return np.nan
def heat_number(text):
    match = re.findall("(?i)HEAT\s{0,3}#?:?\s{0,3}(\S*)",str(text))
    if len(match)!=0:
        if match[0] == "START":
            return np.nan        
        return match[0]
    else:
        return np.nan

with open('VISUAL - Work Order Operations Data.csv','r',encoding="utf-8") as wo_ops_input, open('VISUAL - Parts Specification.csv','r',encoding="utf-8") as part_spec:
   df3 = pd.read_csv(wo_ops_input, usecols=['WORKORDER_TYPE','WORKORDER_BASE_ID','RESOURCE_ID','OP_DESCRIPTION'],low_memory=False)
   df3 = df3[df3['WORKORDER_TYPE']=='W']
   df3 = df3[df3['RESOURCE_ID']=='0 STOCK ROOM']

   df3['Coil No.'] = df3['OP_DESCRIPTION'].map(coil_number)
   df3['Heat No.'] = df3['OP_DESCRIPTION'].map(heat_number)
   df3.drop(['WORKORDER_TYPE','RESOURCE_ID','OP_DESCRIPTION'],axis=1,inplace=True)
   df3.drop_duplicates(subset=['WORKORDER_BASE_ID'],inplace=True)
   df3.to_csv('Heat and Coil ID.csv',index=False)
   
    # df = pd.read_csv(part_spec)
    # # df['PART_ID'] = df['PART_ID'].map(convert_to_text)
    # df['COMMODITY_CODE'] = df.apply(lambda row:commcode_edit(row), axis=1)
    # df['COMMODITY_CODE'] = df['COMMODITY_CODE'].map(alloy_edit)
    # df.to_excel('Part Number Data.xlsx',index=False)

    # df1 = pd.read_csv(wo_part_input)
    # # df1['WORKORDER_BASE_ID'] = df1['WORKORDER_BASE_ID'].map(convert_to_text)
    # df1.dropna(subset=['Start_Part_ID'], inplace=True)
    # df1.drop_duplicates(subset=['WORKORDER_BASE_ID'],inplace=True)
    # df1.to_excel('Work Order Part Data.xlsx',index=False)

    