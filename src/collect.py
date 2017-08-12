# -*- coding: utf-8 -*-
import sys

from src import helper

reload(sys)
sys.setdefaultencoding("utf-8")

import json

import datasource
import http_helper
from stockinfo import BaseStockInfo

# 2016/2/9 14:40:0
END_TIME = 1455000000


def get_latest_new(save_file, page):
    request_url = 'https://xueqiu.com/proipo/query.json?page=' + str(
        page) + '&size=90&order=desc&orderBy=onl_subbegdate&stockType=&column=symbol%2Cname%2Conl_subcode%2Clist_date%2Cactissqty%2Conl_actissqty%2Conl_submaxqty%2Conl_subbegdate%2Conl_unfrozendate%2Conl_refunddate%2Ciss_price%2Conl_frozenamt%2Conl_lotwinrt%2Conl_lorwincode%2Conl_lotwiner_stpub_date%2Conl_effsubqty%2Conl_effsubnum%2Conl_onversubrt%2Coffl_lotwinrt%2Coffl_effsubqty%2Coffl_planum%2Coffl_oversubrt%2Cnapsaft%2Ceps_dilutedaft%2Cleaduwer%2Clist_recomer%2Cacttotraiseamt%2Conl_rdshowweb%2Conl_rdshowbegdate%2Conl_distrdate%2Conl_drawlotsdate%2Cfirst_open_price%2Cfirst_close_price%2Cfirst_percent%2Cfirst_turnrate%2Cstock_income%2Conl_lotwin_amount%2Clisted_percent%2Ccurrent%2Cpe_ttm%2Cpb%2Cpercent%2Chasexist&_=1502195561887'
    json_data = http_helper.get_url(request_url, datasource.HTTP_HEADER)
    data_map = json.loads(json_data)
    info = {}

    for data in data_map['data']:
        if data[3] is None:
            continue
        info['symbol'] = data[0]
        info['name'] = data[1]
        info['list_date'] = helper.format_cst_time(data[3])
        if info['list_date'] <= END_TIME:
            return False
        stock = BaseStockInfo(**info)

        save_file.write(stock.symbol + ', ' + stock.name + ', ' + str(stock.list_date) + ", " + str(stock.list_display_date) + '\n')

    return True
