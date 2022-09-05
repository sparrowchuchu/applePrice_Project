# Crawler: Currencies Rate
# Author : Sharon Wang 2022 Aug
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import datetime, time

# Requests ProductUrl 
# 取得目標 Product soup
def getResponse(url:str):
    response=requests.get(url)
    if response.status_code==200:
        print(f'O 讀取 {url} 成功')
        soup=BeautifulSoup(response.text,'lxml')
        return soup
    else:
        print(f'X 讀取 {url} 失敗')
        return

def closingPrice(f,t):
    url=f'https://www.google.com/finance/quote/{f}-{t}'
    print(f'查詢 {f} 兌換為 {t}')
    try:
        soup=getResponse(url)
        lastClosingPrice=soup.find(id='yDmH0d').find('div','gyFHrc')
        price=lastClosingPrice.text.split('price')[-1]        
    except:
        price='1'
    print(price)
    return [f,price]


star=time.time()
today=datetime.datetime.now().strftime('%Y%m%d')
# 連接 資料庫 取出資料
dbIn='apple_shop_ver6'
conn=sqlite3.connect(f'{dbIn}.db')
print(f'Connect {dbIn}.db successfully.')
storeCurrency=conn.execute(f'SELECT DISTINCT currency FROM apple{today}').fetchall()
conn.close()
print(f'Closed {dbIn}.db successfully.')

# 貨幣和加密貨幣價格由 Morningstar 提供
exchangeTWD=[]
exchangeUSD=[]
currency=[f[0] for f in storeCurrency]
for c in currency:
    f=c.upper()
    t='twd'.upper()   
    exchangeTWD.append(closingPrice(f,t))
    t='usd'.upper()
    exchangeUSD.append(closingPrice(f,t))
    print('-'*20)
    time.sleep(.1)

# 儲存 csv 檔
twd=pd.DataFrame(exchangeTWD,columns=['code',f'toTWDprice{today}']).sort_values(by=['code'])
usd=pd.DataFrame(exchangeUSD,columns=['code',f'toUSDprice{today}']).sort_values(by=['code'])
currencyPrice=twd.merge(usd,how='outer',on='code',suffixes=('','')) 
currencyPrice.to_csv(f'currencyClosingPrice{today}.csv')

# 計算換匯後的價錢，寫入資料庫。
dbIn='apple_shop_ver6'
conn=sqlite3.connect(f'{dbIn}.db')
print(f'Connect {dbIn}.db successfully.')
conn.execute(f'ALTER TABLE apple{today} ADD twdPrice float')
conn.execute(f'ALTER TABLE apple{today} ADD usdPrice float')
exchange=conn.execute(f'SELECT id,price,currency FROM apple{today}').fetchall()
exchangePrice=[]
for i,price,code in exchange:
    print(i,price,code)
    for twd,usd in zip(exchangeTWD,exchangeUSD):
        if twd[0]==code:
            twdPrice1=eval(twd[1])*price
            usdPrice1=eval(usd[1])*price
            exchangePrice.append((twdPrice1,usdPrice1))
            sql=f'''UPDATE apple{today}
                   SET twdPrice={twdPrice1},usdPrice={usdPrice1}
                   WHERE id = {i}'''
            conn.execute(sql)
            continue
print('Execute: SQL successfully.')
conn.commit()
conn.close()
print(f'Closed {dbIn}.db successfully.')

end=time.time()
print('Date   : ',today,'\nRunTime: ',end-star,'\nDone.')





