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
df['Salary'] = df['Salary Estimate'].str.split('(').str[0]

df['Salary'] = df['Salary'].str.replace('$','')
df['Salary'] = df['Salary'].str.replace('K','')
df['Salary'] = df['Salary'].str.replace('Employer Provided Salary:','')

df['hourly'] = df['Salary'].str.contains('Per Hour',regex=False).astype(int)
df['Salary'] = df['Salary'].str.replace('Per Hour','')

df['Salary'] = df['Salary'].str.split('-')

df['Minimum Salary'] = df['Salary'].str[0].astype(int)
df['Maximum Salary'] = df['Salary'].str[1].astype(int)

df['Average Salary'] = (df['Minimum Salary']+df['Maximum Salary'])/2


#convert hourly wage to annual salary by nultiplying by 2000(yearly work hours)/1000(salary in thousands)
df['Minimum Salary'] = df.apply(lambda x: x['Minimum Salary']*2 if x.hourly == 1 else x['Minimum Salary'], axis=1)
df['Maximum Salary'] = df.apply(lambda x: x['Maximum Salary']*2 if x.hourly == 1 else x['Maximum Salary'], axis=1)

df = df.drop(['Salary'],axis=1)


#Getting Company Name and rating from Company name column
df['Company'] = df.apply(lambda x: x['Company Name'] if x['Rating']<0 else x['Company Name'][:-3], axis=1)
# removing \r\n from Company
df['Company'] = df['Company'].str.replace('\r\n','')

#getting state and city from location
df['State'] = df['Location'].str.split(',').str[1]
df['City'] = df['Location'].str.split(',').str[0]

#removing los angles from state and replacing with ca
df['State'] = df['State'].apply(lambda x: 'CA' if x.strip() == 'Los Angeles' else x.strip())


#Check if location and Headquarters are same
df['isheadquarters'] = df.apply(lambda x: 1 if x.Location == x.Headquarters else 0, axis=1)


#Company age
df['Company Age'] = df.apply(lambda x: 2021-x.Founded if x.Founded>0 else x.Founded, axis=1)


# Extracting required skills from JD
df['python_r'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
df['tableau_r'] = df['Job Description'].apply(lambda x: 1 if 'tableau' in x.lower() else 0)
df['excel_r'] = df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)
df['sql'] = df['Job Description'].apply(lambda x: 1 if 'sql' in x.lower() else 0)


#modifying the Job titlle to catagorise the jobs to simpler ones
def title_simplifier(title):
    if 'data scientist' in title.lower():
        return 'Data Scientist'
    elif 'analyst' in title.lower():
        return 'Analyst'
    elif 'machine learning' in title.lower():
        return 'Machine Learning Engineer'
    elif 'data engineer' in title.lower():
        return 'Data Engineer'
    elif 'research scientist' in title.lower():
        return 'Research Scientist'
    elif 'manager' in title.lower():
        return 'Manager'
    elif 'director' in title.lower():
        return 'Director'
    else :
        return 'na'

#divide the roles based on seniority
def seniority(title):
    if 'senior' in title.lower() or 'sr' in title.lower() or 'lead' in title.lower() or 'principal' in title.lower():
        return 'Senior'
    elif 'junior' in title.lower() or 'jr' in title.lower() or 'associate' in title.lower():
        return 'Junior'
    else:
        return 'na'

df['Job_cat'] = df['Job Title'].apply(title_simplifier)
df['Seniority'] = df['Job Title'].apply(seniority)

#Length if Job Description
df['dcrpn_len'] = df['Job Description'].apply(lambda x: len(x))


#create a new csv to store the cleaned data
df.to_csv('cleaned_salary_data.csv',index=False)



