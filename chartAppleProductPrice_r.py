# Chart  : Apple Product Price
# Author : Sharon Wang 2022 Aug
import pandas as pd
import sqlite3
import time
import matplotlib.pyplot as plt

star = time.time()
today = '20220816'
# 連接 資料庫 取出資料
dbIn = 'apple_shop_ver6'
conn = sqlite3.connect(f'{dbIn}.db')
print(f'Connect {dbIn}.db successfully.')
source = conn.execute(f'SELECT * FROM apple{today}').fetchall()
conn.close()
print(f'Closed {dbIn}.db successfully.')

colName = ['id', 'category', 'name', 'price', 'currency',
           'computedCustomStoreName', 'sku', 'twdPrice', 'usdPrice']
sourceDf = pd.DataFrame(source, columns=colName)

# 取出 各國 macbook, ipad, iphone 旗艦機資料
# 16-inch MacBook Pro                     : MK1H3
macbookFs=sourceDf.groupby('sku').get_group('MK1H3')
macbookFsTWD_x=macbookFs.sort_values('twdPrice')['computedCustomStoreName']
macbookFsTWD_x=[i.split(' ')[1] for i in macbookFsTWD_x][:-1]    # Brazil 是離群值，移除。
macbookFsTWD_y=macbookFs.sort_values('twdPrice')['twdPrice'][:-1]

# 12.9-inch iPad Pro Wi-Fi + Cellular 2TB - Silver : MHRE3
ipadFs=sourceDf.groupby('name').get_group('12.9-inch iPad Pro Wi-Fi + Cellular 2TB - Silver')
ipadFsTWD_x=ipadFs.sort_values('twdPrice')['computedCustomStoreName']
ipadFsTWD_x=[i.split(' ')[1] for i in ipadFsTWD_x][:-1]
ipadFsTWD_y=ipadFs.sort_values('twdPrice')['twdPrice'][:-1]

# iPhone 13 Pro Max 1TB Silver  : MLLL3。 MLHJ3: CNY,HKD。 MLKH3: CAD, JPY, MXN
iphoneFs=sourceDf.groupby('name').get_group('iPhone 13 Pro Max 1TB Silver')
iphoneFsTWD_x=iphoneFs.sort_values('twdPrice')['computedCustomStoreName']
iphoneFsTWD_x=[i.split(' ')[1] for i in iphoneFsTWD_x][:-1]
iphoneFsTWD_y=iphoneFs.sort_values('twdPrice')['twdPrice'][:-1]


plt.rcParams['font.family']='Microsoft YaHei'
plt.rcParams['font.size']=12

# 各國 mac, ipad, iphone 最高價規格產品 長條圖
# 註記: StoreName Apple 是 Luxembourg
figMacbookFS='16-inch MacBook Pro'
plt.figure(figsize=(14,7))
plt.bar(macbookFsTWD_x,macbookFsTWD_y,label='換算台幣售價',color='#6E75A4',width=.5)
plt.xticks(rotation=90,fontsize=12) 
plt.ylim(90000, 150000)
plt.title('%s\n'%figMacbookFS,fontsize=27)
plt.xlabel('StoreName',fontsize=16)     
plt.ylabel('TWD Price',fontsize=16)       
plt.legend() 
plt.grid(axis='y')
plt.savefig('%sN.png'%figMacbookFS,dpi=300,bbox_inches='tight')
plt.show()
plt.close()

figIpadFs='12.9-inch iPad Pro Wi-Fi + Cellular 2TB'
plt.figure(figsize=(14,7))
plt.bar(ipadFsTWD_x,ipadFsTWD_y,label='換算台幣售價',color='#1E88A8',width=.5)
plt.xticks(rotation=90,fontsize=12) 
plt.ylim(65000, 100000)
plt.title('%s\n'%figIpadFs,fontsize=27)
plt.xlabel('StoreName',fontsize=16)     
plt.ylabel('TWD Price',fontsize=16)       
plt.legend() 
plt.grid(axis='y') 
plt.savefig('%sN.png'%figIpadFs,dpi=300,bbox_inches='tight')
plt.show()
plt.close()

figIphoneFs='iPhone 13 Pro Max 1TB'
plt.figure(figsize=(14,7))
plt.bar(iphoneFsTWD_x,iphoneFsTWD_y,label='換算台幣售價',color='#24936E',width=.5)
plt.xticks(rotation=90,fontsize=12) 
plt.ylim(45000, 75000)
plt.title('%s\n'%figIphoneFs,fontsize=27)
plt.xlabel('StoreName',fontsize=16)     
plt.ylabel('TWD Price',fontsize=16)       
plt.legend() 
plt.grid(axis='y') 
plt.savefig('%sN.png'%figIphoneFs,dpi=300,bbox_inches='tight')
plt.show()
plt.close()

end = time.time()
print('RunTime: ', end-star, '\nDone.')
