#! /usr/bin/python

import pandas as pd 


if __name__=='__main__':
    ##we are going to read the csv and get the average of each thingy
    ##need to split the dataframes into days and then check 
    df = pd.read_csv('result.csv')
    prevCharge = -1
    counter = 1
    charge_rate_list = []
    list_of_music_indexes = []
    position = 0
    for index, row in df.iterrows():
        currCharge = row['currentCharge']
        if row['application_workload'] == 'music':
            list_of_music_indexes.append(position)
        if currCharge != prevCharge:
            if prevCharge !=-1:
                size = counter - 1 - len(charge_rate_list)
                chargeDrop = prevCharge - currCharge
                chargeDropRate = chargeDrop/size
                for i in range(size):
                    charge_rate_list.append(chargeDropRate)
                prevCharge = currCharge
                counter+=1
                position+=1
                continue
        counter +=1
        position+=1
        prevCharge = currCharge

    list_of_music_charge_rates =[]
    for i in range(len(charge_rate_list)):
       if i in list_of_music_indexes:
            list_of_music_charge_rates.append(charge_rate_list[i])
    
    avg_music = sum(list_of_music_charge_rates)/len(list_of_music_charge_rates)
    charge_rate_list.append(avg_music)
    charge_rate_list.append(avg_music)

    df['discharge_rate'] = charge_rate_list
    df.to_csv('cleaned_result.csv', index = False)
        
    
          
