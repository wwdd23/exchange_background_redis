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
import threading
import re

import time
import websocket
import redis

pool = redis.ConnectionPool(host='localhost', port=6379)
r = redis.Redis(connection_pool=pool)

def send_message(ws, message_dict):
    data = json.dumps(message_dict).encode()
    #print("Sending Message:")
    #pprint.pprint(message_dict)
    ws.send(data)


def on_message(ws, message):
    unzipped_data = gzip.decompress(message).decode()
    msg_dict = json.loads(unzipped_data)
    # print("Recieved Message: ")
    # pprint.pprint(msg_dict)
    print(msg_dict)
    # write redis
    exchange = "huobi"
    if "tick" in msg_dict:
        info = msg_dict["tick"]
        d = info["data"][0]
        #print(re.split('\.',msg_dict["ch"])[1])
        #print( d["price"])
        symbol = re.split('\.',msg_dict["ch"])[1]
        channel = re.split('\.',msg_dict["ch"])[2]
        attr_dict = {
                "symbol": symbol,
                "price": d["price"],
                "side": d["direction"],
                "timestamp": info["ts"],
                }
        key = exchange + "-" + channel +  "-" + symbol
        r.hmset(key, attr_dict)

    if 'ping' in msg_dict:
        data = {
            "pong": msg_dict['ping']
        }
        send_message(ws, data)


def on_error(ws, error):
    print("Error: " + str(error))
    error = gzip.decompress(error).decode()
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    def run(*args):

        data ={
                "sub": "market.btcusdt.trade.detail",
                "id": "id3"
                }
        send_message(ws, data)
        #ws.close()
        print("thread terminating...")

    t = threading.Thread(target=run, args=())
    t.start()


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        "wss://api.huobi.pro/ws",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()

