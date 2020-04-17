# --------------------------------------------------------------------------------------
import pandas
Git_path   = 'D:/Git_Project/'
Project_nm = 'AI_Investment'
# --------------------------------------------------------------------------------------
stock_ls1 = pandas.read_html('https://isin.twse.com.tw/isin/C_public.jsp?strMode=2')[0]
stock_ls2 = pandas.read_html('https://isin.twse.com.tw/isin/C_public.jsp?strMode=4')[0]

stock_ls1 = stock_ls1[stock_ls1[0].str.find("¡@") > 0]
stock_ls1["Code"] = stock_ls1[0].str.split("¡@", n = 1, expand = True)[0]
stock_ls1["idx1"] = stock_ls1[5].str.slice(start = 0, stop = 3) == "ESV"
stock_ls1["idx2"] = stock_ls1[5].str.slice(start = 0, stop = 3) == "CEO"
stock_ls1 = stock_ls1[stock_ls1[['idx1', 'idx2']].any(1)]

stock_ls2 = stock_ls2[stock_ls2[0].str.find("¡@") > 0]
stock_ls2["Code"] = stock_ls2[0].str.split("¡@", n = 1, expand = True)[0]
stock_ls2["idx1"] = stock_ls2[5].str.slice(start = 0, stop = 3) == "ESV"
stock_ls2["idx2"] = stock_ls2[5].str.slice(start = 0, stop = 3) == "CEO"
stock_ls2 = stock_ls2[stock_ls2[['idx1', 'idx2']].any(1)]

# data = pandas.read_csv("https://media.geeksforgeeks.org/wp-content/uploads/nba.csv")

stock_ls1 = stock_ls1["Code"].reset_index(drop = True)
stock_ls2 = stock_ls2["Code"].reset_index(drop = True)

fo = open(Git_path + Project_nm + "/TW_Stock_Code1.csv", "w");
fo.write("Code" + "\n");
for i in range(0, len(stock_ls1)-1):
    fo.write(str(stock_ls1[i]) + "\n");
fo.close()

fo = open(Git_path + Project_nm + "/TW_Stock_Code2.csv", "w");
fo.write("Code" + "\n");
for i in range(0, len(stock_ls2)-1):
    fo.write(str(stock_ls2[i]) + "\n");
fo.close()
# --------------------------------------------------------------------------------------