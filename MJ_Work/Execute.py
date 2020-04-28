# -*- coding: utf-8 -*-
#"""
#Created on Thu Dec 26 18:19:45 2019
#@author: lewis
#"""
import sys
path = 'C:/Users/lewis/Desktop/TW_STOCK/' # directory of .py
sys.path.append(path)

# create function to execute
def execute(stock_id, basic_type, file_path):
    # to break security
    import time
    import random
    time.sleep(random.randint(10,15))
    # to crawl
    import Class_GoodInfoCrawler as gc
    result = gc.goodinfo_crawler(stock_id, basic_type)
    #from GoodInfoCrawler import *
    #result = goodinfo_crawler(stock_id, basic_type)
    result.basic_decide()
    result.parser()
    result.output.to_csv(file_path + basic_type +'_' + stock_id + '.csv', encoding='utf_8_sig')

# read stock id
import pandas as pd
id_path = 'C:/Users/lewis/Desktop/TW_STOCK/'
id_names = [ id_path + name for name in ['All-Code-1_2019-12-07.csv','All-Code-2_2019-12-07.csv']  ]
flatten = lambda l: [item for sublist in l for item in sublist.Code] # l is list with dfs(column name = 'Code')
all_stock = pd.DataFrame(flatten([ pd.read_csv(path) for path in id_names ]))
basic_type = pd.DataFrame(['Asset','Cash','Performance'])
file_path = 'C:/Users/lewis/Desktop/TW_STOCK/basicside_2020/TW_STOCK_'
#fun('0050',Performance,file_path)
# starting
basic_type.apply(lambda y: all_stock.apply(lambda x: execute(x[0],y[0],file_path), axis=1), axis=1)
