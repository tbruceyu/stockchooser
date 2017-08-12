# -*- coding: utf-8 -*-

from kline import Kline
from stockinfo import StockInfo


class NewStockModel(object):
    def __init__(self, stockInfo, kline):
        self.kline = kline
        self.stockInfo = stockInfo

    # 新股的找开口点
    def find_open_index(self):
        index = 0
        for unit in self.kline.unit_list:
            if unit.close != unit.open and unit.percent < 9.9:
                return index
            index += 1
        return -1

    def _cal_market_capital(self, index):
        return self._get_ratio(index) * self.stockInfo.marketCapital

    def _cal_pe_ttm(self, index):
        return self._get_ratio(index) * self.stockInfo.pe_ttm

    def _cal_pe_lyr(self, index):
        return self._get_ratio(index) * self.stockInfo.pe_lyr

    def _get_ratio(self, index):
        return self.stockInfo.close / self.kline.unit_list[index].close

    @staticmethod
    def _cal_price_ratio(low, high):
        if low == 0 or high == 0:
            return 1
        return (high - low) / low

    def start(self):
        open_index = self.find_open_index()
        if open_index < 0:
            return False
        lowest = self.kline.unit_list[open_index].close
        highest = self.kline.unit_list[open_index].close
        before_lowest_highest = self.kline.unit_list[open_index].close
        lowest_index = open_index
        highest_index = open_index
        record_low_index = 0
        max_hl_ratio = 0.0
        is_ok = False
        v_index = -1
        if open_index == -1:
            return False

        for i in range(open_index, len(self.kline.unit_list)):
            unit = self.kline.unit_list[i]
            if unit.close > highest:
                highest = unit.close
                highest_index = i
            if unit.close < lowest:
                lowest = unit.close
                lowest_index = i
                if highest_index < lowest_index:
                    before_lowest_highest = highest
            temp_ratio = self._cal_price_ratio(unit.close, highest)
            if temp_ratio >= 0.3 and highest_index < lowest_index and v_index == -1:
                v_index = i
            if v_index != -1 and self.kline.unit_list[v_index].close > lowest:
                v_index = i

        if v_index < 0:
            # print self.stockInfo.symbol + " 没有找到V点, 最低点前的最高点最低点相差 " + str(
            #     self._cal_price_ratio(lowest, before_lowest_highest))
            return False

        highest = 0
        count = 0
        for i in range(v_index, len(self.kline.unit_list)):
            unit = self.kline.unit_list[i]
            prev_unit = self.kline.unit_list[i - 1]
            walk_down = unit.close < prev_unit.close
            if unit.close > highest:
                highest = unit.close
                highest_index = i
            if unit.close < lowest:
                lowest = unit.close
                lowest_index = i
            # 如果不是走低,开始走高的话,开始寻找高点,这里需要重置之前设置的最高点
            if not walk_down:
                current_hl_ratio = self._cal_price_ratio(lowest, highest)
                if current_hl_ratio > max_hl_ratio:
                    max_hl_ratio = current_hl_ratio
                    record_low_index = lowest_index

        if max_hl_ratio > 0.30:
            pe_ttm = round(self._cal_pe_ttm(record_low_index))
            pe_lyr = round(self._cal_pe_lyr(record_low_index))
            capital = round(self._cal_market_capital(record_low_index) / 100000000)
            lunch_index = self._find_rise_point(lowest_index, highest_index)

            turnrate = "无"
            pre_5_turnrate = "无"

            if lunch_index > 0 and self.twenty_to_20(lunch_index):
                turnrate = str(self.kline.unit_list[lunch_index].turnrate)
                pre_5_turnrate = str(self._get_before_day_adv(lunch_index, 5))
                print self.stockInfo.symbol \
                      + ", " + self.stockInfo.name \
                      + ", " + str(max_hl_ratio) \
                      + ", " + str(highest_index - record_low_index) \
                      + ", " + str(lowest) \
                      + ", " + str(highest) \
                      + ", " + str(capital) + "亿" \
                      + ", " + str(round(capital * (self.stockInfo.float_shares / self.stockInfo.totalShares))) + "亿" \
                      + ", " + str(pe_ttm) + " (动) " + " " + str(pe_lyr) + " (静)" \
                      + ", " + turnrate \
                      + ", " + pre_5_turnrate
            # print "股票:" + self.stockInfo.symbol + " " + self.stockInfo.name + " 开板后最低到最高涨幅大于了30, 从最低到最高花了:" \
            #       + str(highest_index - record_low_index) + "个交易日" + " 最低价:" + str(lowest) + " 最高价:" \
            #       + str(highest) + " 最低市值:" + str(capital) \
            #       + " 市盈率 " + str(pe_ttm) + " (动) " \
            #       + str(pe_lyr) + " (静) " + " 涨幅:" + str(max_hl_ratio) + " 上市时间:" + self.stockInfo.list_display_date
            return True
        else:
            # print "股票:" + self.stockInfo.symbol + " " + self.stockInfo.name + " 最低价:" + str(lowest) + " 最高价:" \
            #       + str(highest) + " 涨幅:" + str(max_hl_ratio) + " 上市时间:" + self.stockInfo.list_display_date
            return False

    def twenty_to_20(self, index):
        lowest = self.kline.unit_list[index].close
        end_index = index + 20
        if end_index > len(self.kline.unit_list):
            end_index = len(self.kline.unit_list)

        for i in range(index, end_index):
            unit = self.kline.unit_list[i]
            ratio = self._cal_price_ratio(lowest, unit.close)
            if ratio > 0.2:
                return True
        return False

    def _find_rise_point(self, lowest_index, highest_index):
        for i in range(lowest_index, highest_index):
            turnrate = self.kline.unit_list[i].turnrate
            adv_pe = self._get_before_day_adv(i, 5)
            if turnrate >= adv_pe * 2:
                return i

        return -1

    def _get_before_day_adv(self, index, day):
        adv = 0.0
        start = index - day
        count = 0
        if index < day:
            start = 0

        for i in range(start, index):
            adv += self.kline.unit_list[i].turnrate
            count += 1
        return adv / count
