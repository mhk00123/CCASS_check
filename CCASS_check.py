import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time 
import ssl
import threading as td
from concurrent.futures import ThreadPoolExecutor


ssl._create_default_https_context = ssl._create_unverified_context

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}

# 輸入股票Number
def input_stock_num():
    stock_num = input("股票Number：")
    if(stock_num == "bye"):
        return 0
    
    return stock_num

def pdread(url):
    data = pd.read_html(url)
    return data

# 取得資料
def data_scrapy(stock_num):

    start_time = time.time()
    
    print("1. 讀取網址")
    # Top5, Top10, Stock in CCASS 數據
    url_1 = 'https://webb-site.com/ccass/cconchist.asp?sc=' + stock_num
    # Holders(投行數量)
    url_2 = 'https://webb-site.com/ccass/ctothist.asp?s=&i=27707&sc=+' + stock_num + '+&o=1'
    # 股價
    url_3 = 'https://webb-site.com/dbpub/hpu.asp?s=datedn&sc=' + stock_num
    
    end_time = time.time()
    print("1. 讀取網址完成")
    print("執行時間：%f 秒\n" % (end_time - start_time))

    # 爬取資料
    start_time = time.time()
    print("2. 爬取資料")

    # 創建3個線程池
    pool = ThreadPoolExecutor(max_workers=3)

    # 向線程池提交任務
    future1 = pool.submit(pdread, url_1)
    future2 = pool.submit(pdread, url_2)
    future3 = pool.submit(pdread, url_3)

    top10_read = future1.result()
    holders_read = future2.result()
    price_read = future3.result()
    
    pool.shutdown()
    end_time = time.time()

    print("2. 爬取資料完成")
    print("執行時間：%f 秒\n" % (end_time - start_time))

    # 讀取資料
    start_time = time.time()
    print("3. 取表格")

    top10_target = top10_read[1]
    holders_target = holders_read[1]
    price_target = price_read[1]
    end_time = time.time()

    print("3. 取表格完成")
    print("執行時間：%f 秒\n" % (end_time - start_time))

    # DataFrame(資料格式化)
    start_time = time.time()
    print("4. DataFrame")

    top10_df = pd.DataFrame(top10_target)
    holders_df = pd.DataFrame(holders_target)
    price_df = pd.DataFrame(price_target)

    # Price整理
    price_df1 = price_df['AdjClose'][:92]

    # Merge
    merge_df = pd.concat([price_df1, top10_df, holders_df], axis=1)[:90]

    # 排序
    merge_df.set_index('Date',inplace=True)
    merge_df = merge_df.sort_values(by = 'Date')

    # Drop 不需要欄位
    df = merge_df.drop(['Row', 'Top 10+NCIP%', 'Holdingdate', 'Holding', 'Change', 'Stake%', 'Issuedshares', 'As at date'] ,axis=1)
    
    # Rename, 重新排輸出順序
    df = df.rename(columns={"Top 5%": "Top5%", "Top 10%": "Top10%", "Stake inCCASS%":"in CCASS", "AdjClose":"Price"})
    df = df.reindex(columns=["Price", 'Top5%', 'Top10%', 'Holders', 'in CCASS'])

    end_time = time.time()
    print("4. DataFrame完成")
    print("執行時間：%f 秒\n" % (end_time - start_time))

    print(df)
    
    return df

# 畫圖
def draw_io(df, stock_num):
    df.plot(subplots=True, grid=True, linestyle='-', fontsize=6, figsize = (10,7))
    # 子圖圖例位置，目前只有"Best"設置，會使得圖例顥示在最空白位置，目前未有找到固定的方法。
    plt.legend(loc='best')  
    plt.suptitle(stock_num) # 標題
    plt.xticks(rotation=30) # X軸標籤旋轉30度
    plt.show()
    plt.close()

# Main Function 
if __name__ == "__main__":
    while(1):
        # 輸入股票number
        stock_num = input_stock_num()
        
        if(stock_num == 0):
            break
        
        rs = data_scrapy(stock_num)
        print("RS pass")
        
        try:
            draw_io(rs, stock_num)
        except:
            print("查無此股票\n")