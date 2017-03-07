# -*- coding: utf-8 -*-
import json

import time

import http_helper
import helper
from abc import ABCMeta, abstractmethod
from kline import Unit, Kline

from stockinfo import StockInfo

HTTP_HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
    'Cache-Control': 'no-cache',
    'Referer': 'https://xueqiu.com',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'Pragma': 'no-cache',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
    'Cookie': 's=691915x1tw; webp=1; bid=a4c7e7b2b5b089672ec38f911de150a4_iyz949tq; ' \
              'aliyungf_tc=AQAAAKoksXWhNQcAEvcnaiQPaDRXjqqF; snbim_minify=true;' \
              ' xq_a_token=d99e7179f8df67bdf02ab6444d1f74a8091818b9;' \
              ' xq_r_token=01013b7c908ec46fa80f9cc2a66b917b6a8121dc;' \
              ' u=121488704118566; Hm_lvt_1db88642e346389874251b5a1eded6e3=1486720344,' \
              '1487501160,1487565836,1488685258; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1488704119;' \
              ' __utma=1.1813155390.1486697195.1488686123.1488704119.7;' \
              ' __utmb=1.1.10.1488704119; __utmc=1; __utmz=1.1486697195.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'
}


class BaseDataSource(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_stock_info(self): pass

    @abstractmethod
    def to_unit(self): pass

    @abstractmethod
    def get_month_daily(self): pass


class XueQiu(BaseDataSource):
    info_url = "https://xueqiu.com/v4/stock/quote.json?code=%s"
    kline_url = "https://xueqiu.com/stock/forchartk/stocklist.json?symbol=%s&period=1day&type=before&begin=%ld&end=%ld&_=%ld"
    stock = None

    def __init__(self, symbol):
        self.symbol = symbol

    def __info_to_obj(self, json_data):
        data_map = json.loads(json_data)[self.symbol]
        stock = StockInfo(**data_map)
        return stock

    def get_stock_info(self):
        if self.stock is not None:
            return self.stock
        request_url = self.info_url % self.symbol
        json_data = http_helper.get_url(request_url, HTTP_HEADER)
        self.stock = self.__info_to_obj(json_data)
        return self.stock

    def __kline_to_obj_list(self, json_data):
        chart_list = json.loads(json_data)['chartlist']
        list = []
        for chat in chart_list:
            chat['time'] = helper.format_gmt_time(chat['time'])
            unit = Unit(**chat)
            list.append(unit)
        return list

    def get_quarter_kline(self):
        now = helper.get_time_stamp_ms()
        three_month_ago = now - 3600 * 24 * 30 * 1000 * 3
        request_url = self.kline_url % (self.symbol, three_month_ago, now, now)
        try:
            json_data = http_helper.get_url(request_url, HTTP_HEADER)
            unit_list = self.__kline_to_obj_list(json_data)
            if len(unit_list) is 0:
                return None
            return Kline(self.stock, unit_list)
        except KeyError:
            return None

    def to_unit(self):
        pass

    def get_month_daily(self):
        pass
