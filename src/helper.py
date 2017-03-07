import os
import time
import ConfigParser
from var_dump import var_dump

CONFIG_FILE = 'conf.cfg'


def get_time_stamp_ms():
    return time.time() * 1000


def format_gmt_time(gmt_time):
    return long(time.mktime(time.strptime(gmt_time, "%a %b %d %H:%M:%S +0800 %Y")) * 1000)


def log(tag, msg):
    print tag + ":" + msg


def dump(obj):
    var_dump(obj)


def black_symbol(symbol):
    black_file = file('black.txt', 'a+')
    lines = black_file.readlines()
    for line in lines:
        if symbol == line:
            black_file.close()
            return
    black_file.write(symbol + "\n")
    log("helper", "black symbol:" + symbol)
    black_file.close()


def get_black_symbol_map():
    black_map = {}
    if not os.path.exists('black.txt'):
        return black_map
    black_file = file('black.txt', 'r')
    lines = black_file.readlines()
    black_file.close()
    for line in lines:
        line = line.strip()
        black_map[line] = True
    return black_map


def save_runtime_config(key, value):
    conf = ConfigParser.ConfigParser()
    conf.add_section("runtime")
    conf.set("runtime", key, value)
    fp = open(CONFIG_FILE, "w")
    conf.write(fp)
    fp.close()


def get_runtime_config(key):
    if not os.path.exists(CONFIG_FILE):
        return None
    cf = ConfigParser.ConfigParser()
    try:
        cf.read(CONFIG_FILE)
    except os.errno:
        return None
    return cf.get("runtime", key)
