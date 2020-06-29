#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File Name:
Author: wudi
Mail: programmerwudi@gmail.com
Created Time: 2020-06-29 01:15:34
"""


import gzip
import json
import pprint
import zlib    #压缩相关的库
import hashlib
import threading
import re

import time
import websocket
import redis

pool = redis.ConnectionPool(host='localhost', port=6379)
r = redis.Redis(connection_pool=pool)



#发送心跳数据
def sendHeartBeat(ws):
    ping = 'ping'
    while(True):
        time.sleep(30) #每隔30秒交易所服务器发送心跳信息
        sent = False
        while(sent is False): #如果发送心跳包时出现错误，则再次发送直到 发送成功为止
            try:
                ws.send(ping)
                sent = True
                print("Ping sent.")
            except Exception as e:
                print(e)


def send_message(ws, message_dict):
    data = json.dumps(message_dict).encode()
    #print("Sending Message:")
    #pprint.pprint(message_dict)
    ws.send(data)

def on_message(ws, message):
    data = json.loads(message)
    try:
        if "table" in data:
            if "trade" == data['table']:
                data_first = data['data'][0]
                symbol = data_first["symbol"]
                price = data_first["price"]
                side = data_first["side"]
                time = data_first["timestamp"]
                volume = data_first["size"]
                attr_dict = {
                        "symbol": symbol,
                        "price": price,
                        "side": side,
                        "timestamp": time,
                        }
                key = exchange + "-" + "trade" + "-" + symbol
                r.hmset(key, attr_dict)

            elif data['table'] == "funding":
                data_first = data['data'][0]
                symbol = data_first["symbol"]
                time = data_first["timestamp"]
                fundingRate = data_first["fundingRate"]
                attr_dict = {
                        "symbol": symbol,
                        "timestamp": time,
                        "fundingRate": fundingRate,
                        }
                key = exchange + "-" + "funding" + "-" + symbol
                r.hmset(key, attr_dict)

            elif ("instrument" == data['table']) and ("indicativeFundingRate" in data["data"][0]):

                data_first = data['data'][0]
                symbol = data_first["symbol"]
                time = data_first["timestamp"]
                indicativeFundingRate = data_first["indicativeFundingRate"]
                attr_dict = {
                        "symbol": symbol,
                        "timestamp": time,
                        "indicativeFundingRate": indicativeFundingRate
                        }
                key = exchange + "-" + "indicativeFundingRate" + "-" + symbol
                r.hmset(key, attr_dict)


    except Exception as e:
        print("error: %s" % e)

def formatTradeData(trade):
    return {
            "channel": trade["e"],
            "timestamp": trade["E"],
            "price": trade["p"],
            "size": trade["q"],
            "side": 'sell' if trade["m"] else 'buy',
            "symbol": trade['s']
            }

def formatMarketPrice(trade):
    return {
            "channel": trade['e'],
            "timestamp": trade['E'],
            "price": trade['p'], # 标记价格
            "funding": trade['r'], # 资金费率
            "fundingTime": trade['T'], # 资金费率
            "symbol": trade['s']
            }



def on_error(ws, error):
    print("Error: " + str(error))
    error = gzip.decompress(error).decode()
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    def run(*args):
        data = {"op": "subscribe", "args": ["trade:XBTUSD", "funding:XBTUSD", "funding:ETHUSD", "instrument"]}
        send_message(ws, data)
        #ws.close()
        print("thread terminating...")

    t = threading.Thread(target=run, args=())
    t.start()


if __name__ == "__main__":
    # websocket.enableTrace(True)
    exchange = "bitmex"
    ws = websocket.WebSocketApp(
        'wss://www.bitmex.com/realtime',
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()

