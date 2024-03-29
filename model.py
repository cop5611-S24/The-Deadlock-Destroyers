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
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import BayesianRidge

np.random.seed(41)

def calc_normalized_RMSE(y_test, predicted):
    normalized_RMSE = sqrt(mean_squared_error(y_test, predicted))/ ((max(y_test)) - (min(y_test)))
    return normalized_RMSE


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

def random_forest_regressor(df, y):
    X = df 
    X_train, X_test,y_train, y_test = train_test_split(X.to_numpy(), y.to_numpy(), test_size = 0.33, random_state=42)
    optimize_num_of_trees(X_train, X_test, y_train, y_test)
    

def bayesian_regressor(df, y):
    X = df 
    #sklearn https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
    X_train, X_test,y_train, y_test = train_test_split(X.to_numpy(), y.to_numpy(), test_size = 0.33, random_state=42)
    model = BayesianRidge(fit_intercept=False)    
    model.fit(X_train, y_train)
    predicted = model.predict(X_test)
    temp = calc_normalized_RMSE(y_test, predicted)
    print("This is NMRSE for the Bayesian regressor")
    print(temp)

def support_vector_regressor(df, y):
    X = df


def linear_regressor(df, y):
    pass


if __name__ == "__main__":
    df = pd.read_csv("cleaned_result.csv")
    y = df['discharge_rate']
    df.drop(columns = ['discharge_rate'], inplace=True)
    random_forest_regressor(df, y)
    bayesian_regressor(df, y)