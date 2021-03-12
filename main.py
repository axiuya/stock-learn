# This is a sample Python script.

import tushare
import pandas
import datetime


def get_tickers_raw_data():
    # pro = tushare.pro_api("631baaa01d1fc48b4e3c9c4421c3c4df9adcc9ffd40d2f919a0e2fed")
    pro = tushare.pro_api("007b2f24bc3afb5ff5c604b0aee583956840210348169bc2436bddf9")
    # tickersRawData = pro.get_stock_basics("20210305")
    # print(tickersRawData)

    frame = pro.query("stock_basic")
    print(frame)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_tickers_raw_data()

