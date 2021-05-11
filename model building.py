#importing libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

#import data
df = pd.read_csv('cleaned_salary_data.csv')

#Selecting required columns for the model
df_mod = df[['Average Salary','Rating','Type of ownership', 'Industry', 'Sector', 'Revenue', 'hourly',
       'State','isheadquarters', 'Company Age', 'python_r','tableau_r', 'excel_r', 'sql_r', 'powerbi_r',
       'aws_r', 'spark_r','Job_cat', 'Seniority', 'dcrpn_len', 'Emp_no']]

# Get dummy variables
df_dum = pd.get_dummies(df_mod)

#Split the data into train and test
from sklearn.model_selection import train_test_split
X = df_dum.iloc[:,1:]
y = df_dum['Average Salary'].values
X_train,X_test,y_train,y_test = train_test_split(X, y, test_size=0.2, random_state=42 )

# Multiple Linear Regression
# Using stats models
import statsmodels.api as sm

X_sm = sm.add_constant(X)
sm_model = sm.OLS(y,X_sm)
sm_results = sm_model.fit()
sm_results.summary()

# Using Scikit-learn
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
lr = LinearRegression()
lr.fit(X_train,y_train)
cross_val_score(lr, X_train, y_train, scoring='neg_mean_absolute_error')
lr_cvs = np.mean(cross_val_score(lr, X_train, y_train, scoring='neg_mean_absolute_error'))

# Lasso Regression
from sklearn.linear_model import Lasso
lasso = Lasso()
cross_val_score(lasso,X_train, y_train, scoring='neg_mean_absolute_error')

from sklearn.linear_model import LassoCV
lassocv = LassoCV(alphas = np.arange(0.1,1,0.01))
cross_val_score(lassocv,X_train, y_train, scoring='neg_mean_absolute_error')
ls_cvs = np.mean(cross_val_score(lassocv,X_train, y_train, scoring='neg_mean_absolute_error'))

# Random forests
# 