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


def random_forest_regressor():
    df = pd.read_csv("cleaned_result.csv")
    y = df['discharge_rate']
    df.drop(columns = ['discharge_rate'], inplace=True)
    X = df 
    np.random.seed(41)
    #sklearn https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
    X_train, X_test,y_train, y_test = train_test_split(X.to_numpy(), y.to_numpy(), test_size = 0.33, random_state=42)
    model = RandomForestRegressor()
    model.fit(X_train, y_train)
    predicted = model.predict(X_test)
    normalized_RMSE = sqrt(mean_squared_error(y_test, predicted))/ ((max(y_test)) - (min(y_test)))
    print(normalized_RMSE)
    

def bayesian_regressor():
    pass

def support_vector_regressor():
    pass

def linear_regressor():
    pass


if __name__ == "__main__":
    random_forest_regressor()