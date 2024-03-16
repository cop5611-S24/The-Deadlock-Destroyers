#! /usr/bin/python

import pandas as pd 


if __name__=='__main__':
    ##we are going to read the csv and get the average of each thingy
    df = pd.read_csv('result.csv')
    prevCharge = -1
    counter = 1
    charge_rate_list = []
    for index, row in df.iterrows():
        currCharge = row['currentCharge']
        if currCharge != prevCharge:
            if prevCharge !=-1:
                size = counter - 1 - len(charge_rate_list)
                chargeDrop = prevCharge - currCharge
                chargeDropRate = chargeDrop/size
                for i in range(size):
                    charge_rate_list.append(chargeDropRate)
                prevCharge = currCharge
                counter+=1
                continue
        counter +=1
        prevCharge = currCharge


    ##since application workload is the most important of the features we will get the mean of those that have an application workload of music
        
    
          
