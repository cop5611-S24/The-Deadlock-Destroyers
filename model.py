#! /usr/bin/python
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns 

import xgboost as xgb 

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder
color = sns.color_palette()
if __name__=='__main__':
    df = pd.read_csv('result.csv')
    df = df.set_index('timestamp')
    df.index = pd.to_datetime(df.index,unit='s')
    df.plot(style='.',title='Battery Charge over Time')
    ##we need to create three different plots one for march 4, one for march 5 an done for march 12
    
    plt.savefig('battery_charge.png')