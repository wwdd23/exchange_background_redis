#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File Name:
Author: wudi
Mail: programmerwudi@gmail.com
Created Time: 2020-06-28 23:44:54
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
                print("ping error %s" % e)

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
    try:
        inflated = inflate(message).decode('utf-8')  #将okex发来的数据>解压
    except Exception as e:
        print("try message: %s" % e)

    print(inflated)
    if inflated == 'pong': 
        #判断推送来的消息类型：如果是服 务器的心跳
            print("Pong received.")
            return
    try:
        msgs = json.loads(inflated)
        if 'event' in msgs: #判断推送来的消息类型：>如果是订阅成功信息
            print(msgs)
        elif 'table' in msgs:
            table = msgs["table"]
            data = msgs["data"]
            if "trade" in table:
                data_first = data[0]
                symbol = data_first["instrument_id"]
                price = data_first["price"]
                side = data_first["side"]
                time = data_first["timestamp"]
                volume = data_first["size"]
                redis_data = {
                        "timestamp": time,
                        "exchange": exchange,
                        "symbol": symbol,
                        "price": price,
                        "side": side,
                        "volume": volume,
                        }
                key = exchange + "-" + table + "-" + symbol
                r.hmset(key, redis_data)

            elif 'funding' in table:
                data_first = data[0]
                symbol = data_first["instrument_id"]
                estimated_rate = data_first["estimated_rate"]
                funding_rate = data_first["funding_rate"]
                funding_time = data_first["funding_time"]
                interest_rate = data_first["interest_rate"]
                settlement_time = data_first["settlement_time"]
                redis_data = {
                        "timestamp": funding_time,
                        "exchange": exchange,
                        "funding_rate": funding_rate,
                        "funding_time": funding_time,
                        "interest_rate": interest_rate,
                        "settlement_time": settlement_time,
                        }
                key = exchange + "-" + table + "-" + symbol 
                r.hmset(key, redis_data)


    except Exception as e:
        print("error: %s" % e)


def on_error(ws, error):
    print("Error: " + str(error))
    error = gzip.decompress(error).decode()
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    def run(*args):

        data = {"op": "subscribe", "args":  ["swap/trade:BTC-USD-SWAP",  "spot/trade:BTC-USDT",
            "swap/funding_rate:BTC-USD-SWAP", "swap/funding_rate:BTC-USDT-SWAP", "swap/funding_rate:ADA-USD-SWAP", "swap/funding_rate:ADA-USDT-SWAP"]}

        send_message(ws, data)
        #ws.close()
        print("thread terminating...")

    t = threading.Thread(target=run, args=())
    t.start()


if __name__ == "__main__":
    # websocket.enableTrace(True)
    exchange = "okex"
    ws = websocket.WebSocketApp(
        'wss://real.okex.com:8443/ws/v3',
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    threading.Thread(target=sendHeartBeat, args=(ws,)).start() #新建一个线程来发送心跳包
    ws.run_forever()

