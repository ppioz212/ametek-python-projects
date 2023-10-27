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
def spec(spec_line):
    text = spec_line[spec_line.index(':')+1:]
    replace_list = {'  ':' ','   ':' ','..':'.','*':''}
    for k,v in replace_list.items():
        text = text.replace(k,v)
    if 'µ' in text:
        text = text.strip()
    else:
        text = text.strip().upper()
    if text.endswith('.'):
        text = text[:-1]
    text = text.strip()
    return text

spec_keys = {'Specs':[['Specs']],'Tensile (Long.)':[['Tensile','Long']],'Yield (Long.)':[['Yield','Long']],'Elong (Long.)':[['Elong','Long']],
    'Tensile (Trans.)':[['Tensile','Trans']],'Yield (Trans.)':[['Yield','Trans']],'Elong (Trans.)':[['Elong','Trans']],'Hardness':[['Hardness']],'Grain Size':[['Grain','Size']],
    'Microstructure':[['Microstructure']],'Grain Count':[['Grain','Count']],'Resistance':[['Resistance']],'Resistivity':[['Resistivity']],'Resist. Stability':[['Resist','Stability']],
    'TCR':[['TCR']],'Coverage':[['Coverage']],'Coil Set':[['Coil','Set']],'Camber':[['Camber']],'Flatness':[['Flatness']],'Cross Bow':[['Cross','Bow']],'Surface':[['Surface']],
    'Intergranular Corrosion':[['Intergranular','Corrosion'],['I.G.C']],'Finish':[['Finish']],'Edge Condition':[['Edge','Condition']],'Oxygen Analysis':[['Oxygen','Analysis']],
    'Hydrogen Analysis':[['Hydrogen','Analysis']],'Coil Requirements':[['Coil','Requirement']],
    'Coil Size':[['Size']],'Coil Core':[['Core']],'Packaging Requirements':[['Packag','Requirement']],'Container':[['Container']],'Labeling':[['Labeling']]}

key_list = list(spec_keys.keys())
with open('Part Spec edit new.csv','w') as csvoutput:
    edit_df = pd.read_csv('S:/Automated Reports/VISUAL - Parts Specification.csv', usecols=['PART_ID','Part_Specifications'])
    edit_df.to_csv('Part Spec input.csv',index=False)
    csvinput = open('Part Spec input.csv')
    r = csv.reader(csvinput)
    w = csv.writer(csvoutput,lineterminator='\n')
    all = []
    row0 = next(r)
    row0.extend(key_list)
    all.append(row0)
    for row in r:
        used_keys = {}
        try:
            spec_lines = row[1].split('\n')
        except IndexError:
            all.append(row)
            continue
        while len(row)!=len(row0):
            row.append('')
        while spec_lines:
            spec_line = spec_lines.pop(0)
            for (k, v) in spec_keys.items():
                found_match = False
                for match_list in v:
                    count = 0
                    for match_str in match_list:
                        if match_str in spec_line:
                            count += 1
                        if count == len(match_list) and k not in used_keys:
                            if ':' in spec_line:
                                row[row0.index(k)] = spec(spec_line)
                                used_keys[k] = True
                            else:
                                row[row0.index(k)] = ''
                                used_keys[k] = True
                            found_match = True
                            break
                if found_match:
                    break
        all.append(row)
    w.writerows(all)
csvinput.close()
os.remove('Part Spec input.csv')
df1 = pd.read_csv('S:/Automated Reports/VISUAL - Parts Specification.csv',usecols=['PART_ID','Customer','COMMODITY_CODE','DESCRIPTION','Temper','Width','Thickness','Surface_Finish','PRODUCT_CODE'])
df1['COMMODITY_CODE'] = df1.apply(lambda row:commcode_edit(row), axis=1)
df1 = df1.set_index('PART_ID')

df = pd.read_csv('Part Spec edit new.csv')
df['Customer'] = df['PART_ID'].map(df1['Customer'])
df['Customer'] = df['Customer'].map(customer_edit)
df['Alloy'] = df['PART_ID'].map(df1['COMMODITY_CODE'])
df['Alloy'] = df['Alloy'].map(alloy_edit)
df['Temper'] = df['PART_ID'].map(df1['Temper'])
df['Width'] = df['PART_ID'].map(df1['Width'])
df['Thickness'] = df['PART_ID'].map(df1['Thickness'])
df['Surface_Finish'] = df['PART_ID'].map(df1['Surface_Finish'])
df['PRODUCT_CODE'] = df['PART_ID'].map(df1['PRODUCT_CODE'])

df.replace('NAN',np.nan,inplace=True)
df = df[['PART_ID','Part_Specifications','Customer','Alloy','Temper','Width','Thickness','Surface_Finish','PRODUCT_CODE','Specs']
        +[c for c in df if c not in ['PART_ID','Part_Specifications','Customer','Alloy','Temper','Width','Thickness','Surface_Finish','PRODUCT_CODE','Specs']]]
df.to_csv('J:/Tech services/Part Spec data.csv',index=False)
os.remove('Part Spec edit new.csv')
def __main__():
    pass

if __name__ == "__main__":
    __main__()