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
    ping = '{"event":"ping"}'
    while(True):
        time.sleep(30) #每隔30秒交易所服务器发送心跳信息
        sent = False
        while(sent is False): #如果发送心跳包时出现错误，则再次发送直到
            发送成功为止
            try:
                ws.send(ping)
                sent = True
                print("Ping sent.")
            except Exception as e:
                print(e)

#解压函数
def inflate(data):
    decompress = zlib.decompressobj(-zlib.MAX_WBITS)
    inflated = decompress.decompress(data)
    inflated += decompress.flush()
    return inflated

def send_message(ws, message_dict):
    data = json.dumps(message_dict).encode()
    #print("Sending Message:")
    #pprint.pprint(message_dict)
    ws.send(data)

def on_message(ws, message):
    d = json.loads(message)
    try:
        if "aggTrade" ==  d["e"]:
            data = formatTradeData(json.loads(message))
            symbol = data["symbol"]
            ch = data["channel"]
            key = exchange + "-" + ch + "-" + symbol
            r.hmset(key, data)

        if "markPriceUpdate" ==  d["e"]:
            print(message)
            data = formatMarketPrice(json.loads(message))
            print(data)
            symbol = data["symbol"]
            ch = data["channel"]
            print(message)
            key = exchange + "-" + ch + "-" + symbol
            r.hmset(key, data)

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

        data = {
                "method": "SUBSCRIBE",
                "params":
                [
                    "btcusdt@aggTrade",
                    "batusdt@aggTrade",
                    "btcusdt@markPrice",
                    "batusdt@markPrice",
                    "adausdt@markPrice",
                    ],
                "id": 1
                }
        send_message(ws, data)
        #ws.close()
        print("thread terminating...")

    t = threading.Thread(target=run, args=())
    t.start()


if __name__ == "__main__":
    # websocket.enableTrace(True)
    exchange = "binancef"
    ws = websocket.WebSocketApp(
        #'wss://fstream.binance.com:9443/ws',
        'wss://fstream.binance.com/ws',
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()

