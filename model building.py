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
from sklearn.metrics import mean_absolute_error
lr = LinearRegression()
lr.fit(X_train,y_train)
cross_val_score(lr, X_train, y_train, scoring='neg_mean_absolute_error')
lr_cvs = np.mean(cross_val_score(lr, X_train, y_train, scoring='neg_mean_absolute_error'))
y_pred_lr = lr.predict(X_test)
mean_absolute_error(y_test,y_pred_lr)

# Lasso Regression
from sklearn.linear_model import Lasso
lasso = Lasso()
cross_val_score(lasso,X_train, y_train, scoring='neg_mean_absolute_error')

from sklearn.linear_model import LassoCV
lassocv = LassoCV(alphas = np.arange(0.1,1,0.01))
lassocv.fit(X_train,y_train)
cross_val_score(lassocv,X_train, y_train, scoring='neg_mean_absolute_error')
ls_cvs = np.mean(cross_val_score(lassocv,X_train, y_train, scoring='neg_mean_absolute_error'))
y_pred_ls = lassocv.predict(X_test)
mean_absolute_error(y_test,y_pred_ls)

# Random forests
from sklearn.ensemble import RandomForestRegressor
rfr = RandomForestRegressor()
rfr.fit(X_train, y_train)
cross_val_score(rfr, X_train, y_train, scoring='neg_mean_absolute_error')
rfr_cvs = np.mean(cross_val_score(rfr, X_train, y_train, scoring='neg_mean_absolute_error'))
y_pred_rfr = rfr.predict(X_test)
mean_absolute_error(y_test,y_pred_rfr)

#GridsearchCV for Random forests
from sklearn.model_selection import GridSearchCV
param_grid = {
    'bootstrap': [True],
    'max_depth': [130,140,150],
    'n_estimators': [100,200,300]
}
gs = GridSearchCV(rfr,param_grid, scoring = 'neg_mean_absolute_error',cv=3)
gs.fit(X_train,y_train)
gs.best_score_
gs.best_estimator_
y_pred_gs = gs.predict(X_test)
mean_absolute_error(y_test,y_pred_gs)

# Comparing different predictions
print("MAE Linear Regression: "+str(mean_absolute_error(y_test,y_pred_lr)))
print("MAE Lasso Regression: "+str(mean_absolute_error(y_test,y_pred_ls)))
print("MAE Random forests: "+str(mean_absolute_error(y_test,y_pred_rfr)))
print("MAE Random forest GridSearch :"+str(mean_absolute_error(y_test,y_pred_gs)))














