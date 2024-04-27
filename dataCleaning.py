#! /usr/bin/python

import pandas as pd 


if __name__=='__main__':
    ##we are going to read the csv and get the average of each thingy
    ##need to split the dataframes into days and then check 
    df = pd.read_csv('result.csv')
    df_first = df.head(175)
    df_second = df.iloc[175:, :]
    print(len(df_first))
    print(len(df_second))
    
    #I need to come up with algo for negatives later! NOW!!!!

    prevCharge = -1
    counter = 1
    charge_rate_list_df1 = []
    charge_rate_list_df2 = []
    list_of_bright60_indexes_df1 = []
    list_of_bright60_indexes_df2 = []
    #list_of_bright100_indexes_df1 = []
    #list_of_bright100_indexes_df2 = []
   # list_of_bright100_charge_rates = []
    list_of_bright60_charge_rates = []


    position = 0
    for index, row in df_first.iterrows():
        currCharge = row['currentCharge']
        if row['brightness'] == 60:
            list_of_bright60_indexes_df1.append(position)
        if currCharge != prevCharge:
            if prevCharge !=-1:
                size = counter - 1 - len(charge_rate_list_df1)
                chargeDrop = prevCharge - currCharge
                chargeDropRate = chargeDrop/size
                for i in range(size):
                    charge_rate_list_df1.append(chargeDropRate)
                prevCharge = currCharge
                counter+=1
                position+=1
                continue
        counter +=1
        position+=1
        prevCharge = currCharge

    position = 0
    counter =1
    prevCharge = -1
    for index, row in df_second.iterrows():
        currCharge = row['currentCharge']
        if row['brightness'] == 60:
            list_of_bright60_indexes_df2.append(position)
        if currCharge != prevCharge:
            if prevCharge !=-1:
                size = counter - 1 - len(charge_rate_list_df2)
                chargeDrop = prevCharge - currCharge
                chargeDropRate = chargeDrop/size
                for i in range(size):
                    charge_rate_list_df2.append(chargeDropRate)
                prevCharge = currCharge
                counter+=1
                position+=1
                continue
        counter +=1
        position+=1
        prevCharge = currCharge


    for i in range(len(charge_rate_list_df1)):
        if i in list_of_bright60_indexes_df1:
            list_of_bright60_charge_rates.append(charge_rate_list_df1[i])

    for i in range (len(charge_rate_list_df2)):
        if i in list_of_bright60_indexes_df2:
            list_of_bright60_charge_rates.append(charge_rate_list_df2[i])

    avg_bright60 = sum(list_of_bright60_charge_rates)/len(list_of_bright60_charge_rates)
    charge_rate_list_df1.append(avg_bright60)
    charge_rate_list_df1.append(avg_bright60)
    charge_rate_list_df2.append(avg_bright60)
    charge_rate_list_df2.append(avg_bright60)
    print(len(charge_rate_list_df1))
    print(len(charge_rate_list_df2))
    df['discharge_rate'] = charge_rate_list_df1 + charge_rate_list_df2
    #df.to_csv('cleaned_result.csv', index = False)

    for index, row in df.iterrows():
        if row['application_workload']  == 'none':
            df.at[index, 'application_workload'] = 0
        elif row['application_workload'] == 'game':
            df.at[index, 'application_workload'] =1
        elif row['application_workload'] == 'video720':
            df.at[index, 'application_workload'] = 2
        elif row['application_workload'] == 'video1080':
            df.at[index, 'application_workload'] = 3
        elif row['application_workload'] == 'browsing':
            df.at[index, 'application_workload'] = 4
        elif row['application_workload'] == 'music':
            df.at[index, 'application_workload'] = 5
    #we need to turn the string columns into numbers
    df.to_csv('newcleaned_result.csv', index = False)
          
