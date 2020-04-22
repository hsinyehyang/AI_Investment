# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 11:04:58 2020

@author: nhri
"""

import pandas as pd;
import numpy as np;
import matplotlib.dates as mpl_dates;
import os;
import matplotlib.pyplot as plt;
import mpl_finance as mpf

#arguments
input_file = "C:/Users/nhri/Desktop/KLine/TW_STOCK_0050.csv";
output_file = "C:/Users/nhri/Desktop/KLine/result/";
day = 20;  #default
pixel_width = 224;  #default
pixel_height = 224;  #default
begin = None; #string, ex: "1991-02-07"; default is the first date in your data
end = None; #string, ex: "1991-02-07"; default is the last date in your data
show_date = False;  #default
show_margin = False;  #default
grayscale = False;  #default
smooth = True;  #default

###########
#  begin  #
###########
data = pd.read_csv(input_file);

#############################################
#  drop the row that includes empty values  #
#############################################
tmp = np.where(pd.isnull(data));
data = data.drop(np.unique(tmp[0]), axis=0);

#####################
#  date: begin~end  #
#####################
data["Date2"]=pd.to_datetime(data["Date"]);

if begin is None:
    begin = data.iloc[0, 7];
else:
    begin = pd.to_datetime(begin);

if end is None:
    end = data.iloc[data.shape[0]-1, 7];
else:
    end = pd.to_datetime(end);

data = data.loc[ (data.iloc[:, 7]>=begin) & (data.iloc[:, 7]<=end), : ]

#####################
#  date: begin~end  #
#####################
if smooth==False:
    data["Date2"] = data["Date2"].apply(mpl_dates.date2num);
else:
    data["Date2"]=range(0, data.shape[0]);

#############################
#  output_file preparation  #
#############################
try:
    if not os.path.exists(output_file):
        os.makedirs(output_file)
except OSError:
    print ('Error: Creating directory. ' +  output_file)

##################
#  candlesticks  #
##################
name_stock = input_file.split("_");
name_stock = name_stock[len(name_stock)-1];
name_stock = name_stock.strip(".csv");

for i in range(0, data.shape[0]-day+1):
    main_plot=name_stock+", "+"".join(data.iloc[i:(i+day), :]["Date"].iloc[0].split("-"))+"-"+"".join(data.iloc[i:(i+day), :]["Date"].iloc[day-1].split("-"))
    output_name = name_stock+"-"+"".join(data.iloc[i:(i+day), :]["Date"].iloc[day-1].split("-"));
    fig, ax = plt.subplots(figsize=(pixel_width/96, pixel_height/96), dpi=96)
    
    if show_date==True and show_margin == True:
        plt.subplots_adjust(top = 0.99, bottom = 0.08*pixel_width/pixel_height, right = 0.98, left = 0.01) #show_date = True; show_margin = True;
        plt.xticks([])
        plt.yticks([])
        plt.xlabel(main_plot, labelpad=3, color="grey", fontsize=10*pixel_width/224)
    elif show_date==True and show_margin == False:
        plt.subplots_adjust(top = 1, bottom = 0.1*pixel_width/pixel_height, right = 1, left = 0) #show_date = True; show_margin = False;
        plt.xticks([])
        plt.yticks([])
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        plt.xlabel(main_plot, labelpad=3, color="grey", fontsize=10*pixel_width/224)
    elif show_date==False and show_margin == True:
        plt.subplots_adjust(top = 1, bottom = 0.01, right = 0.99, left = 0) #show_date = False; show_margin = True;
        plt.xticks([])
        plt.yticks([])
    else:
        plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0); #show_date = False; show_margin = False;
        plt.axis('off')

    if grayscale==False:
        mpf.candlestick_ohlc(ax, data.iloc[i:(i+day), [7, 1, 2, 3, 4]].values, width=0.6, colorup='red', colordown='green', alpha=0.8)
    else:
        mpf.candlestick_ohlc(ax, data.iloc[i:(i+day), [7, 1, 2, 3, 4]].values, width=0.6, colorup='black', colordown='black', alpha=0.8)

    #save the picture
    plt.savefig(output_file+output_name+".png", dpi=96);
    plt.close(fig)