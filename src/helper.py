import time
import types
from var_dump import var_dump

def get_time_stamp_ms():
    return time.time() * 1000


def format_gmt_time(gmt_time):
    return long(time.mktime(time.strptime(gmt_time, "%a %b %d %H:%M:%S +0800 %Y")) * 1000)


def log(tag, msg):
    print tag + ":" + msg


def dump(obj):
    var_dump(obj)


def dump_obj(obj):
    if type(obj) == list:
        for item in obj:
            __dump_obj(item)


def __dump_obj(obj, level=0):
    for key, value in obj.__dict__.items():
        if not isinstance(value, types.InstanceType):
            print " " * level + "%s -> %s" % (key, value)
        else:
            dump_obj(value, level + 2)
