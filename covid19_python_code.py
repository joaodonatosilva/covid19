%clear #clear console
# ========================== LIBRARIES ======================================
# Scientific Computing libraries
import numpy as np
import pandas as pd
import scipy as scipy
from scipy import stats
# Data Visualization
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

# ========================== DATA READING ===================================

# Extract Data deaths in Portugal from 2009-2020
data1=pd.read_csv("Data/Dados_SICO_2020-12-30-Nr_mortes.csv")

data2=pd.read_csv("Data/owid-covid-data.csv") # data covid all countries
# Extract Data Covid from Portugal
data2=data2.loc[data2['iso_code'] == 'PRT'] # data covid Portugal

# ========================== DATA ANALYSIS ==================================
# Data 1 - Deaths in PT
dy = data1.sum()
dy=dy.to_frame()
dy.drop(axis=0,index="Data",inplace=True)
dy.rename(columns={0:"Deaths"},inplace=True)
dc20=6906
dy.loc['2020','Deaths']=dy.loc['2020','Deaths']-dc20
dy.reset_index(inplace=True)
dy.rename(columns={"index":"Year"},inplace=True)

# Data 2 - Covid Numbers PT
# Create variable with number of deaths by month from 2015-2020
year=2015
num_years=2021-year
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
        temp = data1.loc[n:sum_days,year_str]
        pt_deaths_total_month[i,j] = temp.sum()
        year=year+1
    year=2015    
    n=n+days_per_month[i-1]
    if i != 12:
        sum_days = sum_days+days_per_month[i]

dm = pd.DataFrame(pt_deaths_total_month)

# Data 2 - Covid deaths and number of cases
df=data2.loc[:,["date","new_cases","new_deaths"]]
df.reset_index(inplace=True)
df.drop(columns=['index'],inplace=True)
df['new_cases']=df['new_cases'].fillna(0) #replace NaN by zeros
df['new_deaths']=df['new_deaths'].fillna(0) #replace NaN by zeros
df['month'] = pd.DatetimeIndex(df['date']).month
total=df.groupby('month')['new_cases','new_deaths'].sum()
total.loc[1,:]=0


# Chi-square test
#stats.chi2_contingency(total,correction=True)

# ========================== DATA VISUALIZATION =============================

# PLOT 1: Number of deaths in Portugal by year
array=[0,0,0,0,0,0,0,0,0,0,0,dc20]
average=dy.iloc[0:10,1].mean()

plt.bar(dy.loc[:,'Year'],dy.loc[:,'Deaths'],color="b",label="No Covid")
plt.bar(dy.loc[:,'Year'],array,bottom=dy.loc[:,'Deaths'],color="r",label="Covid")
plt.axhline(y = average, color = 'k', linestyle = '--')
plt.title('Portugal - Number of deaths by year')
plt.grid(linestyle=':')
plt.yticks(np.arange(0,130000,10000))
plt.xticks(fontsize=9)
plt.xlabel("Year")
plt.ylabel("Total of deaths")
plt.legend(fontsize=8)

# PLOT 2: Number of deaths in Portugal by month during 2015-2020
rows2=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
columns2=['2015','2016','2017','2018','2019','2020']
df2=pd.DataFrame(data=pt_deaths_total_month[1:13,:],index=rows2,columns=columns2)
df2.plot.bar()
plt.title('Portugal - Nr of deaths by month from 2015-2020')
plt.yticks(np.arange(0, 15000, 1000))
plt.grid(linestyle=':')

# PLOT 3
df2.plot()
plt.title('Portugal - Nr of deaths by month from 2015-2020')
plt.xticks(np.arange(12), rows2)
plt.grid(linestyle=':')
plt.show()

# PLOT 4
plt.subplot(2,1,1)
plt.title('Portugal - Nr of cases and deaths by Corona in 2020')
plt.bar(rows2,total.loc[:,'new_cases'],color="b",label="New cases")
plt.xlabel("Month")
plt.yticks(np.arange(0, 165000, 20000))
plt.legend(fontsize=8)
plt.grid(linestyle=':')

plt.subplot(2,1,2)
plt.bar(rows2,total.loc[:,'new_deaths'],color="r",label="New deaths")
plt.xlabel("Month")
plt.yticks(np.arange(0, 2500, 400))
plt.legend(fontsize=8)
plt.grid(linestyle=':')


# PLOT 5: Pearson plot with new_cases x new_deaths
# Pearson correlation
pearson_coef,p_value=stats.pearsonr(total['new_cases'],total['new_deaths'])
print("The Pearson Correlation Coefficient is", pearson_coef, " with a P-value of P =", p_value)  
# coef=0.91 => Large positive relationship 
# p=0,00003 => Strong certainty in the result

fig, ax1 = plt.subplots()
x = df['new_cases'];
y = df['new_deaths'];
ax1 = sns.regplot(x=x, y=y, marker=".")
ax1.set_title('Pearson correlation between new cases and new deaths')
ax1.set_xlabel('New cases') # returns a Text instance
ax1.set_ylabel('New deaths')
ax1.grid(axis='both',linestyle=':')
ax1.plot(label='Pearson coef: 0,91')
ax1.plot(label='p=0,00003')
ax1.text(0,270,'Pearson coef= 0,91',style ='italic',fontsize = 10,color ="black") 
ax1.text(0,250,'p=0,00003',style ='italic',fontsize = 10,color ="black") 
plt.show()