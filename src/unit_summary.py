class UnitSummary(object):
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


