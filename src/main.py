# -*- coding: utf-8 -*-
import time

import re

from datasource import XueQiu
import helper
from src.collect import get_latest_new
from src.model import NewStockModel
from src.stockinfo import StockInfo


def find_low():
    stock_file = open('stocks.txt', 'r')
    stock_lines = stock_file.readlines()
    black_symbol_map = helper.get_black_symbol_map()
    work_index = helper.get_runtime_config("work_index")
    if work_index:
        work_index = int(work_index)
        stock_lines = stock_lines[work_index:(len(stock_lines) - 1)]
    i = 0
    for line in stock_lines:
        start_index = line.find(":")
        helper.save_runtime_config("work_index", i)
        i += 1
        if start_index < 1:
            continue
        name = line[0:start_index]
        symbol = line[start_index + 1:(len(line) - 1)]
        if black_symbol_map.get(symbol):
            continue
        data_source = XueQiu(symbol)
        kline = data_source.get_quarter_kline()
        if kline is None:
            # 如果不能拿到K线,说明这个股票有问题,需要拉黑
            helper.black_symbol(symbol)
            continue
        if kline.is_stop():
            # 如果停牌,则忽略
            helper.log("stock", name + " 已停牌")
            continue
        print name + ":" + symbol + " LP:" + str(kline.is_latest_low_point())
        time.sleep(1)


def main_get_latest():
    save_file = open('data/latest.csv', 'w')
    save_file.write("股票名, 代码, 时间戳, 上市时间\n")
    for i in range(1, 7):
        if get_latest_new(save_file, i) is False:
            break
            # ind_builder = indicator.IndicatorBuilder()
            # for unit in kline.unit_list:
            #     helper.dump(ind_builder.build_with(unit))
            # print kline.get_highest()
    save_file.close()


def main_analyze():
    latest_file = open('data/latest.csv', 'r')
    line = latest_file.readline()
    good_count = 0
    bad_count = 0
    for line in latest_file.xreadlines():
        group = line.split(', ')
        symbol = group[0]
        start_timestamp = long(group[2])
        display_time = group[3]
        if _analyze_stock(symbol, start_timestamp):
            good_count += 1
        else:
            bad_count += 1
    print "满足条件的数量:%d, 不满足的数量:%d" % (good_count, bad_count)


def _analyze_stock(symbol, start_timestamp):
    data_source = XueQiu(symbol)
    now_ms = helper.get_time_stamp_ms()
    end_timestamp_ms = start_timestamp * 1000 + 365 * 3600 * 24 * 1000
    if now_ms < end_timestamp_ms:
        end_timestamp_ms = now_ms

    stock_info = data_source.get_stock_info()
    stock_info.set_list_time(start_timestamp)
    kline = data_source.get_kline_from(start_timestamp * 1000, end_timestamp_ms)
    if kline is None or kline.unit_list is None or len(kline.unit_list) is 0:
        return
    model = NewStockModel(stock_info, kline)
    return model.start()


if __name__ == '__main__':
    # main_get_latest()
    print "股票, 公司名, 涨幅, 交易日, 最低价, 最高价, 市值, 流通市值, 最低市盈率, 启动时换手率, 前五天平均换手率"

    main_analyze()
    # _analyze_stock("SZ300657", 1495468800)
