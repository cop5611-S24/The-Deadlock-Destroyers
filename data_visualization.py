#! /usr/bin/python
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns 
from sklearn.preprocessing import MinMaxScaler

import xgboost as xgb 

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder

color = sns.color_palette()


def gen_box_plots (df_filtered, feature):
    sns.set_style("whitegrid")
    sns.boxplot(x= 'brightness', y = 'discharge_rate', data= df_filtered)
    plt.savefig('boxplot.png')





if __name__=='__main__':

    # https://saturncloud.io/blog/how-to-detect-and-exclude-outliers-in-a-pandas-dataframe/
    df = pd.read_csv('cleaned_result.csv')
    first_quartile = df['discharge_rate'].quantile(0.25)
    third_quartile = df['discharge_rate'].quantile(0.75)
    inter_quartile_range = third_quartile - first_quartile
    lower_whisker = first_quartile - 1.5 * inter_quartile_range
    upper_whisker = third_quartile + 1.5 * inter_quartile_range
    outliers = df[(df['discharge_rate'] < lower_whisker) | (df['discharge_rate']> upper_whisker)]
    df_filtered = df.drop(outliers.index)
    #I will make 5 plots then call it a day 
    #So we will have boxplots for each feature 
