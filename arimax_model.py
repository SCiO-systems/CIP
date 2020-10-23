#!/usr/bin/env python
# coding: utf-8


import numpy as np
import pmdarima as pm
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
import pathlib
import time


path_to_folder = str(pathlib.Path().absolute())
countries = ['Uzbekistan', 'Kyrgyzstan', 'Kazakhstan', 'Iran', 'Turkmenistan', 'Tajikistan', 'Mongolia']

index = "ndvi" #"ndvi", "smi"
exog_var_1 = "prec"  
exog_var_2 = "temp"
rcp = "rcp45" #"rcp85"
save_index = "NDVI" #"NDVI", "Soil_Moisture"
path_to_data = path_to_folder + "/data/Timeseries_Data/"
n_periods = 81 


for country in countries:

    path_to_data_country = path_to_data + country + "/Final_CSVs/"
    path_to_save = path_to_data + country + "/" + save_index + "_predictions/"


    all_files = sorted(os.listdir(path_to_data_country))
    if ".ipynb_checkpoints" in all_files: all_files.remove(".ipynb_checkpoints")

    exogenous_files_1 = [x for x in all_files if exog_var_1 in x]
    exogenous_files_1 = sorted([x for x in exogenous_files_1 if rcp in x])

    exogenous_files_2 = [x for x in all_files if exog_var_2 in x]
    exogenous_files_2 = sorted([x for x in exogenous_files_2 if rcp in x])

    index_files = [x for x in all_files if index in x]
    index_files = sorted([x for x in index_files if rcp in x])



    for i in range(len(index_files)):     

        
        ind = pd.read_csv(path_to_data_country + index_files[i])
        prec = pd.read_csv(path_to_data_country + exogenous_files_1[i])
        temp = pd.read_csv(path_to_data_country + exogenous_files_2[i])

        starting_year = ind.iloc[0][0]
        starting_row = prec.loc[prec['Year'] == starting_year]
        starting_row_index = starting_row.index[0]
        
    
        
        new_prec = prec[starting_row_index:].reset_index(drop=True)
        new_temp = temp[starting_row_index:].reset_index(drop=True)

        train_series = ind["Value"]
        train = train_series.to_numpy()


        year_2020_index = new_prec.loc[new_prec['Year'] == 2018.0].index[0]

        
        exog_train_series_1 = new_prec[:year_2020_index + 1]
        exog_train_series_1 = exog_train_series_1["Value"]
        exog_train_1 = np.expand_dims(exog_train_series_1.to_numpy(),axis=1)
        exog_pred_series_1 = new_prec[year_2020_index + 1:]
        years = exog_pred_series_1["Year"].reset_index(drop=True)
        exog_pred_series_1 = exog_pred_series_1["Value"]
        exog_pred_1 = np.expand_dims(exog_pred_series_1.to_numpy(),axis=1)
        
        
        exog_train_series_2 = new_temp[:year_2020_index + 1]
        exog_train_series_2 = exog_train_series_2["tmax"]
        exog_train_2 = np.expand_dims(exog_train_series_2.to_numpy(),axis=1)        
        exog_pred_series_2 = new_temp[year_2020_index + 1:]
        exog_pred_series_2 = exog_pred_series_2["tmax"]
        exog_pred_2 = np.expand_dims(exog_pred_series_2.to_numpy(),axis=1)
   
    
        exog_train_series = pd.concat([exog_train_series_1,exog_train_series_2],axis=1)
        exog_train = exog_train_series.to_numpy()
        
        
        
        exog_pred_series = pd.concat([exog_pred_series_1,exog_pred_series_2],axis=1)
        exog_pred = exog_pred_series.to_numpy()

        #change parameters accordingly
        my_order = (0, 1, 2)
        smodel = pm.ARIMA(order=my_order)
        

        smodel_fit = smodel.fit(train,exogenous=exog_train)
        fitted = smodel.predict(n_periods=n_periods, exogenous=exog_pred) #
        fitted_series = pd.Series(fitted,name='Value')
        fitted_series = pd.concat([years,fitted_series],axis=1)
  
        final = pd.concat([ind,fitted_series],axis=0, ignore_index=True)
        plt.plot(final["Value"])
        plt.show()
        
        final.to_csv(path_to_save + index_files[i], index=False)



#experimenting with automodel ARIMAX
start = time.time()
smodel = pm.auto_arima(train,
                       exog_train,
                       start_p=0,
                       start_q=0,
                       test='adf',
                       max_p=3,
                       max_q=3,
                       d=None,
                       trace=True,
                       error_action='ignore',  
                       suppress_warnings=True, 
                       stepwise=True)
end = time.time()
smodel.summary()



#experimenting with manualmodel ARIMAX
my_order = (0, 2, 2)
smodel = pm.ARIMA(order=my_order)

start = time.time()
smodel_fit = smodel.fit(train,exogenous=exog_train)
end = time.time()


n_periods = 81 

start = time.time()
fitted, confint = smodel.predict(n_periods=n_periods, exogenous=exog_pred, return_conf_int=True) #
end = time.time()
print("Time elapsed for prediction: ",end - start)

print(type(fitted))

# Make as pandas series
fc_series = pd.Series(fitted, index=exog_pred_series.index-1) 
lower_series = pd.Series(confint[:, 0], index=exog_pred_series.index-1)
upper_series = pd.Series(confint[:, 1], index=exog_pred_series.index-1)

plt.figure(figsize=(30,10), dpi=100)
plt.plot(train, label='historical soil moisture index')
plt.plot(fc_series, label='predicted soil moisture index')
plt.title('Forecast vs Actuals')
plt.legend(loc='upper left', fontsize=15)
plt.show()


plt.figure(figsize=(30,10))
plt.plot(exog_pred_series)


plt.figure(figsize=(30,10), dpi=100)
plt.plot(fc_series, label='predicted soil moisture index')
plt.title('Forecast vs Actuals')
plt.legend(loc='upper left', fontsize=15)
plt.show()

