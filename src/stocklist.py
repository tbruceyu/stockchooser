# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
import re
import requests
from bs4 import BeautifulSoup

HTTP_HEADER = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
TIME_OUT = 15

CHUANGYE_RE = r'300\d{3}'
HU_A = r'60[0|1|3]\d{3}'
SHEN_A_RE = r'000\d{3}'
ZHONGXIAO_RE = r'002\d{3}'

STOCK_SYMBOL_RE = r'http://quote.eastmoney.com/(.*).html'

STOCK_TABLES = [CHUANGYE_RE, HU_A, SHEN_A_RE, ZHONGXIAO_RE]


def check_stock(stock):
    match_obj = re.match(r'(.*)\((.*)\).*', stock, re.M | re.I)
    if match_obj:
        name = match_obj.group(1)
        code = match_obj.group(2)
        for re_str in STOCK_TABLES:
            if re.match(re_str, code):
                return name, code
    return None, None


if __name__ == '__main__':
    url = "http://quote.eastmoney.com/stocklist.html"
    page = requests.session().get(url, headers=HTTP_HEADER, timeout=TIME_OUT)
    content = page.content.decode('gbk').encode('utf-8')
    contentSoup = BeautifulSoup(content, 'html.parser')
    all_tags = contentSoup.find_all('a', {'target': '_blank'})
    save_file = open('stocks.txt', 'w')

    for tag in all_tags:
        if tag.string is not None:
            href = tag.get("href")
            name, code = check_stock(tag.string)
            if code:
                symbol = re.match(STOCK_SYMBOL_RE, href, re.M | re.I).group(1).upper()
                save_file.write(name + ":" + symbol + "\n")

    save_file.close()
