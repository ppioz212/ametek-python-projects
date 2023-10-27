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
def qty_good_edit(text):
    try:
        qty_good_list = {'0.0':0}
        for mist in qty_good_list:
            text = text.replace(mist,qty_good_list[mist])
    except:
        return text
def resource_id(text):
    resource_id_mapping = {'A DREVER #1':'A-D1','A DREVER #2':'A-D2','A DREVER #3':'A-D3','A DREVER GRP':'A-D GRP','A LINDBERG':'A-LIND','B BEAD BLAST':'BB',
                        'C ADS':'CLN-ADS','C LEWIS':'CLN-L','F BLOCKING':'F-BLK','F FOIL CLEAN':'F-CLN','F FOIL CLEAN #2':'F-CLN2','FOIL CLEAN GR':'F-CLN GRP',
                        'F FOIL MILL #1':'F-MILL #1','F FOIL MILL #2':'F-MILL #2','F FOIL MILL #3':'F-MILL #3','F FOIL MILL GRP':'F-MILL GRP','F SLITTERS':'F-SLIT',
                        'M 12 MILL #1':'12M-1','M 12 MILL #2':'12M-2','M 12 MILL GRP':'12M-GRP','M 14 MILL':'14M','M Z-HIGH MILL':'ZHI',}
    for mist in resource_id_mapping:
        try:
            text = text.replace(mist,resource_id_mapping[mist])
        except:
            return text
    return text
mill_list = ['F FOIL MILL #1','F FOIL MILL #2','F FOIL MILL GRP','M 12 MILL #1','M 12 MILL #2','M 12 MILL GRP','M 14 MILL','M Z-HIGH MILL']
op_type_mapping = {'12 MILL':'12M','14 MILL':'14M','ANNEALING':'Anneal','BASE PROCESS':'Base Proc.','CLEANING':'Clean','FOIL BLOCKING':'F-Block',
                    'FOIL CLEANING':'F-Clean','FOIL MILL':'F-Mill','FOIL SLITTING':'F-Slit','FOIL TRVRS WIND':'F-Wind','FOIL WRAP':'F-PK'}

with open('S:/Automated Reports/VISUAL - Work Order Operations Data.csv','r',encoding="utf-8") as wo_ops_input:

            # df = pd.read_csv('Master Ops Data Raw.csv')
            df = pd.read_csv(wo_ops_input,low_memory=False)
            df = df[df['WORKORDER_TYPE']=='W']
            df = df.sort_values(['WORKORDER_BASE_ID','WORKORDER_LOT_ID','WORKORDER_SUB_ID','SEQUENCE_NO'],axis=0)
            df['RESOURCE_ID'] = df['RESOURCE_ID'].map(resource_id)
            df.to_csv('WO ops data edit.csv', encoding="utf-8", index=False)
            
with open('WO ops shortage data.csv','w',encoding="utf-8",) as wo_output, open('WO ops data edit.csv','r',encoding="utf-8",) as wo_input:
    r = csv.reader(wo_input)
    input_row1 = next(r)

    qty_good_index = input_row1.index('QTY_GOOD')
    run_compl_index = input_row1.index('Run_Complete')
    seq_index = input_row1.index('SEQUENCE_NO')
    op_type_index = input_row1.index('OPERATION_TYPE')
    quant_index = input_row1.index('CALC_END_QTY')
    op_desc_index = input_row1.index('OP_DESCRIPTION')
    res_id_index = input_row1.index('RESOURCE_ID')

    skip_list = ['INSPECTION']
    w = csv.writer(wo_output,lineterminator='\n')
    all = []
    row0= ['WORKORDER_BASE_ID','WORKORDER_LOT_ID','Order Shortage']
    all.append(row0)
    for i,row in enumerate(r):
        if i==0:
            continue
        if i==1:
            curr_base_id = row[1]
            curr_lot_id = row[2]
            data = [curr_base_id,curr_lot_id]
            shortage_val = ''
        if row[1]!=curr_base_id or row[2]!=curr_lot_id:
            data.append(shortage_val)
            all.append(data)
            curr_base_id = row[1]
            curr_lot_id = row[2]
            data = [curr_base_id,curr_lot_id]
            shortage_val = ''
        if row[op_type_index] in skip_list:
            continue
        if row[run_compl_index] == 'Yes':
            if len(row[qty_good_index])==0 or float(row[qty_good_index]) < 30:
                continue
            else:
                try:
                    percent_loss = round((float(row[quant_index])-float(row[qty_good_index]))/float(row[quant_index]),3)
                except ZeroDivisionError:
                    continue
                if percent_loss > 0.1:
                    seq_no = 'OP#' + str(row[seq_index])
                    op = str(row[res_id_index])
                    shortage_val = shortage_val + op + ' ' + seq_no + ' Loss: ' + str(round(percent_loss*100,1)) + '%, '
    w.writerows(all)
os.remove('WO ops data edit.csv')
