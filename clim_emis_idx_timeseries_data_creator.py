#!/usr/bin/env python
# coding: utf-8


import rasterio
from rasterio.mask import mask
import numpy as np
import os
import sys
import pathlib
import geojson
import matplotlib.pyplot as plt
import csv 
import boto3
from osgeo import gdal

from rasterio import plot
import matplotlib.pyplot as plt
from rasterstats import zonal_stats
import time
import datetime



path_to_folder = str(pathlib.Path().absolute())
path_to_data = path_to_folder + "/data/"
print(path_to_folder)
print(path_to_data)

path_to_hist_aggr_data = path_to_data + "Historical_Aggregate_Data/"
path_to_cmip6_data = path_to_data + "NEX_GDDP_Data/"
path_to_timeseries_data = path_to_data + "Timeseries_Data/"
path_to_emissions_data = path_to_data + "Emission_Predictions_Decadal_Data/"
path_to_polygons = path_to_folder + "/polygons/"
    
path_to_reference_tif = "/home/ds/Desktop/ml_projects/CMIP6_AGGREGATES_ssp126_2021_2040.tif"
reference_tif = gdal.Open(path_to_reference_tif)
gt = reference_tif.GetGeoTransform()
wkt_projection = reference_tif.GetProjectionRef()
geo_info = [gt,wkt_projection]
ref_width = reference_tif.RasterYSize
ref_height = reference_tif.RasterXSize

#############################################################


# Historical Soil Moisture Data
def historical_index_timeseries_creator(path_to_hist_index_data, path_to_save_folder, index_name, country, region, polygon):
    csv_file_name = path_to_save_folder + "/" + index_name + "_historical/Historical_" + index_name + "_Timeseries_" + country + "_" + region + ".csv"
    if os.path.isfile(csv_file_name):
        print("File at path: ", csv_file_name, " exists already")
        return
    files_list = sorted(os.listdir(path_to_hist_index_data))
    time_series = {"Year": [], "Value": []}

    for file in files_list[:-1]: 
        date = file[-8:-4]
        temp = zonal_stats(polygon, path_to_hist_index_data + file, stats="mean")
        time_series["Year"].append(date)
        time_series["Value"].append(temp[0]["mean"])


    zd = zip(*time_series.values())
    with open(csv_file_name, 'w') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(time_series.keys())
        writer.writerows(zd)

    return



# Historical Prec Data
def historical_exog_var_timeseries_creator(path_to_hist_aggr_data, path_to_save_folder, exogenous_variable, country, region, polygon):
    csv_file_name = path_to_save_folder + "/" + exogenous_variable + "_historical/Historical_" + exogenous_variable + "_Timeseries_" + country + "_" + region + ".csv"        

    if os.path.isfile(csv_file_name):
        print("File at path: ", csv_file_name, " exists already")
        return
    
    files_list = sorted(os.listdir(path_to_hist_aggr_data))
    files_list = [x for x in files_list if exogenous_variable in x]
    
    time_series = {"Year": [], "Value": []}


    for file in files_list:

        temp = zonal_stats(polygon, path_to_hist_aggr_data + file, stats="mean")
        time_series["Value"].append(temp[0]["mean"])

    starting_year = 1961
    years = list(range(starting_year, starting_year + len(files_list)))
    for year in years:
        date = str(year)
        time_series["Year"].append(date)



    zd = zip(*time_series.values())
    with open(csv_file_name, 'w') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(time_series.keys())
        writer.writerows(zd)

    return


# In[2]:


def save_arrays_to_tif(array_to_save):
    outRaster = "temp_tif.tif"
    driver = gdal.GetDriverByName("GTiff")
    if (len(array_to_save.shape)!=3):
        array_to_save = np.expand_dims(array_to_save,axis=0)
    no_bands, width, height = array_to_save.shape

    DataSet = driver.Create(outRaster, height, width, no_bands, gdal.GDT_Float32)
    geo_trans = (-180.0, 360.0/height,0.0,90.0,0.0, -180.0/width)
    DataSet.SetGeoTransform(geo_trans)
    DataSet.SetProjection(geo_info[1])
#     print(geo_trans)
#     print(geo_info[1])


#     array_to_save = np.expand_dims(array_to_save, axis=0)
    for i, image in enumerate(array_to_save, 1):
        DataSet.GetRasterBand(i).WriteArray(image)
    DataSet = None
#     print("Temporary tif: ", outRaster, " has been saved")
    return


# In[64]:


# CMIP6 Prec Data
def cmip_exog_var_timeseries_creator(path_to_cmip6_data, path_to_save_folder, exogenous_variable, country, region, polygon, rcp):
    csv_file_name = path_to_save_folder + "/" + exogenous_variable + "_predictions/NEX_GDDP_yearly_" + rcp + "_" + exogenous_variable + "_Timeseries_" + country + "_" + region + ".csv"        
    if os.path.isfile(csv_file_name):
        print("File at path: ", csv_file_name, " exists already")
        return
    
    
    files_list = sorted(os.listdir(path_to_cmip6_data))
    years_to_predict = 81

    files_list = [x for x in files_list if rcp in x ]
    files_list = [x for x in files_list if exogenous_variable in x ]

    time_series = {"Year": [], "Value": []}



    for file in files_list:
        temp = zonal_stats(polygon, path_to_cmip6_data + file, stats="mean")
        if exogenous_variable == "prec":
            time_series["Value"].append(temp[0]["mean"] * 31556926/10)
        else: 
            time_series["Value"].append(temp[0]["mean"]-273)


    starting_year = 2019
    years = list(range(starting_year, starting_year + years_to_predict))
    for year in years:
        date = str(year)
        time_series["Year"].append(date)


    zd = zip(*time_series.values())
    with open(csv_file_name, 'w') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(time_series.keys())
        writer.writerows(zd)

    return


# In[27]:


# Emissions Data

def emissions_timeseries_creator(path_to_emissions_data, path_to_save_folder, country, region, polygon):
    path_to_save_folder = path_to_save_folder + "/Emissions/"
    SSPs = ["SSP2","SSP5"]
    gases = ["CH4","COE", "NH3", "NOX", "VOC"]
    emissions_names = ["agri", "buil", "burn", "ener", "indu", "solv", "ship", "tran", "wast"]    

    files_list = os.listdir(path_to_emissions_data)
    print(len(files_list))
    time_series = {"Year": [], "Value": []}

    date = "2005"     
    time_series["Year"].append(date)


    starting_year = 2010
    final_year = 2100
    years = list(range(starting_year, final_year + 1,10))
    for year in years:
        date = str(year)
        time_series["Year"].append(date)


    geojson_region = obj["hits"]["hits"][0]["_source"]    
    lis = []
    for ssp in SSPs:
        for gas in gases:
            for emis in emissions_names:
                time_series["Value"] = []
                for i in range(1,12):
                    read_file = "Emissions_" + ssp + "_" + gas + "_" + emis + ".tif"

                    temp = zonal_stats(polygon, path_to_emissions_data + read_file, stats="mean",band_num=i)
                    time_series["Value"].append(temp[0]["mean"])

                    zd = zip(*time_series.values())
                csv_file_name = path_to_save_folder + "Emissions_Timeseries_"  + ssp + "_" + gas + "_" + emis + "_"  + country + "_" + region + ".csv" 
                with open(csv_file_name, 'w') as file:
                    writer = csv.writer(file, delimiter=',')
                    writer.writerow(time_series.keys())
                    writer.writerows(zd)
    return




#############################################################

rcp = "rcp45" #"rcp85"
index_name = "NDVI" #"Soil_Moisture"

path_to_hist_index_data = path_to_data + "Historical_" + index_name + "_Yearly_Data/"


exogenous_variable = "tasmin"  #"tasmax"
countries = ["Kazakhstan", "Iran", "Kyrgyzstan", "Mongolia", "Tajikistan", "Turkmenistan","Uzbekistan"] #
adm_level = ["0", "1"]

for country in countries:
    print("Country: ", country)
    for level in adm_level:
        datastring = path_to_polygons + "JSON_" + country + "_adm_lvl_" + level + ".txt"
        with open(datastring) as f:
            obj = geojson.load(f)
        for i in range(0,obj["hits"]["total"]):
            if level == "0":
                region_name = obj["hits"]["hits"][i]["_source"]["properties"]["NAME_0"]
            elif level == "1":
                region_name = obj["hits"]["hits"][i]["_source"]["properties"]["NAME_1"]         
            print(region_name)
            geojson_region = obj["hits"]["hits"][i]["_source"]
            if region_name == "Aqtöbe":
                test_polygon = geojson_region
            historical_index_timeseries_creator(path_to_hist_index_data, path_to_timeseries_data + country, index_name, country, region_name, geojson_region)
            historical_exog_var_timeseries_creator(path_to_hist_aggr_data, path_to_timeseries_data + country, exogenous_variable, country, region_name, geojson_region)
            cmip_exog_var_timeseries_creator(path_to_cmip6_data, path_to_timeseries_data + country, exogenous_variable, country, region_name, geojson_region, rcp)
            emissions_timeseries_creator(path_to_emissions_data, path_to_timeseries_data + country, country, region_name, geojson_region)
