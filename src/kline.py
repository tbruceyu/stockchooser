# -*- coding: utf-8 -*-
import time

RATIO_CONST = 100


class Kline(object):
    def __init__(self, stock_info, unit_list):
        self.stock_info = stock_info
        self.unit_list = unit_list

    def get_highest(self):
        highest_unit = self.unit_list[0]
        for unit in self.unit_list:
            if unit.close > highest_unit.close:
                highest_unit = unit

        return highest_unit

    def get_lowest(self):
        lowest_unit = self.unit_list[0]
        for unit in self.unit_list:
            if unit.close < lowest_unit.close:
                lowest_unit = unit

        return lowest_unit

    def get_latest(self):
        return self.unit_list[len(self.unit_list) - 1]

    # 获取最近5日的K线unit,如果是新股,可能返回的list会小于5
    def get_last5(self):
        last_offset = len(self.unit_list) - 1
        start = (last_offset - 5) >= 0 and (last_offset - 5) or 0
        return self.unit_list[start:last_offset]

    # 最近5日只要有一个点和最低点的差值与最高低差值比在20
    def is_latest_low_point(self):
        highest = self.get_highest()
        lowest = self.get_lowest()
        high_low_diff = highest.close - lowest.close
        last5 = self.get_last5()
        for unit in last5:
            diff_percent = ((unit.close - lowest.close) / high_low_diff) * 100
            if diff_percent < 20:
                return True
        return False


class Unit(object):
    def __init__(self, **kwargs):
        self.volume = kwargs['volume']
        self.open = kwargs['open']
        self.high = kwargs['high']
        self.close = kwargs['close']
        self.low = kwargs['low']
        self.chg = kwargs['chg']
        self.percent = kwargs['percent']
        self.turnrate = kwargs['turnrate']
        self.ma5 = kwargs['ma5']
        self.ma10 = kwargs['ma10']
        self.ma20 = kwargs['ma20']
        self.ma30 = kwargs['ma30']
        self.dif = kwargs['dif']
        self.dea = kwargs['dea']
        self.macd = kwargs['macd']
        self.time = kwargs['time']
        self.human_time = time.strftime('%Y-%m-%d', time.localtime(self.time / 1000))

    def is_up(self):
        return self.open < self.close

    def get_up_shadow(self):
        if self.is_up():
            return self.high - self.close
        else:
            return self.high - self.open

    # 获取上影线长度百分比
    def get_up_shadow_percent(self):
        up_shadow = self.get_up_shadow()
        divisor = self.get_entity() + up_shadow
        divisor = divisor == 0 and 1 or divisor
        return int((up_shadow / divisor) * RATIO_CONST)

    def get_down_shadow(self):
        if self.is_up():
            return self.open - self.low
        else:
            return self.close - self.low

    # 获取下影线长度百分比
    def get_down_shadow_percent(self):
        down_shadow = self.get_down_shadow()
        divisor = self.get_entity() + down_shadow
        divisor = divisor == 0 and 1 or divisor
        return int((down_shadow / divisor) * RATIO_CONST)

    # 获取实体长度
    def get_entity(self):
        if self.is_up():
            return self.close - self.open
        else:
            return self.open - self.close
