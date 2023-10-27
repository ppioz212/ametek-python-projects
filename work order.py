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
            df = pd.read_csv(wo_ops_input,low_memory=False)
            df = df[df['WORKORDER_TYPE']=='M']
            df = df.sort_values(['WORKORDER_BASE_ID','WORKORDER_LOT_ID','WORKORDER_SUB_ID','SEQUENCE_NO'],axis=0)

            df1 = pd.read_csv(part_spec, usecols=['PART_ID','Thickness','Width'])
            df1.set_index('PART_ID',inplace=True)
            df1.dropna(inplace=True)

            df2 = pd.read_csv(wo_part_input,usecols=['WORKORDER_TYPE','WORKORDER_BASE_ID','WORKORDER_LOT_ID','Start_Part_ID'],low_memory=False)
            df2 = df2.rename({'Start_Part_ID':'PART_ID'},axis='columns')
            df2 = df2[df2['WORKORDER_TYPE']=='M']
            df2.dropna(subset=['PART_ID'], inplace=True)
            df2.drop_duplicates(subset=['WORKORDER_BASE_ID','WORKORDER_LOT_ID'], inplace=True)
            
            df3 = pd.read_csv('S:/Automated Reports/VISUAL - Parts Specification.csv', usecols=['PART_ID','Customer','COMMODITY_CODE','DESCRIPTION'])
            df3['COMMODITY_CODE'] = df3.apply(lambda row:commcode_edit(row), axis=1)

            # df4 = pd.read_csv('Work Order data.csv')
            # df4 = pd.read_excel('WO Info by Resource 123122.xlsx', usecols=['WORKORDER_BASE_ID','WORKORDER_LOT_ID'])


            df = df.merge(df2,on=['WORKORDER_TYPE','WORKORDER_BASE_ID','WORKORDER_LOT_ID'])
            df = df.merge(df1,left_on='PART_ID',right_index=True)
            df = df.rename(columns={'PART_ID':'Start Part'})
            # df = df[(df['Start Part']=='794470')| (df['Start Part']== int(794470))]
            # all_reviews_df[(all_reviews_df['reviewTimestamp'].dt.year == 2019) | (all_reviews_df['reviewTimestamp'].dt.year == 2020)]
            # df = df.merge(df4,on=['WORKORDER_BASE_ID','WORKORDER_LOT_ID'])
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
    row0 = next(r)
    row0.extend(['R1 Mill','R1 CR %','R2 Mill','R2 CR %','R3 Mill','R3 CR %','R4 Mill','R4 CR %'])
    all.append(row0)
    roll_toup = [('R1 Mill','R1 CR %'),('R2 Mill','R2 CR %'),('R3 Mill','R3 CR %'),('R4 Mill','R4 CR %')]
    for i,row in enumerate(r):
        while len(row)!=len(row0):
            row.append('')
        if i==0:
            x = 0
            curr_base_id = row[1]
            curr_lot_id = row[2]
            curr_thickness = row[15]
            continue
        if row[1]!=curr_base_id or row[2]!=curr_lot_id:
            x = 1 
            curr_base_id = row[1]
            curr_lot_id = row[2]
            curr_thickness = row[15]
            # print(curr_base_id,curr_lot_id)
            continue
        if row[6] not in mill_list:
            row[15] = curr_thickness
        else:
            try:
                rf_thick = float(curr_thickness)
                rt_thick = (rf_thick)*100/float(row[7]) 
                row[15] = rt_thick
                curr_thickness = rt_thick
                percent_cr = ((rf_thick-rt_thick)/rf_thick)*100
                mill = row[6]
                row[row0.index(roll_toup[x][0])] = mill
                row[row0.index(roll_toup[x][1])] = percent_cr
                x+=1
            except (ValueError,ZeroDivisionError) as error:
                row[15] = curr_thickness
        all.append(row)
    w.writerows(all)
os.remove('WO ops data edit.csv')

# with open('S:/Automated Reports/VISUAL - Work Order Operations Data.csv','r',encoding="utf-8") as wo_input, open('S:/Automated Reports/VISUAL - Work Order Part Requirement.csv','r',encoding="utf-8") as wo_part_input:
#     df = pd.read_csv(wo_input,low_memory=False)
#     df = df[df['WORKORDER_TYPE']=='M']
#     # df.to_csv('WO ops data edit.csv', encoding="utf-8", index=False)
    
#     df1 = pd.read_csv('S:/Automated Reports/VISUAL - Parts Specification.csv','r', encoding="utf-8", usecols=['Part ID','Thickness','Width'])
#     df1.set_index('Part ID',inplace=True)
#     df1.dropna(inplace=True)

#     df2 = pd.read_csv(wo_part_input,usecols=['WORKORDER_TYPE','WORKORDER_BASE_ID','WORKORDER_LOT_ID','PART_ID'],low_memory=False)
#     df2 = df2[df2['WORKORDER_TYPE']=='W']
#     df2.dropna(subset=['PART_ID'], inplace=True)
#     df2.drop_duplicates(subset=['WORKORDER_BASE_ID','WORKORDER_LOT_ID'], inplace=True)
    
#     df3 = pd.read_csv('S:/Automated Reports/VISUAL - Parts Specification.csv','r', encoding="utf-8", usecols=['Part ID','Customer','Commodity Code','DESCRIPTION'])
#     df3['Commodity Code'] = df3.apply(lambda row:commcode_edit(row), axis=1)

#     # df4 = pd.read_csv('Work Order data.csv')
#     # df4 = pd.read_excel('WO Info by Resource 123122.xlsx', usecols=['WORKORDER_BASE_ID','WORKORDER_LOT_ID'])


#     df = df.merge(df2,on=['WORKORDER_TYPE','WORKORDER_BASE_ID','WORKORDER_LOT_ID'])
#     df = df.merge(df1,left_on='PART_ID',right_index=True)
#     df = df.rename(columns={'PART_ID':'Start Part'})
#     # df = df[(df['Start Part']=='794470')| (df['Start Part']== int(794470))]
#     # all_reviews_df[(all_reviews_df['reviewTimestamp'].dt.year == 2019) | (all_reviews_df['reviewTimestamp'].dt.year == 2020)]
#     # df = df.merge(df4,on=['WORKORDER_BASE_ID','WORKORDER_LOT_ID'])
#     df['Thickness'] = df['Thickness'].map(thickness_edit)
#     df['Alloy'] = df['WORKORDER_BASE_ID'].map(df3.set_index('Part ID')['Commodity Code'])
#     df['Customer'] = df['WORKORDER_BASE_ID'].map(df3.set_index('Part ID')['Customer'])
#     df['Alloy'] = df['Alloy'].map(alloy_edit)
#     df.to_csv('WO ops data edit.csv', encoding="utf-8", index=False)
