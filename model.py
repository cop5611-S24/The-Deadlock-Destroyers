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
    df.plot(y='currentCharge', title='Battery Charge over Time')
    plt.savefig('plots/charge_v_time/battery_charge.png')
    df1 = df.loc['2024-03-04']
    df2 = df.loc['2024-03-11']
    df1.plot(y='currentCharge', title='Battery Charge over Time')
    plt.savefig('plots/charge_v_time/battery_charge_march4.png')
    df2.plot(y='currentCharge', title='Battery Charge over Time')
    plt.savefig('plots/charge_v_time/battery_charge_march11.png')