# This is a sample Python script.

import tushare
import pandas
import datetime


def get_tickers_raw_data():
    pro = tushare.pro_api("631baaa01d1fc48b4e3c9c4421c3c4df9adcc9ffd40d2f919a0e2fed")
    # tickersRawData = pro.get_stock_basics("20210305")
    # print(tickersRawData)

    frame = pro.query("stock_basic")
    print(frame)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_tickers_raw_data()

