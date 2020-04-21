# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 11:04:58 2020

@author: nhri
"""

import pandas as pd;
import numpy as np;
import matplotlib.dates as mpl_dates;
import matplotlib.pyplot as plt;
import mpl_finance as mpf

#arguments
input_file = "C:/Users/nhri/Desktop/KLine/TW_STOCK_0050.csv";
output_file = "C:/Users/nhri/Desktop/KLine/result/";
day = 20;  #default
pixel_width = 224;  #default
pixel_height = 224;  #default
show_date = True;  #default
show_margin = True;  #default
grayscale = False;  #default
smooth=False;  #default

###########
#  begin  #
###########
data = pd.read_csv(input_file);
#############################################
#  drop the row that includes empty values  #
#############################################
tmp = np.where(pd.isnull(data));
data = data.drop(np.unique(tmp[0]), axis=0);

if smooth==False:
    data["Date2"]=pd.to_datetime(data["Date"]);
    data["Date2"] = data["Date2"].apply(mpl_dates.date2num);
else:
    data["Date2"]=range(0, data.shape[0]);

##################
#  candlesticks  #
##################
for i in range(0, data.shape[0]-day+1):
    tmp_label="xx"+", "+"".join(data.iloc[i:(i+day), :]["Date"].iloc[0].split("-"))+"-"+"".join(data.iloc[i:(i+day), :]["Date"].iloc[day-1].split("-"))
    output_name = "".join(data.iloc[i:(i+day), :]["Date"].iloc[day-1].split("-"));
    fig, ax = plt.subplots(figsize=(pixel_width/96, pixel_height/96), dpi=96)

    if show_date==True and show_margin == True:
        plt.xticks([])
        plt.yticks([])
        plt.xlabel(tmp_label, labelpad=3, color="grey", fontsize=10*pixel_width/224)
    elif show_date==True and show_margin == False:
        plt.xticks([])
        plt.yticks([])
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        plt.xlabel(tmp_label, labelpad=3, color="grey", fontsize=10*pixel_width/224)
    elif show_date==False and show_margin == True:
        plt.xticks([])
        plt.yticks([])
    else:
        plt.axis('off')

    if grayscale==False:
        mpf.candlestick_ohlc(ax, data.iloc[i:(i+day), [7, 1, 2, 3, 4]].values, width=0.6, colorup='red', colordown='green', alpha=0.8)
    else:
        mpf.candlestick_ohlc(ax, data.iloc[i:(i+day), [7, 1, 2, 3, 4]].values, width=0.6, colorup='black', colordown='black', alpha=0.8)

    #save the picture
    plt.savefig(output_file+output_name+".png", dpi=96);
    plt.close(fig)