%clear #clear console

# -------------------------- LIBRARIES --------------------------------------
# Linear algebra
import numpy as np

# Data processing
import pandas as pd


# Data Visualization
import matplotlib.pyplot as plt

plt.close('all')

# -------------------------- DATA READING -----------------------------------
data1=pd.read_csv("Data/owid-covid-data.csv") # data covid all countries

# Extract Data from Portugal
data1_pt=data1.loc[data1['iso_code'] == 'PRT'] # [2020/02/02 - 2020/12/19]


data2=pd.read_csv("Data/Dados_SICO_2020-12-20-Nr_mortes.csv")

# -------------------------- DATA ANALYSIS ----------------------------------

# Create variable with number of deaths by year in Portugal
year=2015
num_years=2021-year
pt_deaths_total_year = np.zeros((2,num_years))
pt_deaths_total_year[0,:]=range(year,2021)
pt_deaths_total_year = pt_deaths_total_year.astype('int32')
i=0

while ( year != 2021):
    year_str = str(year) 
    temp = data2.loc[:,[year_str]]
    pt_deaths_total_year[1,i]=temp.sum(axis=0,skipna=True)
    year = year+1
    i=i+1

# Create variable with number of deaths by month for 6 years in Portugal
pt_deaths_total_month = np.zeros((13,num_years))
pt_deaths_total_month[0,[0,1,2,3,4,5]] = range(2015,2021)

year=2015
days_per_month=[31,29,31,30,31,30,31,31,30,31,30,31]
j=0
i=1
n=0
sum_days = days_per_month[0]-1

for i in range(1,13):    # Cycle per each month
    for j in range(0,6):    # Cycle per each year
        year_str=str(year)
        temp = data2.loc[n:sum_days,year_str]
        pt_deaths_total_month[i,j] = temp.sum()
        year=year+1
    year=2015    
    n=n+days_per_month[i-1]
    if i != 12:
        sum_days = sum_days+days_per_month[i]
    

# -------------------------- DATA VISUALIZATION -----------------------------

# Graph 1: Number of deaths in Portugal by year
plt.bar(pt_deaths_total_year[0,:],pt_deaths_total_year[1,:])
plt.title('Portugal - Number of deaths by year')
plt.show()

# Graph 2: Number of deaths in Portugal by month during 2015-2020
# =============================================================================
# plt.figure()
# f, axes = plt.subplots(1, 4, sharey=True)
# plt.title('Portugal - Nr of deaths by month from 2015-2020')
# 
# for k in range(1,13):
#     plt.subplot(2,6,k)
#     plt.bar(pt_deaths_total_month[0,:],pt_deaths_total_month[k,:])
# =============================================================================

# Graph 3: Number of deaths in Portugal by month during 2015-2020
rows1=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
columns1=['2015','2016','2017','2018','2019','2020']
df=pd.DataFrame(data=pt_deaths_total_month[1:13,:],index=rows1,columns=columns1)
df.plot.bar()
plt.title('Portugal - Nr of deaths by month from 2015-2020')