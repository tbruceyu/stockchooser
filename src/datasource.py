# -*- coding: utf-8 -*-
import gzip
import json
import urllib2
from StringIO import StringIO
from abc import ABCMeta, abstractmethod

from stock import Stock

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
    info_url = "https://xueqiu.com/v4/stock/quote.json?code="
    stock = None

    def __init__(self, symbol):
        self.symbol = symbol

    def __info_to_obj(self, json_data):
        data_map = json.loads(json_data)[self.symbol]
        stock = Stock(**data_map)
        return stock

    def get_stock_info(self):
        if self.stock is not None:
            return self.stock
        request_url = self.info_url + self.symbol
        request = urllib2.Request(request_url, None, HTTP_HEADER)
        response = urllib2.urlopen(request, timeout=10)
        if response.info().get('Content-Encoding') == 'gzip':
            buf = StringIO(response.read())
            f = gzip.GzipFile(fileobj=buf)
            data = f.read()
            self.stock = self.__info_to_obj(data)
            return self.stock
        return None

    def to_unit(self):
        pass

    def get_month_daily(self):
        pass
