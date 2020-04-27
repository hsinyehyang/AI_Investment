# -*- coding: utf-8 -*-
#"""
#Created on Tue Dec 24 16:45:26 2019
#@author: lewis
#"""
#--- define function for stock performance 
class goodinfo_crawler():
    
    def __init__(self, stock_id, basic_type):
        import pandas as pd
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'} 
        self.id = stock_id
        self.type = basic_type
        self.url = ''
        self.td = []
        self.output = pd.DataFrame()
        
    
    def basic_decide(self):
        if self.type == 'Performance':
            self.url = 'https://goodinfo.tw/StockInfo/StockBzPerformance.asp?STOCK_ID=' + self.id
            self.td = {'div_id':'divFinDetail', 'table_class':'solid_1_padding_4_0_tbl'}
        elif self.type == 'Asset':
            self.url = 'https://goodinfo.tw/StockInfo/StockAssetsStatus.asp?STOCK_ID=' + self.id
            self.td = {'div_id':'divDetail', 'table_class':'solid_1_padding_4_0_tbl'}
        else:
            self.url = 'https://goodinfo.tw/StockInfo/StockCashFlow.asp?STOCK_ID=' + self.id
            self.td = {'div_id':'divDetail', 'table_class':'solid_1_padding_4_1_tbl'}
        
    def parser(self):
        import requests
        from bs4 import BeautifulSoup
        import pandas as pd
        #-- make soup
        r = requests.get(self.url, headers =self.headers)
        r.encoding ='utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')
        #-- check if table data exist
        if soup.find(name = 'div', attrs = {'id':self.td['div_id']}) is not None:
            #-- read table data to dfs
            rows = soup.find(name='div', attrs={"id": self.td['div_id']}).find(name='table', attrs={"class": self.td['table_class']})
            # fix HTML
            for body in rows("tbody"):
                body.unwrap()
            self.output = pd.read_html(str(rows), flavor="bs4")[0]        
            #-- make column name(adapt to GoodInfo.)
            td_frscol = soup.find('thead').find('tr',{'height':'23px'}).find_all('td')
            cols = []
            for i in range(len(td_frscol)):
                col = td_frscol[i]
                if type(col.get('rowspan'))==str:
                    cols.append(col.text)
                else:
                    if len(cols) == i:
                        col = [col.text for col in soup.find('thead').find('tr',{'height':'40px'}).find_all('td')]
                        cols.extend(col)                
            #-- rename column
            self.output.columns.get_level_values(0)
            self.output.columns =cols
