# -*- coding: utf-8 -*-

from datasource import XueQiu
import indicator
import pprint
import helper

if __name__ == '__main__':
    data_source = XueQiu("SH600458")
    kline = data_source.get_month_kline()
    ind_builder = indicator.IndicatorBuilder()
    for unit in kline.unit_list:
        pprint.pprint(helper.dump(ind_builder.build_with(unit)))
        # print kline.get_highest()
