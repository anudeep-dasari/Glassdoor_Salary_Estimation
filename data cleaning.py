#importing required libraries
import pandas as pd

# reading data
df = pd.read_csv('glassdoor_jobs.csv')

# dropping columns not required
df.columns
df = df.drop(['Unnamed: 0','Competitors'], axis=1)

#removing rows with no salary
df = df[df['Salary Estimate'] != '-1']

#cleaning Salary column
df['Salary Estimate'] = df['Salary Estimate'].str.split('(').str[0]

df['Salary Estimate'] = df['Salary Estimate'].str.replace('$','')
df['Salary Estimate'] = df['Salary Estimate'].str.replace('K','')
df['Salary Estimate'] = df['Salary Estimate'].str.replace('Employer Provided Salary:','')

df['hourly'] = df['Salary Estimate'].str.contains('Per Hour',regex=False)
df['Salary Estimate'] = df['Salary Estimate'].str.replace('Per Hour','')

df['Salary Estimate'] = df['Salary Estimate'].str.split('-')

df['Minumum Salary'] = df['Salary Estimate'].str[0]
df['Maximum Salary'] = df['Salary Estimate'].str[1]



