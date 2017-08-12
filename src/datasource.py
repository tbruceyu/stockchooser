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
    'Cookie': 's=691915x1tw; webp=1; bid=a4c7e7b2b5b089672ec38f911de150a4_iyz949tq; device_id=b2479fe4a5560872b'
              'b6071e36d8db867; remember=1; remember.sig=K4F3faYzmVuqC0iXIERCQf55g2Y; xq_a_token=8b97ab28179b040'
              '7a8248af93817f23f7943a4cf; xq_a_token.sig=1lS8Im4PTKV4NhUeET7EKIWjS_I; xq_r_token=657750dd45b6dbf9'
              'efc5d624c66d67320bee5a3c; xq_r_token.sig=_A-by6x6nLXo9C33XAtFqLjA_NA; xq_is_login=1; xq_is_login.sig'
              '=J3LxgPVPUzbBg3Kee_PquUfih7Q; u=3624172871; u.sig=nN2ADMRg5z6s-MVHoUWkaRCin68; aliyungf_tc=AQAAACt3'
              'X2ogUwwAEpM0eHRQVSVT97Lz; Hm_lvt_1db88642e346389874251b5a1eded6e3=1501724508,1501996041,1502084866,15'
              '02156458; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1502174421; __utma=1.1813155390.1486697195.15021'
              '58717.1502173678.62; __utmc=1; __utmz=1.1489325639.23.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic'
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
    kline_url = "https://xueqiu.com/stock/forchartk/stocklist.json?symbol=%s&period=1day&type=normal&begin=%ld&end=%ld&_=%ld"
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
        return self.get_kline_from(three_month_ago, now)

    def get_kline_from(self, from_timestamp, to_timestamp):
        request_url = self.kline_url % (self.symbol, from_timestamp, to_timestamp, to_timestamp)
        try:
            json_data = http_helper.get_url(request_url, HTTP_HEADER)
            unit_list = self.__kline_to_obj_list(json_data)
            if len(unit_list) is 0:
                return None
            kline = Kline(unit_list)
            kline.set_stock_info(self.stock)
            return kline
        except Exception:
            return None

    def to_unit(self):
        pass

    def get_month_daily(self):
        pass
