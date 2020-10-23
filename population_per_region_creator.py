#!/usr/bin/env python
# coding: utf-8


import numpy as np
import os
import sys
import pathlib
import matplotlib.pyplot as plt
import csv 
import pandas as pd



# OFFICIAL DATA AS OF 2020
kaz_total_pop = 18632.169
kaz_code_dict = {
    "KZ-AKM" : (736.682 + 1136.008)/kaz_total_pop, #"Aqmola",  #
    "KZ-AKT" : 881.728/kaz_total_pop, #"Aqtöbe",  #
    "KZ-ALM" : (2055.651 + 1916.782)/kaz_total_pop, #"Almaty",  #
    "KZ-ATY" : 645.371/kaz_total_pop, #"Atyrau",  #
    "KZ-KAR" : 1376.827/kaz_total_pop, #"Qaraghandy",  #
    "KZ-KUS" : 868.524/kaz_total_pop, #"Qostanay",  #
    "KZ-KZY" : 803.545/kaz_total_pop, #"Qyzylorda",  #
    "KZ-MAN" : 698.919/kaz_total_pop, #"Mangghystau",  #
    "KZ-PAV" : 752.252/kaz_total_pop, #"Pavlodar",  #
    "KZ-SEV" : 548.751/kaz_total_pop, #"North Kazakhstan", #Soltüstik Qazaqstan
    "KZ-VOS" : 1369.635/kaz_total_pop, #"East Kazakhstan", # Shyghys Qazaqstan
    "KZ-YUZ" : (1036.144 + 2018.100)/kaz_total_pop, #"South Kazakhstan", # Ongtüstik Qazaqstan
    "KZ-ZAP" : 656.974/kaz_total_pop, #"West Kazakhstan",  #Batys Qazaqstan
    "KZ-ZHA" : 1130.276/kaz_total_pop, #"Zhambyl" #
#     "Kazakhstan_Kazakhstan" : "KZ"#

}
# print(kaz_code_dict)


turk_total_pop = 6550.000
turk_code_dict = {
    "TM-A" : 939.700/turk_total_pop, #"Ahal",#
    "TM-B" : 553.500/turk_total_pop, #"Balkan",#
    "TM-D" : 1370.400/turk_total_pop, #"Tashauz", #
    "TM-L" : 1334.500/turk_total_pop, #"Chardzhou", #
    "TM-M" : 1480.400/turk_total_pop, #"Mary", #
    "TM-S" : 871.500/turk_total_pop, #"Aşgabat"#
#     "Turkmenistan_Turkmenistan" : "TM"#
}
# print(turk_code_dict)


taj_total_pop = 9313.800
taj_code_dict = {
    "TJ-DU" : 863.400/taj_total_pop,#"Dushanbe",#
    "TJ-GB" : 228.900/taj_total_pop,#"Gorno-Badakhshan",#
    "TJ-KT" : 3348.300/taj_total_pop,#"Khatlon",#
    "TJ-RA" : 2165.900/taj_total_pop,#"Tadzhikistan Territories", #
    "TJ-SU" : 2707.300/taj_total_pop,#"Leninabad" #
#     "Tajikistan_Tajikistan" : "TJ"#
}
# print(taj_code_dict)

mon_total_pop = 3186.347
mon_code_dict = {
    "MN-035" : 103.217/mon_total_pop,#"Orhon",#
    "MN-037" : 104.238/mon_total_pop,#"Darhan-Uul",#
    "MN-039" : 77.664/mon_total_pop,#"Hentiy",#
    "MN-041" : 134.371/mon_total_pop,#"Hövsgöl",#
    "MN-043" : 88.447/mon_total_pop,#"Hovd",#
    "MN-046" : 83.617/mon_total_pop,#"Uvs",#
    "MN-047" : 95.045/mon_total_pop,#"Töv",#
    "MN-049" : 109.255/mon_total_pop,#"Selenge",#
    "MN-051" : 62.611/mon_total_pop,#"Sühbaatar",#
    "MN-053" : 69.124/mon_total_pop,#"Ömnögovi",#
    "MN-055" : 116.645/mon_total_pop,#"Övörhangay",#
    "MN-057" : 73.088/mon_total_pop,#"Dzavhan",#
    "MN-059" : 46.820/mon_total_pop,#"Dundgovi",#
    "MN-061" : 82.295/mon_total_pop,#"Dornod",#
    "MN-063" : 69.560/mon_total_pop,#"Dornogovi",#
    "MN-064" : 17.489/mon_total_pop,#"Govisümber",#
    "MN-065" : 58.280/mon_total_pop,#"Govi-Altay",#
    "MN-067" : 61.794/mon_total_pop,#"Bulgan", #
    "MN-069" : 88.359/mon_total_pop,#"Bayanhongor", #
    "MN-071" : 103.675/mon_total_pop,#"Bayan-Ölgiy",#
    "MN-073" : 95.994/mon_total_pop,#"Arhangay", #
    "MN-1" : 1444.669/mon_total_pop,#"Ulaanbaatar"
#     "Mongolia_Mongolia" : "MN"#
}
# print(mon_code_dict)

uzb_total_pop = 33905.242
uzb_code_dict = {
    "UZ-AN" : 3127.683/uzb_total_pop,#"Andijon",#
    "UZ-BU" : 1923.934/uzb_total_pop,#"Bukhoro",#
    "UZ-FA" : 3752.034/uzb_total_pop,#"Ferghana",#
    "UZ-JI" : 1382.060/uzb_total_pop,#"Jizzakh",#
    "UZ-NG" : 2810.843/uzb_total_pop,#"Namangan",#
    "UZ-NW" : 997.100/uzb_total_pop,#"Navoi",#
    "UZ-QA" : 3280.418/uzb_total_pop,#"Kashkadarya",#
    "UZ-QR" : 1898.351/uzb_total_pop,#"Karakalpakstan", #
    "UZ-SA" : 3877.355/uzb_total_pop,#"Samarkand", #
    "UZ-SI" : 846.260/uzb_total_pop,#"Sirdaryo",#
    "UZ-SU" : 2629.135/uzb_total_pop,#"Surkhandarya",#
    "UZ-TO" : 2941.908/uzb_total_pop,#"Tashkent", #
    "UZ-TK" : 2571.668/uzb_total_pop,#"Tashkent City",#
    "UZ-XO" : 1866.493/uzb_total_pop,#"Khorezm" #
#     "Uzbekistan_Uzbekistan" : "UZ"#
}
# print(uzb_code_dict)

krg_total_pop = 6523.529
krg_code_dict = {
    "KG-B"  : 537.365/krg_total_pop,#"Batken",#
    "KG-C"  : 959.884/krg_total_pop,#"Chüy",#
    "KG-GB" : 1053.915/krg_total_pop,#"Biškek", #
    "KG-J"  : 1238.750/krg_total_pop,#"Jalal-Abad",#
    "KG-N"  : 289.621/krg_total_pop,#"Naryn",#
    "KG-O"  : 1368.054/krg_total_pop,#"Osh",#
    "KG-GO" : 312.530/krg_total_pop,#"Osh (city)",#
    "KG-T"  : 267.360/krg_total_pop,#"Talas",#
    "KG-Y"  : 496.050/krg_total_pop,#"Ysyk-Köl"#
#     "Kyrgyzstan_Kyrgyzstan" : "KG",#
}
# print(krg_code_dict)

irn_total_pop = 83075.000
irn_code_dict = {
    "IR-01" : 4018.000/irn_total_pop,#"East Azarbaijan",#
    "IR-02" : 3398.000/irn_total_pop,#"West Azarbaijan",#
    "IR-03" : 1297.000/irn_total_pop,#"Ardebil",#
    "IR-04" : 5292.000/irn_total_pop,#"Esfahan",#
    "IR-05" : 597.000/irn_total_pop,#"Ilam",#
    "IR-06" : 1230.000/irn_total_pop,#"Bushehr",#
    "IR-07" : 13807.000/irn_total_pop,#"Tehran",#
    "IR-08" : 979.000/irn_total_pop,#"Chahar Mahall and Bakhtiari",#
    "IR-10" : 4885.000/irn_total_pop,#"Khuzestan",#
    "IR-11" : 1095.000/irn_total_pop,#"Zanjan",#
    "IR-12" : 750.000/irn_total_pop,#"Semnan",#
    "IR-13" : 2978.000/irn_total_pop,#"Sistan and Baluchestan",#
    "IR-14" : 5006.000/irn_total_pop,#"Fars",#
    "IR-15" : 3299.000/irn_total_pop,#"Kerman",#
    "IR-16" : 1658.000/irn_total_pop,#"Kordestan",#
    "IR-17" : 1989.000/irn_total_pop,#"Kermanshah",#
    "IR-18" : 744.000/irn_total_pop,#"Kohgiluyeh and Buyer Ahmad",#
    "IR-19" : 2562.000/irn_total_pop,#"Gilan",#
    "IR-20" : 1793.000/irn_total_pop,#"Lorestan",#
    "IR-21" : 3365.000/irn_total_pop,#"Mazandaran",#
    "IR-22" : 1467.000/irn_total_pop,#"Markazi",#
    "IR-23" : 1902.000/irn_total_pop,#"Hormozgan",#
    "IR-24" : 1771.000/irn_total_pop,#"Hamadan",#
    "IR-25" : 1213.000/irn_total_pop,#"Yazd",#
    "IR-26" : 1373.000/irn_total_pop,#"Qom",#
    "IR-27" : 1951.000/irn_total_pop,#"Golestan",#
    "IR-28" : 1322.000/irn_total_pop,#"Qazvin",#
    "IR-29" : 809.000/irn_total_pop,#"South Khorasan", #
    "IR-30" : 6768.000/irn_total_pop,#"Razavi Khorasan",#
    "IR-31" : 892.000/irn_total_pop,#"North Khorasan", #
    "IR-32" : 2865.000/irn_total_pop,#"Alborz"#
#     "Iran_Iran" : "IR",#
}
# print(irn_code_dict)

dicts_list = [irn_code_dict, krg_code_dict, kaz_code_dict, mon_code_dict, taj_code_dict, turk_code_dict, uzb_code_dict]
# print(dicts_list)




path_to_folder = str(pathlib.Path().absolute())
print(path_to_folder)
path_to_data = path_to_folder + "/data/Populations/data/"

path_to_results = path_to_folder + "/data/Populations/results/"
# print(path_to_timeseries)
# countries = os.listdir(path_to_timeseries)
# if ".ipynb_checkpoints" in countries: countries.remove(".ipynb_checkpoints")
countries = sorted(['Uzbekistan', 'Kyrgyzstan', 'Kazakhstan', 'Iran', 'Turkmenistan', 'Tajikistan', 'Mongolia'])
print(countries)
csvs = sorted(os.listdir(path_to_data))
if ".ipynb_checkpoints" in csvs: csvs.remove(".ipynb_checkpoints")

print(csvs)
print(os.listdir(path_to_results))



for i in range(len(csvs)//2):
    pops = path_to_data + csvs[2*i]
    age_groups = path_to_data + csvs[2*i +1]
    dict_to_use = dicts_list[i]
    print(pops)
    pops_df = pd.read_csv(pops)
    age_groups_df = pd.read_csv(age_groups)
    print(csvs[2*i])
    print(csvs[2*i +1])
#     print(dict_to_use)
#     print()
#     print()
    for region in dict_to_use.keys():
        factor = dict_to_use[region]

        local_pop_df = pops_df.copy()
        local_pop_df.iloc[:,-3:] = local_pop_df.iloc[:,-3:] * factor
        print(local_pop_df)
        local_age_groups_df = age_groups_df.copy()
        local_age_groups_df.iloc[:,-3:] = local_age_groups_df.iloc[:,-3:] * factor
        print(local_age_groups_df)

        print(csvs[2*i].replace(csvs[2*i][:2], region))
        print(csvs[2*i +1].replace(csvs[2*i+1][:2], region))

        local_pop_df.to_csv(path_to_results + csvs[2*i].replace(csvs[2*i][:2], region),index=False)
        local_age_groups_df.to_csv(path_to_results + csvs[2*i+1].replace(csvs[2*i+1][:2], region),index=False)
    
   