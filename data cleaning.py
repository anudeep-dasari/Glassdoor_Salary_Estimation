#importing required libraries
import pandas as pd

# reading data
df = pd.read_csv('glassdoor_jobs.csv')

# dropping columns not required
df.columns
df = df.drop(['Unnamed: 0','Competitors'], axis=1)

#removing rows with no salary
df = df[df['Salary Estimate'] != '-1']
df = df.reset_index(drop=True)

#cleaning Salary column
df['Salary Estimate'] = df['Salary Estimate'].str.split('(').str[0]

df['Salary Estimate'] = df['Salary Estimate'].str.replace('$','')
df['Salary Estimate'] = df['Salary Estimate'].str.replace('K','')
df['Salary Estimate'] = df['Salary Estimate'].str.replace('Employer Provided Salary:','')

df['hourly'] = df['Salary Estimate'].str.contains('Per Hour',regex=False).astype(int)
df['Salary Estimate'] = df['Salary Estimate'].str.replace('Per Hour','')

df['Salary Estimate'] = df['Salary Estimate'].str.split('-')

df['Minimum Salary'] = df['Salary Estimate'].str[0].astype(int)
df['Maximum Salary'] = df['Salary Estimate'].str[1].astype(int)

df['Average Salary'] = (df['Minimum Salary']+df['Maximum Salary'])/2

#Getting Company Name and rating from Company name column
df['Company'] = df.apply(lambda x: x['Company Name'] if x['Rating']<0 else x['Company Name'][:-3], axis=1)

#getting state and city from location
df['State'] = df['Location'].str.split(',').str[1]
df['City'] = df['Location'].str.split(',').str[0]
#Check if location and Headquarters are same
df['isheadquarters'] = df.apply(lambda x: 1 if x.Location == x.Headquarters else 0, axis=1)

#Company age
df['Company Age'] = df.apply(lambda x: 2021-x.Founded if x.Founded>0 else x.Founded, axis=1)

