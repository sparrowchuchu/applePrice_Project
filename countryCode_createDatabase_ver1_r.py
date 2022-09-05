# Databace
# Author: Sharon Wang 2022 Aug
import requests
import pandas as pd
import sqlite3

# Country_List
sourceButterfly=requests.get("http://butterfly.abacus.com.tw/docs/countryList.htm#up")
sourceButterfly.encoding = "big5"

if sourceButterfly.status_code==200:
    print("讀取 URL 成功")
else:
    print("讀取 URL 失敗")
    
df=pd.read_html(sourceButterfly.text)
colButterfly=pd.Series(['國碼','國家／地區_英文名稱','國家／地區'])
dfButterfly=df[1].dropna().rename(columns=colButterfly).iloc[1:,:]

# Country_Territory_and_Currency_Codes
sourceUps=requests.get("https://www.ups.com/worldshiphelp/WSA/CHT/AppHelp/mergedProjects/CORE/Codes/Country_Territory_and_Currency_Codes.htm")
sourceUps.encoding = "utf-8"

if sourceUps.status_code==200:
    print("讀取 URL 成功")
else:
    print("讀取 URL 失敗")
    
df=pd.read_html(sourceUps.text)
dfUps=df[0].rename(columns=df[0].iloc[0,:]).iloc[1:,:]

# 合併 DataFrame
dfCountryCodes=dfButterfly.merge(dfUps,how='outer')

# 連接資料庫，如果資料庫不存在則建立資料庫。
conn = sqlite3.connect('country_code.db')  
print('Connect Database')

# pandas格式資料寫入資料庫。
dfCountryCodes.to_sql('country_code', conn)
print('資料寫入完成')

conn.close()
print('Closed Database successfully')