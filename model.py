#! /usr/bin/python
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns 
from math import sqrt
import xgboost as xgb 
from math import sqrt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import BayesianRidge
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

np.random.seed(41)

def calc_normalized_RMSE(y_test, predicted):
    normalized_RMSE = sqrt(mean_squared_error(y_test, predicted))/ ((max(y_test)) - (min(y_test)))
    return normalized_RMSE

"""
def optimize_num_of_trees(X_train, X_test, y_train, y_test):
    min_RMSE = -1
    min_RMSE_num_trees = -1
    for i in range (1, 100, 1):  
        model = RandomForestRegressor(n_estimators = i)
        model.fit(X_train, y_train)
        predicted = model.predict(X_test)
        temp =calc_normalized_RMSE(y_test, predicted)
        if (min_RMSE == -1 or min_RMSE > temp):
            min_RMSE = temp
            min_RMSE_num_trees = i
    print_string = "The minimunum NRMSE for our optimized Random Forest Regressor with " + str(min_RMSE_num_trees) + " trees was "+ str(min_RMSE) +"."
    print(print_string)
"""

def random_forest_regressor(df, y):
    X = df 
    X_train, X_test,y_train, y_test = train_test_split(X.to_numpy(), y.to_numpy(), test_size = 0.33, random_state=42)
    #sklearn https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
    model = RandomForestRegressor(n_estimators = 30)
    model.fit(X_train, y_train)
    predicted = model.predict(X_test)
    normalized_RMSE = calc_normalized_RMSE(y_test, predicted)
    print(normalized_RMSE)
    MAE =  mean_absolute_error(y_test, predicted)/((max(y_test)) - (min(y_test)))
    print(f"MAE: {MAE}")
    MSE = mean_squared_error(y_test, predicted)/((max(y_test)) - (min(y_test)))
    print(f"MSE: {MSE}")
    #r2 = r2_score(y_test, predicted)
   # print(f"R^2 Score: {r2}")
    

def bayesian_regressor(df, y):
    X = df 
    #sklearn https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
    X_train, X_test,y_train, y_test = train_test_split(X.to_numpy(), y.to_numpy(), test_size = 0.33, random_state=42)
    model = BayesianRidge(fit_intercept=False)    
    model.fit(X_train, y_train)
    predicted = model.predict(X_test)
    temp = calc_normalized_RMSE(y_test, predicted)
    MAE = mean_absolute_error(y_test, predicted)
    print(f"MAE: {MAE}")
    MSE = mean_squared_error(y_test, predicted) 
    print(f"MSE: {MSE}")    
    #Our R^2 was very bad but this is do to our data problem of having too few observations
    print("This is NMRSE for the Bayesian regressor")
    print(temp)


def linear_regressor(df, y):
    df.drop(columns=['timestamp','currentCharge'],inplace=True)
    X = df
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print(y_train)
    mse = mean_squared_error(y_test, y_pred)
    print("Mean Squared Error:", mse)

    # Print coefficients
    print("Intercept:", model.intercept_)
    print("Coefficient:", model.coef_)


if __name__ == "__main__":
    df = pd.read_csv("cleaned_result.csv")
    y = df['discharge_rate']
    df.drop(columns = ['discharge_rate'], inplace=True)
    random_forest_regressor(df, y)
    bayesian_regressor(df, y)
    linear_regressor(df,y)
