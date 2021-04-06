import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time 

# 輸入
def input_stock_num():

    stock_num = input("股票Number：")

    if(stock_num == "bye"):
        return 0

    return stock_num

# 爬資料
def data_scrapy(stock_num):
    start_time = time.time()
    print("1. Load網址")
    url_1 = 'https://webb-site.com/ccass/cconchist.asp?sc=' + stock_num
    url_2 = 'https://webb-site.com/ccass/ctothist.asp?s=&i=27707&sc=+' + stock_num + '+&o=1'
    url_3 = 'https://webb-site.com/dbpub/hpu.asp?s=datedn&sc=' + stock_num
    end_time = time.time()
    print("1. Load網址完成")
    print("執行時間：%f 秒\n" % (end_time - start_time))

    # 爬資料
    start_time = time.time()
    print("2. 爬資料")
    top10_read = pd.read_html(url_1)
    holders_read = pd.read_html(url_2)
    price_read = pd.read_html(url_3)
    end_time = time.time()
    print("2. 爬資料完成")
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

    # DataFrame
    start_time = time.time()
    print("4. DataFrame")
    top10_df = pd.DataFrame(top10_target)
    holders_df = pd.DataFrame(holders_target)
    price_df = pd.DataFrame(price_target)

    # Price整理
    price_df1 = price_df['AdjClose'][:92]

    # Merge
    merge_df = pd.concat([price_df1, top10_df, holders_df], axis=1)[:90]

    merge_df.set_index('Date',inplace=True)
    merge_df = merge_df.sort_values(by = 'Date')

    df = merge_df.drop(['Row', 'Top 10+NCIP%', 'Holdingdate', 'Holding', 'Change', 'Stake%', 'Issuedshares', 'As at date'] ,axis=1)
    df = df.rename(columns={"Top 5%": "Top5%", "Top 10%": "Top10%", "Stake inCCASS%":"in CCASS", "AdjClose":"Price"})
    df = df.reindex(columns=["Price", 'Top5%', 'Top10%', 'Holders', 'in CCASS'])

    end_time = time.time()
    print("4. DataFrame完成")
    print("執行時間：%f 秒\n" % (end_time - start_time))

    print(df)

    return df

# 畫圖
def draw_io(df, stock_num):
    # print(df)
    df.plot(subplots=True, grid=True, linestyle='-', fontsize=6, figsize = (10,7))
    plt.legend(loc='best')
    plt.suptitle(stock_num)
    plt.xticks(rotation=30)
    plt.show()
    plt.close()

if __name__ == "__main__":
    while(1):
        stock_num = input_stock_num()
        if(stock_num == 0):
            break

        # draw_io(data_scrapy(stock_num), stock_num)

        try:
            draw_io(data_scrapy(stock_num), stock_num)
        except:
            print("查無此股票\n")