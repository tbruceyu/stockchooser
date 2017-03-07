# -*- coding: utf-8 -*-
import time

from datasource import XueQiu
import helper

if __name__ == '__main__':
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
        print name + ":" + symbol + " LP:" + str(kline.is_latest_low_point())
        time.sleep(1)
        # ind_builder = indicator.IndicatorBuilder()
        # for unit in kline.unit_list:
        #     helper.dump(ind_builder.build_with(unit))
        # print kline.get_highest()
