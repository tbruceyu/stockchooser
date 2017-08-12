# -*- coding: utf-8 -*-
from src.helper import timestamp_to_datetime


class BaseStockInfo(object):
    def __init__(self, **kwargs):
        self.symbol = kwargs['symbol']
        self.name = kwargs['name']
        # 上市时间
        self.list_date = kwargs['list_date']
        self.list_display_date = timestamp_to_datetime(self.list_date)


class StockInfo(object):
    def __init__(self, **kwargs):
        self.symbol = kwargs['symbol']  # self.symbol= "SH600458"
        self.exchange = kwargs['exchange']  # self.exchange= "SH"
        self.code = kwargs['code']  # self.code = "600458"
        self.name = kwargs['name']  # self.name = "时代新材"
        self.current = kwargs['current']  # self.current = 14.39
        self.percentage = kwargs['percentage']  # self.percentage = "0.3"
        self.change = kwargs['change']  # self.change= "0.00"
        self.open = float(kwargs['open'])  # self.open = "14.31"
        self.high = float(kwargs['high'])  # self.high = "14.39"
        self.low = float(kwargs['low'])  # self.low = "14.24"
        self.close = float(kwargs['close'])  # self.close = "14.39"
        self.last_close = kwargs['last_close']  # self.last_close = "14.39"
        self.high52week = kwargs['high52week']  # self.high52week = "18.49"
        self.low52week = kwargs['low52week']  # self.low52week = "11.71"
        self.volume = kwargs['volume']  # self.volume = "4702170.0"#
        self.volumeAverage = kwargs['volumeAverage']  # self.volumeAverage = "24561243"
        self.marketCapital = float(kwargs['marketCapital'])
        # self.eps = "0.25"
        # 市盈率（动）
        self.pe_ttm = float(kwargs['pe_ttm'])
        # 市盈率（静）
        self.pe_lyr = float(kwargs['pe_lyr'])
        self.float_shares = float(kwargs['float_shares'])
        self.totalShares = float(kwargs['totalShares'])
        if 'list_date' in kwargs:
            self.list_date = kwargs['list_date']
            self.list_display_date = timestamp_to_datetime(self.list_date)

        # self.beta = "0.0"
        # self.totalShares = "802798152"
        # self.time = "Fri Mar 03 14=59=59 +0800 2017"
        # self.afterHours = "0.0"
        # self.afterHoursPct = "0.0"
        # self.afterHoursChg = "0.0"
        # self.updateAt = "1469448001946"
        # self.dividend = "0.05"
        # self.yield_ = "0.35"
        # self.turnover_rate = "0.71%"
        # self.instOwn = "0.0"
        # self.rise_stop = "15.83"
        # self.fall_stop = "12.95"
        # self.currency_unit = "CNY"
        # self.amount = "6.7255283E7"
        # self.net_assets = "6.1025"
        # self.hasexist = ""
        # self.has_warrant = "0"
        # self.type = "11"
        # self.flag = "1"
        # self.rest_day = ""
        # self.amplitude = "1.04%"
        # self.market_status = "周末休市"
        # self.lot_size = "100"
        # self.min_order_quantity = "0"
        # self.max_order_quantity = "0"
        # self.tick_size = "0.01"
        # self.kzz_stock_symbol = ""
        # self.kzz_stock_name = ""
        # self.kzz_stock_current = "0.0"
        # self.kzz_convert_price = "0.0"
        # self.kzz_covert_value = "0.0"
        # self.kzz_cpr = "0.0"
        # self.kzz_putback_price = "0.0"
        # self.kzz_convert_time = ""
        # self.kzz_redempt_price = "0.0"
        # self.kzz_straight_price = "0.0"
        # self.kzz_stock_percent = ""
        # self.pb = "2.36"
        # self.benefit_before_tax = "0.0"
        # self.benefit_after_tax = "0.0"
        # self.convert_bond_ratio = ""
        # self.totalissuescale = ""
        # self.outstandingamt = ""
        # self.maturitydate = ""
        # self.remain_year = ""
        # self.convertrate = "0.0"
        # self.interestrtmemo = ""
        # self.release_date = ""
        # self.circulation = "0.0"
        # self.par_value = "0.0"
        # self.due_time = "0.0"
        # self.value_date = ""
        # self.due_date = ""
        # self.publisher = ""
        # self.redeem_type = "T"
        # self.issue_type = "1"
        # self.bond_type = ""
        # self.warrant = ""
        # self.sale_rrg = ""
        # self.rate = ""
        # self.after_hour_vol = "0"
        # self.float_market_capital = "9.51786388949E9"
        # self.disnext_pay_date = ""
        # self.convert_rate = "0.0"
        # self.psr = "1.0639"

    def set_list_time(self, timestamp):
        self.list_date = timestamp
        self.list_display_date = timestamp_to_datetime(self.list_date)
