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
num_years=2020-year+1
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

# -------------------------- DATA VISUALIZATION -----------------------------

# Graph 1: Number of deaths in Portugal by year
plt.bar(pt_deaths_total_year[0,:],pt_deaths_total_year[1,:])
plt.title('Portugal - Number of deaths by year')
plt.show()