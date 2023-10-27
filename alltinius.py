import pandas as pd
import datetime as dt
import time
import numpy as np
import re

def clean_text(text):
    try:
        text = text.strip().upper()
    except:
        pass
    return text
def countstr(params):
    count = 0
    for i in params:
        if isinstance(i,str):
            count +=1
    return count
def anneal_edit(text):
    text = str(text).upper().strip()
    if re.search("^(-?)(0?|([1-9][0-9]*))(\\.[0-9]+)?A?$",text) !=None:
        match = re.findall("([0-9]*\.?[0-9][0-9]*)",text)
        try:
            return 'RF. ' + str(float(match[0]))
        except:
            return text
    anneal_list = {'@':'/',' ':'','"':'','//':'/','+':'','2000FiPM':'2000F','12000F':'1200F','11375F':'1175F',
            '13525F':'1325F','1276F':'1275F','14285F':'1425F','1424F':'1425F','DREVER':'D',
            '11500':'1150','21500':'2150','16754F':'1675F','/F':'F/','/A/':'/AS/','#2':'D2',
            'O2':'N2','11PM':'11FPM',
            'PFM':'FPM','KF':'F',}
    start_list = {'200F':'2000F','110F':'1100F','150F':'1500F','170F':'1700F','195F':'1950F',}
    for mist in start_list:
        if text.startswith(mist):
            text = text.replace(mist,start_list[mist])
    for mist in anneal_list:
        text = text.replace(mist,anneal_list[mist])
    temp = 0
    if re.search("([0-9]{3,4}).{0,2}F?",text)!=None:
        match = re.findall("([0-9]{3,4}).{0,2}F?",text)
        temp = match[0]+'F'
    fpm = 0
    if re.search("([1-9]?[0-9]\.?5?)\D*F.{1,3}M",text)!=None:
        match = re.findall("([1-9]?[0-9]\.?5?)\D*F.{1,3}M",text)
        fpm = match[0]+'FPM'
    atmos = 0
    if 'HYDROGEN' in text or re.search("H.{0,2}2?",text)!=None:
        atmos = 'H2'
    elif re.search("A.{0,2}R|A.{0,2}S|A.{0,2}2",text)!=None:
        atmos = 'AS'
    elif 'NITROGEN' in text or re.search("N.{0,2}2?",text)!=None:
        atmos = 'N2'
    furnace = 0
    if  re.search("D.{0,2}1",text)!=None:
        furnace = 'D1'
    elif  re.search("D.{0,2}2",text)!=None:
        furnace = 'D2'
    elif  re.search("D.{0,2}3",text)!=None:
        furnace = 'D3'
    if countstr([temp,fpm,atmos,furnace])>2 and isinstance(temp,str) and isinstance(fpm,str):
        return str(temp)+'/'+str(fpm)+'/'+str(atmos)+'/'+str(furnace)
    elif re.search("R\.*\s*F",text)!=None and re.search("([0-9]*\.?[0-9][0-9]*)",text)!=None:
        match = re.findall("([0-9]*\.?[0-9][0-9]*)",text)
        try:
            return 'RF. ' + str(float('.'+str(match[0])))
        except:
            return 'RF. ' + str(float(match[0]))
    elif countstr([temp,fpm,atmos,furnace])<3:
        return text 
    else:
        return str(temp)+'/'+str(fpm)+'/'+str(atmos)+'/'+str(furnace)
def anneal_edit_2(text):
    if text==None:
        return np.nan
    text = str(text).upper().strip()
    if re.search("^(-?)(0?|([1-9][0-9]*))(\\.[0-9]+)?A?$",text) !=None:
        match = re.findall("([0-9]*\.?[0-9][0-9]*)",text)
        try:
            return 'RF. ' + str(float(match[0]))
        except:
            return 'Unedited'
    anneal_list = {' N ':'N2','10FPM/N':'FPM/N2','NSD1':'N2D1','@':'/',' ':'','"':'','//':'/','+':'','2000FiPM':'2000F','12000F':'1200F','11375F':'1175F',
            '13525F':'1325F','1276F':'1275F','14285F':'1425F','1424F':'1425F','DREVER':'D',
            '11500':'1150','21500':'2150','16754F':'1675F','/F':'F/','/A/':'/AS/','#2':'D2',
            'O2':'N2','11PM':'11FPM',
            'PFM':'FPM','KF':'F',}
    start_list = {'ANN 1':'1','200F':'2000F','110F':'1100F','150F':'1500F','170F':'1700F','195F':'1950F',}
    for mist in start_list:
        if text.startswith(mist):
            text = text.replace(mist,start_list[mist])
    for mist in anneal_list:
        text = text.replace(mist,anneal_list[mist])
    temp = 0
    if re.search("([0-9]{3,4}).{0,2}F?",text)!=None:
        match = re.findall("([0-9]{3,4}).{0,2}F?",text)
        tempval = float(match[0])
        temp = match[0]+'F'
    fpm = 0
    if re.search("([1-9]?[0-9]\.?5?)\D*F.{1,3}M",text)!=None:
        match = re.findall("([1-9]?[0-9]\.?5?)\D*F.{1,3}M",text)
        fpmval = float(match[0])
        fpm = match[0]+'FPM'
    atmos = 0
    if 'HYDROGEN' in text or re.search("H.{0,2}2?",text)!=None:
        atmos = 'H2'
    elif 'NITROGEN' in text or re.search("N.{0,2}2|NI",text)!=None:
        atmos = 'N2'
    elif re.search("A",text)!=None:
        atmos = 'AS'
    furnace = 0
    if  re.search("D.{0,2}1",text)!=None:
        furnace = 'D1'
    elif  re.search("D.{0,2}2",text)!=None:
        furnace = 'D2'
    elif  re.search("D.{0,2}3",text)!=None:
        furnace = 'D3'
    if isinstance(temp,str) and isinstance(fpm,str):
        return str(temp)+'/'+str(fpm)+'/'+str(atmos)+'/'+str(furnace)
    if countstr([temp,fpm,atmos,furnace])>2:
        return str(temp)+'/'+str(fpm)+'/'+str(atmos)+'/'+str(furnace)
    elif re.search("R\.*\s*F",text)!=None and re.search("([0-9]*\.?[0-9][0-9]*)",text)!=None:
        match = re.findall("([0-9]*\.?[0-9][0-9]*)",text)
        try:
            return 'RF. ' + str(float('.'+str(match[0])))
        except:
            return 'RF. ' + str(float(match[0]))
    elif countstr([temp,fpm,atmos,furnace])<3:
        if '?' in text:
            return np.nan
        else:
            return 'Unedited' 
    else:
        return str(temp)+'/'+str(fpm)+'/'+str(atmos)+'/'+str(furnace)
def anneal_finaledit(row):
    if row['Anneal Cycle Edit'] =='Unedited':
        return row['Ann Cycle/RF']
    else:
        return row['Anneal Cycle Edit']
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
def alloy_finaledit(row):
    if row['Alloy Temp'] == 'NAN':
        return row['Alloy']
    else:
        return row['Alloy Temp']
def alloy_edit(text):
    try:
        text = str(text).upper().strip()
        alloy_list = {'TI-GR1':'TI-GR 1','.':'','®':''}
        for mist in alloy_list:
            text = text.replace(mist,alloy_list[mist])
    except:
        pass
    return text
def baseid(text):
    text = str(text)
    return text[:7]
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
def size_edit(text):
    try:
        text = float(text)
        return text
    except:
        pass
    try:
        text = str(text).strip().upper()
        text = text.replace('..','.')
        if 'X' in text:
            text = float(text[:text.find('X')].strip())
    except:
        pass
    return text
def direction_edit(text):
    try:
        text = str(text).upper().strip()
        if text == 'L' or 'LONG' in text:
            text = 'LONG'
        elif text =='T' or 'TRANS' in text:
            text = 'TRANS'
    except:
        pass
    return text
def wo_edit(text):
    text = str(text).upper().strip()
    if len(text) == 6:
        text = '0' + text + '/1'
    return text
def anneal_temp(row):
    try:
        if row['Anneal Cycle Edit']!='Unedited' and 'RF' not in row['Anneal Cycle Edit'] and row['Anneal Cycle Edit'].split('/')[0]!=0:
            return int(row['Anneal Cycle Edit'].split('/')[0][:-1])
        else:
            return np.nan
    except:
        return np.nan
def anneal_fpm(row):
    try:
        if row['Anneal Cycle Edit']!= 'Unedited' and 'RF' not in row['Anneal Cycle Edit'] and row['Anneal Cycle Edit'].split('/')[1]!=0:
            return float(row['Anneal Cycle Edit'].split('/')[1][:-3])
        else:
            return np.nan
    except:
        return np.nan
def anneal_furnace(row):
    try:    
        if row['Anneal Cycle Edit']!= 'Unedited' and 'RF' not in row['Anneal Cycle Edit'] and row['Anneal Cycle Edit'].split('/')[1]!=0:
            return row['Anneal Cycle Edit'].split('/')[3]
        else:
            return np.nan
    except:
        return np.nan
def percentcr(row):
    try:    
        if row['Anneal Cycle Edit']!= 'Unedited' and 'RF' in row['Anneal Cycle Edit']:
            if re.search("([0-9]*\.?[0-9][0-9]*)",row['Anneal Cycle Edit'])!=None:
                match = re.findall("([0-9]*\.?[0-9][0-9]*)",row['Anneal Cycle Edit'])
                return round(1-float(row['Size'])/float(match[0]),2)
    except:
        return np.nan
def mpi(row):
    furn_length = {'D1':6,'D2':12,'D3':7.5}
    try:
        mpi = (furn_length[row['Ann-Furnace']])/(row['Ann-FPM']*row['Size'])
        return mpi
    except:
        return np.nan


start = time.time()
df = pd.read_csv("Tinius Information 00-20.csv")
df.replace([0,'0','.','?','5%','6%'],np.nan,inplace=True)
df = df.drop_duplicates()
print(len(df.index))
# index_drop = df[(df['Process Number']=='') & (df['Ann Cycle/RF']=='')].index
# df.drop(index_drop, inplace=True)
df['Process Number'] = df['Process Number'].map(wo_edit)
df = df[~df['Process Number'].str.contains('VER')]

df1 = pd.read_csv('Work Order Data.csv',usecols=['Type','Base ID','Part ID'])
df1 = df1[df1['Type']=='W']
df1['Base ID']=df1['Base ID'].map(wo_edit)

df2 = pd.read_csv('Part number data.csv',usecols=['Part ID','Customer','Commodity Code','Description'])
df2['Commodity Code'] = df2.apply(lambda row:commcode_edit(row), axis=1)
merge_df = pd.merge(df1,df2,left_on=['Part ID'],right_on=['Part ID'],how='left')
merge_df = merge_df.set_index('Base ID')
merge_df = merge_df.loc[~merge_df.index.duplicated(keep='first')]

df['Base ID'] = df['Process Number'].map(baseid)
df['Part Number'] = df['Base ID'].map(merge_df['Part ID'])
df['Alloy Temp'] = df['Part Number'].map(df2.set_index('Part ID')['Commodity Code'])
df['Alloy Temp'] = df['Alloy Temp'].map(alloy_edit)
df['Alloy'] = df.apply(lambda row:alloy_finaledit(row), axis=1)
df['Alloy'] = df['Alloy'].map(alloy_edit)
df.drop(['Alloy Temp','Base ID'], axis=1,inplace=True)
df['Customer'] = df['Part Number'].map(df2.set_index('Part ID')['Customer'])
df['Customer'] = df['Customer'].map(customer_edit)
df['Size'] = df['Size'].map(size_edit)
df['Direction'] = df['Direction'].map(direction_edit)
df['Scale'] = df['Scale'].map(clean_text)
df['Tensile'] = np.where((df['Scale']=='MPA'), df['Tensile']*0.145038, df['Tensile'])
df['Yield'] = np.where((df['Scale']=='MPA'), df['Yield']*0.145038, df['Yield'])
# df['Anneal Test'] = df['Ann Cycle/RF'].map(anneal_edit)
df['Anneal Cycle Edit'] = df['Ann Cycle/RF'].map(anneal_edit_2)
df['Ann-Temp'] = df.apply(lambda row:anneal_temp(row),axis=1)
df['Ann-FPM'] = df.apply(lambda row:anneal_fpm(row),axis=1)
df['Ann-Furnace'] = df.apply(lambda row:anneal_furnace(row),axis=1)
df['CR %'] = df.apply(lambda row:percentcr(row),axis=1)
df['MPI'] = df.apply(lambda row:mpi(row),axis=1)
df['Anneal Cycle Edit'] = df.apply(lambda row:anneal_finaledit(row),axis=1)
# df.drop('Ann Cycle/RF',axis=1,inplace=True)
df.replace('NAN',np.nan,inplace=True)
df.dropna(how='all',subset=['Part Number','Anneal Cycle Edit'],inplace=True)
df.dropna(how='any',subset=['Tensile','Yield','Elongation'],inplace=True)
print(len(df.index))
df = df[['Process Number', 'Part Number','Anneal Cycle Edit','CR %','Ann-Temp','Ann-FPM','Ann-Furnace','MPI','Size',]
        +[c for c in df if c not in ['Process Number', 'Part Number','Anneal Cycle Edit','MPI','Size','CR %','Ann-Temp','Ann-FPM','Ann-Furnace',]]]
df.to_csv('Total Tinius Edit.csv',index=False)
# df.to_csv('Tinius Information 00-20.csv',index=False)
end = time.time()
print(end - start)


# csvname = "initial edit.csv"
# df.to_csv(csvname, index=False)
# file= open(csvname, newline="")
# csvfile = csv.reader(file)
# def removeperiod(date):
#     return date.replace('.','')

# with open('Final edit.csv', 'w+', newline = '') as file:
#     final_list = [output[key].signifier + output[key].data for key in output]
#     write = csv.writer(file)
#     write.writerows(final_list)

# Anneal Edit extras for old method
    # if text.find('FPM')!=-1:
    #     if text[4]=='F' and text[5]!='/':
    #         text = text[:5] + '/' + text[5:]
    #     elif text[4]!='F' and text[5]=='/':
    #         text = text[:4] + 'F' + text[4:]
    #     elif text[4]!='F' and text[5]!='/':
    #         text = text[:4] + 'F/' + text[4:]
    #     if text[text.find('FPM')+3]!='/':
    #         text = text[:text.find('FPM')+3] + '/' + text[text.find('FPM')+3:]
    #     for atmos in ['AS','N2','H2']:
    #         if text.find(atmos)!=-1 and text[text.find(atmos)+2]!='/':
    #             text = text[:text.find(atmos)+2] + '/' + text[text.find(atmos)+2:]
    #     anneal_list2 = {'D/SD3':'AS/D3','D/S':'AS','DS':'D2','SD1':'D1','AD1':'AS/D1','2D1':'D1','HD2':'H2/D2','D3H2':'H2/D3','//':'/',
    #                     'AS/S/D3':'AS/D3','/N/D1':'/N2/D1','SD3':'D3','HD1':'H2/D1','HD3':'H2/D3','D1H2':'H2/D1','1995F/0F':'1995F'}
    #     for mist in anneal_list2:
    #         text = text.replace(mist,anneal_list2[mist])
