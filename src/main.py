# -*- coding: utf-8 -*-
from datasource import XueQiu

if __name__ == '__main__':
    data_source = XueQiu("SH600458")
    stock = data_source.get_stock_info()
    print stock.name
