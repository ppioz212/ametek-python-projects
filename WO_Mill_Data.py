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
mill_list = ['F FOIL MILL #1','F FOIL MILL #2','F FOIL MILL GRP','M 12 MILL #1','M 12 MILL #2','M 12 MILL GRP','M 14 MILL','M Z-HIGH MILL']
with open('S:/Automated Reports/VISUAL - Work Order Part Requirement.csv','r',encoding="utf-8") as wo_part_input:
    with open('S:/Automated Reports/VISUAL - Parts Specification.csv','r',encoding="utf-8") as part_spec:
        with open('S:/Automated Reports/VISUAL - Work Order Operations Data.csv','r',encoding="utf-8") as wo_ops_input:

            # df = pd.read_csv('Master Ops Data Raw.csv')
            df = pd.read_csv(wo_ops_input,low_memory=False)
            df = df.sort_values(['WORKORDER_BASE_ID','WORKORDER_LOT_ID','WORKORDER_SUB_ID','SEQUENCE_NO'],axis=0)

            df1 = pd.read_csv(part_spec, usecols=['PART_ID','Thickness','Width'])
            df1.set_index('PART_ID',inplace=True)
            df1.dropna(inplace=True)

            df2 = pd.read_csv(wo_part_input,usecols=['WORKORDER_TYPE','WORKORDER_BASE_ID','WORKORDER_LOT_ID','Start_Part_ID'],low_memory=False)
            df2 = df2.rename({'Start_Part_ID':'PART_ID'},axis='columns')
            df2.dropna(subset=['PART_ID'], inplace=True)
            df2.drop_duplicates(subset=['WORKORDER_BASE_ID','WORKORDER_LOT_ID'], inplace=True)

            df3 = pd.read_csv('S:/Automated Reports/VISUAL - Parts Specification.csv', usecols=['PART_ID','Customer','COMMODITY_CODE','DESCRIPTION'])
            df3['COMMODITY_CODE'] = df3.apply(lambda row:commcode_edit(row), axis=1)

            df = df.merge(df2,on=['WORKORDER_TYPE','WORKORDER_BASE_ID','WORKORDER_LOT_ID'])
            df = df.merge(df1,left_on='PART_ID',right_index=True)
            df = df.rename(columns={'PART_ID':'Start Part'})
            df['Thickness'] = df['Thickness'].map(thickness_edit)
            df['Alloy'] = df['WORKORDER_BASE_ID'].map(df3.set_index('PART_ID')['COMMODITY_CODE'])
            df['Customer'] = df['WORKORDER_BASE_ID'].map(df3.set_index('PART_ID')['Customer'])
            df['Alloy'] = df['Alloy'].map(alloy_edit)
            df = df.sort_values(['WORKORDER_BASE_ID','WORKORDER_LOT_ID','WORKORDER_SUB_ID','SEQUENCE_NO'], axis=0)
            df.to_csv('WO ops data edit.csv', encoding="utf-8", index=False)
with open('WO ops data final edit.csv','w',encoding="utf-8",) as wo_output, open('WO ops data edit.csv','r',encoding="utf-8",) as wo_input:
    r = csv.reader(wo_input)
    w = csv.writer(wo_output,lineterminator='\n')
    all = []
    row0= ['WORKORDER_BASE_ID','WORKORDER_LOT_ID','R1 Mill','R1 CR %','R1 Thick','R2 Mill','R2 CR %','R2 Thick','R3 Mill','R3 CR %','R3 Thick','R4 Mill','R4 CR %','R4 Thick','R5 Mill','R5 CR %','R5 Thick']
    all.append(row0)
    roll_toup = [('R1 Mill','R1 CR %','R1 Thick'),('R2 Mill','R2 CR %','R2 Thick'),('R3 Mill','R3 CR %','R3 Thick'),('R4 Mill','R4 CR %','R4 Thick'),('R5 Mill','R5 CR %','R5 Thick')]
    for i,row in enumerate(r):
        if i==0:
            continue
        if i==1:
            data = []
            curr_base_id = row[1]
            curr_lot_id = row[2]
            curr_thickness = row[17]
            data.extend([curr_base_id,curr_lot_id])
            continue
        if row[1]!=curr_base_id or row[2]!=curr_lot_id:
            all.append(data)
            data = []
            curr_base_id = row[1]
            curr_lot_id = row[2]
            curr_thickness = row[17]
            data.extend([curr_base_id,curr_lot_id])
            continue
        if row[6] not in mill_list:
            continue
        else:
            try:
                rf_thick = float(curr_thickness)
                rt_thick = (rf_thick)*100/float(row[7]) 
                row[17] = rt_thick
                curr_thickness = rt_thick
                percent_cr = round(((rf_thick-rt_thick)/rf_thick)*100,4)
                mill = row[6]
                data.extend([mill,percent_cr,rt_thick])
            except (ValueError,ZeroDivisionError) as error:
                row[17] = curr_thickness
    w.writerows(all)
os.remove('WO ops data edit.csv')
master_df = pd.read_excel('J:/Production Control/Database/Master Part data.xlsx')
mill_df = pd.read_csv('WO ops data final edit.csv',on_bad_lines='skip')
master_df = master_df.merge(mill_df,on=['WORKORDER_BASE_ID','WORKORDER_LOT_ID'])
master_df.to_csv("J:/Tech Services/Work order data mill data.csv",index=False)

