import csv
import pandas as pd
import datetime as dt


df = pd.read_excel("CoPQ Data.xlsx")
df = df.drop_duplicates()
# for col in df.columns:
#     print(col)
def clean_number(text):
    try:
        return float(str(text).strip())
    except:
        pass
df = df[df["YEAR EVENT DATE"]>2021]
df['ALLOY'] = df['ALLOY'].map(lambda a:str(a).strip().upper())
df['PART NUMBER'] = df['PART NUMBER'].map(lambda a:str(a).strip().upper())
df['PART THICKNESS (in)'] = df['PART THICKNESS (in)'].map(lambda a:clean_number(a))
df['PART WIDTH (in)'] = df['PART WIDTH (in)'].map(lambda a:clean_number(a))

# print(df['PART NUMBER'].value_counts()[:10])
# print(df['DEFECT NAME'].value_counts()[:10])
# new_df = df.groupby(['PART NUMBER','CUSTOMER','ALLOY','PART THICKNESS (in)','PART WIDTH (in)'])['TOTAL COST OF POOR QUALITY'].sum()
# out = df.groupby('PART NUMBER', as_index=False, sort=False).agg({'TOTAL COST OF POOR QUALITY':'sum', 'CUSTOMER':'first'})
new_df = df.groupby(['PART NUMBER','PART THICKNESS (in)','PART WIDTH (in)'])['TOTAL COST OF POOR QUALITY'].sum()
new_df = new_df.sort_values(ascending=False)[:20]
print(new_df)
# new_df.to_csv('copqprocessed.csv')
# new_df = df.groupby(by='DEFECT NAME')['TOTAL COST OF POOR QUALITY'].sum()
# print(new_df.sort_values(ascending=False)[:10])
# new_df = df.groupby(by='DEFECT CATEGORY')['TOTAL COST OF POOR QUALITY'].sum()
# print(new_df.sort_values(ascending=False)[:10])

# new_df = df.groupby(['PART NUMBER','TOTAL COST OF POOR QUALITY'], sort=True).sum().reset_index()
# new_df = new_df.sort_values(by = 'TOTAL COST OF POOR QUALITY', ascending=False)
# new_df = new_df[['PART NUMBER','TOTAL COST OF POOR QUALITY']][:15]
# print((new_df))


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