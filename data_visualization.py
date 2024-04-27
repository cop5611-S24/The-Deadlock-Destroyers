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
from sklearn.tree import DecisionTreeClassifier
color = sns.color_palette()


def gen_box_plot(df_filtered, feature):
    sns.set_style("whitegrid")
    sns.boxplot(x= feature, y = 'discharge_rate', data= df_filtered)
    name_to_save = 'plots/boxplot/'+feature + '_vs_discharge_rate.png'
    plt.savefig(name_to_save)
    plt.clf()


def gen_violin_plot(df_filtered, feature):
    sns.set_style("whitegrid")
    sns.violinplot(data=df_filtered, x=feature, y="discharge_rate")
    name_to_save = 'plots/violin/'+feature+'_vs_discharge_rate.png'
    plt.savefig(name_to_save)
    plt.clf()

def gen_scatter_plot(df, feature):
    sns.set_style("whitegrid")
    sns.swarmplot(data=df, x=feature, y="discharge_rate")
    name_to_save = 'plots/scatterplots/'+feature+'_vs_discharge_rate.png'
    plt.savefig(name_to_save)
    plt.clf()

if __name__=='__main__':
    df = pd.read_csv('cleaned_result.csv')
    first_quartile = df['discharge_rate'].quantile(0.25)
    third_quartile = df['discharge_rate'].quantile(0.75)
    inter_quartile_range = third_quartile - first_quartile
    lower_whisker = first_quartile - 1.5 * inter_quartile_range
    upper_whisker = third_quartile + 1.5 * inter_quartile_range
    outliers = df[(df['discharge_rate'] < lower_whisker) | (df['discharge_rate']> upper_whisker)]
    df_filtered = df.drop(outliers.index)
    gen_box_plot(df_filtered, 'brightness')
    gen_box_plot(df_filtered, 'gps')
    gen_box_plot(df_filtered, 'application_workload')
    gen_box_plot(df_filtered, 'power_saving')
    gen_box_plot(df_filtered, 'refresh_rate')
    gen_violin_plot(df_filtered, 'brightness')
    gen_violin_plot(df_filtered, 'gps')
    gen_violin_plot(df_filtered, 'application_workload')
    gen_violin_plot(df_filtered, 'power_saving')
    gen_violin_plot(df_filtered, 'refresh_rate')
    df_new = df_filtered.drop('timestamp', axis =1)
    df_new_new = df_new.rename(columns={'application_workload': 'workload', 'power_saving': 'powerSave', 'refresh_rate': 'refRate', 'discharge_rate': 'disRate'})
    plt.figure(figsize= (10, 8))
    sns.heatmap(df_new_new.corr(),annot=True )
    plt.savefig('plots/corr_matrix.png')
    plt.clf()


   

    