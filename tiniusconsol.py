import csv
import pandas as pd
import datetime as dt
import re
import numpy as np
import os

def base_id(text):
    text = str(text).strip()
    if len(text)>7:
        text = text[:7]
    return text
def date_edit(text):
    text = str(text).strip()
    try:
        date = dt.datetime.strptime(text,'%m/%d/%Y %H:%M:%S %p')
    except:
        date = dt.datetime.strptime(text,'%m/%d/%Y')
    return date.date()
def countstr(params):
    count = 0
    for i in params:
        if isinstance(i,str):
            count +=1
    return count
def size_edit(text):
    try:
        text = float(text)
        return text
    except:
        pass
    try:
        text = str(text).strip().upper()
        text = text.replace('"','')
        text = text.replace('..','.')
        if 'X' in text:
            text = float(text[:text.find('X')].strip())
    except:
        pass
    return text
def anneal_edit(text):
    try:
        text = str(text).upper().strip()
        if text.startswith('RF '):
            return text.split()[0] + '. ' + str(float(text.split()[1]))
        if text.startswith('RF.'):
            return text.split()[0] + ' ' + str(float(text.split()[1]))
        if re.search("^(-?)(0?|([1-9][0-9]*))(\\.[0-9]+)?$",text) !=None:
            text = 'RF. ' + str(float(text))
        anneal_list = {'//':'/','A/S':'AS','AR':'AS','D-3AS':'AS/D3','170F':'1700F','21500F':'2150F','150F':'1500F','16754F':'1675F','@':'/',' ':'','"':''}
        for mist in anneal_list:
            text = text.replace(mist,anneal_list[mist])
        if text.find('FPM')!=-1:
            if text[4]=='F' and text[5]!='/':
                text = text[:5] + '/' + text[5:]
            elif text[4]!='F' and text[5]=='/':
                text = text[:4] + 'F' + text[4:]
            elif text[4:6]!='F/':
                text = text[:4] + 'F/' + text[6:]
            if text[text.find('FPM')+3]!='/':
                text = text[:text.find('FPM')+3] + '/' + text[text.find('FPM')+3:]
            for atmos in ['AS','N2','H2']:
                if text.find(atmos)!=-1 and text[text.find(atmos)+2]!='/':
                    text = text[:text.find(atmos)+2] + '/' + text[text.find(atmos)+2:]
    except:
        pass
    return text
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
    if row['Anneal Test 2'] =='Unedited':
        return row['Anneal cycle']
    else:
        return row['Anneal Test 2']
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
def date_edit(text):
    return str(text).replace('.','')
def removeperiod(date):
        return date.replace('.','')
def convert_date(date):
    try:
        converted_date = dt.datetime.strptime(date, '%M/%d/%Y')
    except ValueError:
        try:
            converted_date = dt.datetime.strptime(date, '%M/%d/%y')
        except ValueError:
            converted_date = date
    return converted_date
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
def alloy_finaledit(row):
    if row['Alloy Temp'] == 'NAN':
        return row['Alloy']
    else:
        return row['Alloy Temp']
def anneal_temp(row):
    try:
        if row['Anneal Test 2']!='Unedited' and 'RF' not in row['Anneal Test 2'] and row['Anneal Test 2'].split('/')[0]!=0:
            return int(row['Anneal Test 2'].split('/')[0][:-1])
        else:
            return np.nan
    except:
        return np.nan
def anneal_fpm(row):
    try:
        if row['Anneal Test 2']!= 'Unedited' and 'RF' not in row['Anneal Test 2'] and row['Anneal Test 2'].split('/')[1]!=0:
            return float(row['Anneal Test 2'].split('/')[1][:-3])
        else:
            return np.nan
    except:
        return np.nan
def anneal_furnace(row):
    try:    
        if row['Anneal Test 2']!= 'Unedited' and 'RF' not in row['Anneal Test 2'] and row['Anneal Test 2'].split('/')[1]!=0:
            return row['Anneal Test 2'].split('/')[3]
        else:
            return np.nan
    except:
        return np.nan
def percentcr(row):
    try:    
        if row['Anneal Test 2']!= 'Unedited' and 'RF' in row['Anneal Test 2']:
            if re.search("([0-9]*\.?[0-9][0-9]*)",row['Anneal Test 2'])!=None:
                match = re.findall("([0-9]*\.?[0-9][0-9]*)",row['Anneal Test 2'])
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
class DataRow():
    def __init__(self, date, data, signifier):
        self.date = date
        self.data = data
        self.signifier = signifier

    def older_than(self, other):
        return convert_date(self.date) < convert_date(other.date)
    def combine(self, other):
        new_row = DataRow(self.date, self.data,self.signifier)
        for i, d in enumerate(other.data):
            if new_row.data[i] == '' and d != '':
                new_row.data[i] = d
            elif new_row.data[i] != '' and d != '':
                try:
                    if new_row.older_than(other):
                        new_row.data[i] = d
                except:
                    new_row.data[i] = d
        return new_row
df = pd.read_csv('S:/Tinius/Tinius/horizon outputs/Verification Sample.csv', low_memory=False)
df = df.replace('HEAT TREAT','HEAT TREATED')
df.replace([0,'0','.','?','5%','6%'],np.nan,inplace=True)
df = df.drop_duplicates()

df_pdata = pd.read_csv('S:/Automated Reports/VISUAL - Parts Specification.csv',usecols=['PART_ID','Customer','COMMODITY_CODE','DESCRIPTION'])
df_pdata['COMMODITY_CODE'] = df_pdata.apply(lambda row:commcode_edit(row), axis=1)
with open('S:/Automated Reports/VISUAL - Work Order Part Requirement.csv','r',encoding="utf-8") as wo_part_input:
    df_wo = pd.read_csv(wo_part_input)
    df_wo.dropna(subset=['Start_Part_ID'], inplace=True)
    df_wo.drop_duplicates(subset=['WORKORDER_BASE_ID'],inplace=True)
    df['Base ID'] = df['Work Order'].map(base_id)
    df['Part Number'] = df['Base ID'].map(df_wo.set_index('WORKORDER_BASE_ID')['End_Part_ID'])
    df.drop('Base ID',axis=1,inplace=True)
    df['Customer'] = df['Part Number'].map(df_pdata.set_index('PART_ID')['Customer'])
    df['Customer'] = df['Customer'].map(customer_edit)
    df['Alloy Temp'] = df['Part Number'].map(df_pdata.set_index('PART_ID')['COMMODITY_CODE'])
    df['Alloy Temp'] = df['Alloy Temp'].map(alloy_edit)
    df['Alloy'] = df.apply(lambda row:alloy_finaledit(row), axis=1)
    df['Alloy'] = df['Alloy'].map(alloy_edit)
    df.drop('Alloy Temp', axis=1,inplace=True)
    df['Direction'] = df['Direction'].map(direction_edit)
    df['Size'] = df['Size'].map(size_edit)
    df['Anneal Test 2'] = df['Anneal cycle'].map(anneal_edit_2)
    df['Date'] = df['Date'].map(date_edit)
    df['Ann-Temp'] = df.apply(lambda row:anneal_temp(row),axis=1)
    df['Ann-FPM'] = df.apply(lambda row:anneal_fpm(row),axis=1)
    df['Ann-Furnace'] = df.apply(lambda row:anneal_furnace(row),axis=1)
    df['CR %'] = df.apply(lambda row:percentcr(row),axis=1)
    df['MPI'] = df.apply(lambda row:mpi(row),axis=1)
    df.drop('Anneal Test 2',axis=1, inplace=True)
    df.replace('NAN',np.nan,inplace=True)
    # df.dropna(how='all',subset=['Part Number','Anneal Test 2'],inplace=True)
    df.dropna(how='any',subset=['Tensile','Yield','Elongation'],inplace=True)

    # print(df.head())

    csvname = 'middle edit.csv'
    df.to_csv(csvname, index=False)
    middlefile= open(csvname, newline="")
    csvfile = csv.reader(middlefile)

    output = {}
    for  line in csvfile:
        key = "".join(line[:8] + line[9:14])
        date = line[20]
        data = line[14:]
        signifier = line[:14]
        row = DataRow(date, data, signifier)
        if key in output:
            output[key] = output[key].combine(row)
        else:
            output[key] = row 
        # print(output[key].signifier + output[key].data)
    middlefile.close()
    os.remove('middle edit.csv')

with open('tinius 21-22 edit.csv', 'w+', newline = '') as file:
    final_list = [output[key].signifier + output[key].data for key in output]
    write = csv.writer(file)
    write.writerows(final_list)
df = pd.read_csv('tinius 21-22 edit.csv')
df.rename(columns={'Anneal cycle':'Anneal Cycle/RF'},inplace=True)
df_mech = pd.read_excel('Mechanical Testing Data 2000-2021.xlsx')
df = df[['Work Order', 'Part Number','Anneal Cycle/RF','CR %','Ann-Temp','Ann-FPM','Ann-Furnace','MPI','Size',]
        +[c for c in df if c not in ['Work Order', 'Part Number','Anneal Cycle/RF','MPI','Size','CR %','Ann-Temp','Ann-FPM','Ann-Furnace',]]]
df = pd.concat([df_mech,df],ignore_index=True)
# df['Date'] = df['Date'].map(date_edit)
print(df.shape)
df.drop_duplicates(inplace=True)
print(df.shape)
os.remove('tinius 21-22 edit.csv')
df.to_csv('J:/Tech services/Tinius Data (Daily Refresh).csv',index=False)

# Excessive customer mapping if ever needed
# customer_mapping = {('ACOUSTIC',):'ACOUSTIC DESIGN INC',('B&C',):'B & C SPEAKERS SPA',('BIRK',):'BIRK MANUFACTURING',
# ('BRUNK',):'BRUNK INDUSTRIES INC',('BROOK',):'BROOKS INSTRUMENT LLC',('BOSTON',):'BOSTON SCIENTIFIC/GUIDANT',('CARBOFIX',):'CARBOFIX ORTHOPEDICS LTD',
# ('QING','QUING'):'CHONGQING SILIAN MEASURE & CONTROL TECHNOLOGY CO L',('PICHER',):'EAGLEPICHER TECHNOLOGIES LLC',('EASTERN',):'EASTERN INDUSTRIES CORPORATION',
# ('GREATBATCH',):'GREATBATCH INC',('HAM-LET',):'HAM-LET ADVANCED CONTROL TECHNOLOGY',('HONEYWELL',):'HONEYWELL INC',('HERAEUS',):'HERAEUS MEDICAL COMPONENTS DIVISION',
# ('HUDSON',):'HUDSON TECHNOLOGIES',('IRCA',):'IRCA SPA',('ITT',):'ITT AEROSPACE CONTROLS',('J.T.D','JTD'):'JTD STAMPING CO INC',('KLESK METAL',):'KLESK METAL STAMPING',
# ('MATINO',):'MATINO MEDICAL DEVICES GMBH & CO KG',('MEIER',):'MEIER TOOL & ENGINEERING INC',('MINCO',):'MINCO PRODUCTS',('MPS',):'MPS MICRO PRECISION SYSTEMS AG',
# ('PALL',):'PALL AEROPOWER CORPORATION',('PCT',):'PCT EBEAM AND INTEGRATION, LLC',('PENN UNITED',):'PENN UNITED TECHNOLOGIES INC',('RCF',):'RCF SPA',
# ('SENIOR',):'SENIOR OPERATIONS LLC',('SENSATA',):'SENSATA TECHNOLOGIES INC',('JUDE',):'ST JUDE MEDICAL AB',('TECOMET',):'TECOMET INC.',('TRANSLOGIC',):'TRANSLOGIC',
# ('VERIFLO',):'VERIFLO DIV/INSTRUMENTATION GROUP'}
