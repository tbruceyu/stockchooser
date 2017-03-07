# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod

GREAT_THRESHOLD = 10
HUMMER_HEAD_THRESHOLD = 5


class Indicator(object):
    __metaclass__ = ABCMeta

    def __init__(self, unit):
        self.unit = unit


class GreatUp(Indicator):
    # 大阳线
    def __init__(self, unit):
        super(GreatUp, self).__init__(unit)

    @staticmethod
    def measure(unit):
        if unit.get_up_shadow_percent() < GREAT_THRESHOLD \
                and unit.get_down_shadow_percent() < GREAT_THRESHOLD \
                and unit.percent >= 5.0 \
                and unit.is_up():
            return True
        return False


class GreatDown(Indicator):
    # 大阴线
    def __init__(self, unit):
        super(GreatDown, self).__init__(unit)

    @staticmethod
    def measure(unit):
        if unit.get_up_shadow_percent() < GREAT_THRESHOLD \
                and unit.get_down_shadow_percent() < GREAT_THRESHOLD \
                and unit.percent >= 5.0 \
                and not unit.is_up():
            return True
        return False


class HammerUp(Indicator):
    def __init__(self, unit):
        super(HammerUp, self).__init__(unit)

    @staticmethod
    def measure(unit):
        if unit.get_up_shadow_percent() > GREAT_THRESHOLD \
                and unit.get_down_shadow_percent() < HUMMER_HEAD_THRESHOLD and unit.is_up():
            return True
        return False


class HammerDown(Indicator):
    # 大阴线
    def __init__(self, unit):
        super(HammerDown, self).__init__(unit)

    @staticmethod
    def measure(unit):
        if unit.get_down_shadow_percent() > GREAT_THRESHOLD \
                and unit.get_up_shadow_percent() < HUMMER_HEAD_THRESHOLD and not unit.is_up():
            return True
        return False


class IndicatorBuilder(object):
    all_indicators = {GreatUp, GreatDown, HammerUp, HammerDown}

    def build_with(self, unit):
        ind_obj = []
        for ind_cls in self.all_indicators:
            if ind_cls.measure(unit):
                ind_obj.append(ind_cls(unit))
        return ind_obj
