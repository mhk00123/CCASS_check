# CCASS_check
A program can check CCASS data : Top5%, Top10%, Stake in CCASS%, Holders......

## Features

- 快速查詢過3個月CCASS的資料：
- Top5, Top10持倉比例
- 流通股量
- Holder數量

## 開發環境
- Python 3.7.4 64bit

## 依賴
- Pandas
> pip install pandas

- Matplotlib
> pip install matplotlib

## 開發思路
由於CCASS網站是較為傳統的網站，大部份資料都以HTML方式呈現，可以直接爬取，因此直接透過Pandas自帶`read_html()`方法即可以取得所需資料，不需要另外引入額外的爬取方式。

