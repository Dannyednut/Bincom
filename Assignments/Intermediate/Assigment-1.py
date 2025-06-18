import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

dataset = pd.read_csv("dataset/fifa21_raw_data.csv")
data = pd.DataFrame(dataset)

"""
1. Convert the height and weight columns to numerical forms
"""
def convert_to_int(value):
    if 'lbs' in value:
        return int(value.replace('lbs', ''))
    elif '"' in value:
        value = value.replace('"', '')
        feet, inches = value.split('\'')
        return int(feet) * 12 + int(inches)

data['Height'] = data['Height'].apply(convert_to_int)
data['Weight'] = data['Weight'].apply(convert_to_int)
data[['Height','Weight']].dtypes

"""
2. Remove the unnecessary newline characters from all columns that have them.
"""
#Lets check which columns have values with '\n' character
mapping = {}
cols = data.columns.tolist()
for col in cols:
    n = 0
    for i in data[col]:
        if '\n' in str(i):
            n+=1
            mapping[col] = n

print(mapping) #output: {'Team & Contract': 18979, 'Hits': 16384}

#Lets replace the '\n' in 'Team & Contract' and 'Hits' column
data['Team & Contract'] = data['Team & Contract'].str.replace('\n','')
data['Hits'] = data['Hits'].str.replace('\n','')
data[['Team & Contract','Hits']].head()

"""
3.
"""
#Convert value to datatime format
data['Joined'] = pd.to_datetime(data['Joined'], format='%b %d, %Y')
#get the all 'Joined' rows of duplicate players
duplicates = data['Joined'][data['LongName'].duplicated()]
# Check the min
print(duplicates.min()) #output: 2010-01-01 00:00:00
print(duplicates.max()) #output: 2020-10-05 00:00:00

# We conclude that all players with duplicated value have change clubs within 10 years.
# We anaylize players without duplcates.
unique_players = data[['LongName','Joined']][~data['LongName'].duplicated(keep=False)]
unique_players['Years'] = (datetime.now() - unique_players['Joined']).dt.days/365.25
unique_players[unique_players['Years']>10]

"""
4.
"""
def convert(value):
    if 'M' in value:
        value = value.replace('€', '')
        return float(value.replace('M', ''))*1000000
    elif 'K' in value:
        value = value.replace('€', '')
        return float(value.replace('K', ''))*1000
    else:
        return float(value.replace('€', ''))
       
data['Value'] = data['Value'].apply(convert)
data['Wage'] = data['Wage'].apply(convert)
data['Release Clause'] = data['Release Clause'].apply(convert)
data[['Value','Wage','Release Clause']]

"""
5. 
"""
columns = {}
cols = data.columns.tolist()
for col in cols:
    n = 0
    for i in data[col]:
        if '★' in str(i):
            n+=1
            columns[col] = n

print(columns)

data['W/F'] = data['W/F'].str.replace('★', '')
data['SM'] = data['SM'].str.replace('★','')
data['IR'] = data['IR'].str.replace('★', '')
data[['W/F','SM', 'IR']]

"""
6.
"""
avg_value = data['Value'].mean()
avg_wage = data['Wage'].mean()

value_threshold = data['Value'].quantile(0.75)
print(value_threshold)
underpaid_threshold = 0.25
highly_valuable_underpaid = data['LongName'][(data['Value'] > value_threshold) & (data['Wage'] / data['Value'] < underpaid_threshold)]


# Scatter plot 
plt.figure(figsize=(25,15))
plt.scatter(data['Wage'], data['Value'], s=25)
plt.xlabel('Wage')
plt.ylabel('Value')
plt.title('Scatter Plot between Value and Wage')
plt.show()
