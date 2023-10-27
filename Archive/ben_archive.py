import csv
import pandas as pd
import datetime as dt
import re
import numpy as np
import os
def customer_edit(text):
    try:
        text = str(text).upper().strip()
        if text.startswith('HPM'):
            return text
        customer_mapping = {('®',):'',('B&C','B & C'):'B & C SPEAKERS SPA',
        ('BRUNK',):'BRUNK INDUSTRIES INC',('BROOK',):'BROOKS INSTRUMENT LLC',('EASTERN',):'EASTERN INDUSTRIES CORPORATION',
        ('FORTIVE SETRA',):'FORTIVE SETRA ICG TIANJIN CO LTD',('GREATBATCH',):'GREATBATCH INC',('HINES',):'HINES PRECISON INC',('HONEYWELL',):'HONEYWELL INTERNATIONAL',
        ('MATINO',):'MATINO MEDICAL DEVICES GMBH & CO KG',('MEIER',):'MEIER TOOL & ENGINEERING INC',('MINCO',):'MINCO PRODUCTS',('MPS',):'MPS MICRO PRECISION SYSTEMS AG',
        ('PALL',):'PALL AEROPOWER CORPORATION',('RCF',):'RCF SPA',('TECOMET',):'TECOMET INC.',('TECH ETCH',):'TECH ETCH INC'}
        for key in customer_mapping:
            for word in key:
                if word in text:
                    text = customer_mapping[key]
    except:
        pass
    return text
def alloy_edit(text):
    try:
        text = str(text).upper().strip()
        alloy_list = {'TI-GR1':'TI-GR 1','.':'','®':''}
        for mist in alloy_list:
            text = text.replace(mist,alloy_list[mist])
    except:
        pass
    return text
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

spec_keys = {'Tensile (Long.)':['Tensile','Long'],'Yield (Long.)':['Yield','Long'],'Elong (Long.)':['Elong','Long'],
    'Tensile (Trans.)':['Tensile','Trans'],'Yield (Trans.)':['Yield','Trans'],'Elong (Trans.)':['Elong','Trans'],'Hardness':['Hardness'],'Grain Size':['Grain','Size'],
    'Microstructure':['Microstructure'],'Grain Count':['Grain','Count'],'Resistivity':['Resistivity'],'Resist. Stability':['Resist','Stability'],'Coil Set':['Coil','Set'],
    'Camber':['Camber'],'Flatness':['Flatness'],'Cross Bow':['Cross','Bow'],'Coil Requirements':['Coil','Requirement'],'Coil Size':['Size'],
    'Coil Core':['Core'],'Packaging Requirements':['Packag','Requirement'],'Container':['Container'],'Labeling':['Labeling']}
key_list = list(spec_keys.keys())
with open('VISUAL - Parts Specification.csv','r') as csvinput, open('Part Spec edit normal.csv','w') as csvoutput:
    r = csv.reader(csvinput)
    w = csv.writer(csvoutput,lineterminator='\n')
    all = []
    row0 = next(r)
    row0.extend(key_list)
    all.append(row0)
    # First, we need a way to determine when we are reading data for a new part
    # For each key we get, we'll add it to a list / set / dictionary
    for row in r:
        used_keys = {}
        try:
            spec_lines = row[1].split('\n')
        except IndexError:
            all.append(row)
            continue
        while spec_lines:
            spec_line = spec_lines.pop(0)
            for (k, v) in spec_keys.items():
                count = 0
                found_match = False
                for match_str in v:
                    if match_str in spec_line:
                        count += 1
                    if count == len(v) and k not in used_keys:
                        try:
                            row.append(spec_line.split(':')[1].replace('*','').strip())
                            used_keys[k] = True
                        except IndexError:
                            print('Error found at ' + row[0] + ' for ' + k)
                            row.append('')
                            used_keys[k] = True
                        found_match = True
                        break
                if found_match:
                    break
            # Find way to make it so that if you don't find anything, you add a value still so it 
            # doesn't mess up the order (it's doing that right now)
            # if count == 0:
            #     row.append(' ')   
        # find what keys didn't get used. Look for index corresponding to key. Insert element where it wasn't found. Covers all specs that aren't found.
        missed_keys = list(set(key_list).difference(used_keys))
        if len(missed_keys)!=0:
            for mkey in missed_keys:
                row.insert(row0.index(mkey),'Key not found')
        all.append(row)
    w.writerows(all)

df1 = pd.read_csv('Part number data.csv',usecols=['Part ID','Customer','Commodity Code','Description','Temper','Width','Thickness','Surface Finish','Product Code'])
df1['Commodity Code'] = df1.apply(lambda row:commcode_edit(row), axis=1)
df1 = df1.set_index('Part ID')

df = pd.read_csv('Part Spec edit normal.csv')
df['Customer'] = df['PART_ID'].map(df1['Customer'])
df['Customer'] = df['Customer'].map(customer_edit)
df['Alloy'] = df['PART_ID'].map(df1['Commodity Code'])
df['Alloy'] = df['Alloy'].map(alloy_edit)
df['Temper'] = df['PART_ID'].map(df1['Temper'])
df['Width'] = df['PART_ID'].map(df1['Width'])
df['Thickness'] = df['PART_ID'].map(df1['Thickness'])
df['Surface Finish'] = df['PART_ID'].map(df1['Surface Finish'])
df['Product Code'] = df['PART_ID'].map(df1['Product Code'])

df.replace('NAN',np.nan,inplace=True)
df = df[['PART_ID','Part_Specifications','Customer','Alloy','Temper','Width','Thickness','Surface Finish']
        +[c for c in df if c not in ['PART_ID','Part_Specifications','Customer','Alloy','Temper','Width','Thickness','Surface Finish']]]
df.to_csv('Part Spec edit normal.csv',index=False)
def __main__():
    pass

if __name__ == "__main__":
    __main__()