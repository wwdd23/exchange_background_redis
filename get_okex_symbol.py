#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File Name:
Author: wudi
Mail: programmerwudi@gmail.com
Created Time: 2020-10-15 10:32:24
"""

import requests
import random
import hashlib
import json



host = "https://www.okex.com"
spot_path = "/api/spot/v3/instruments"
swap_path = "/api/swap/v3/instruments"
futures_path = "/api/futures/v3/instruments"

spot_url = host + spot_path
spot_res = requests.get(spot_url)
spot_data = json.loads(spot_res.text)

swap_url = host + swap_path
swap_res = requests.get(swap_url)
swap_data = json.loads(swap_res.text)

futures_url = host + futures_path
futures_res = requests.get(futures_url)
futures_data = json.loads(futures_res.text)
spot_trade = []
swap_trade = []
futures_trade = []
funding_list = []
# 获取spot trade list 
for i in spot_data:
    print(i["instrument_id"])
    spot_trade.append( ("spot/trade:" + i["instrument_id"]))
# 获取swap trade list 
for i in swap_data:
    print(i["instrument_id"])
    swap_trade.append( ("swap/trade:" + i["instrument_id"]))
for i in futures_data:
    print(i["instrument_id"])
    futures_trade.append( ("future/trade:" + i["instrument_id"]))
for i in swap_data:
    print(i["instrument_id"])
    funding_list.append( ("swap/funding_rate:" + i["instrument_id"]))



# 火币交易对信息

host="https://api-aws.huobi.pro"
path = "/v1/common/currencys"
huobi_url = host + path
huobi_res = requests.get(huobi_url)
huobi_data = json.loads(huobi_res.text)


url = "https://api.huobi.pro/market/tickers"



huobi_res = requests.get(url)
