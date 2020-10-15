#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File Name:
Author: wudi
Mail: programmerwudi@gmail.com
Created Time: 2020-10-15 21:53:30
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
    #unzipped_data = gzip.decompress(message).decode()
    msg_dict = json.loads(message)

    #print("Recieved Message: ")
    #pprint.pprint(msg_dict)

    #print(msg_dict)
    # write redis
   # exchange = "coinlist"
    if "ticker" in msg_dict["channel"]:
        #info = msg_dict["tick"]
        d = msg_dict["data"]
        print(d)
        quto = d["quote"]
        symbol = d["symbol"]
        
        #print(re.split('\.',msg_dict["ch"])[1])
        #print( d["price"])
        attr_dict = {
                "symbol": symbol,
                "ask": quto["ask"],
                "ask_size": quto["ask_size"],
                "bid": quto["bid"],
                "bid_size": quto["bid_size"],
                "timestamp": d["logical_time"],
                }
        key = "coinlist" + "-" + msg_dict["channel"]+  "-" + symbol
        r.hmset(key, attr_dict)



def on_error(ws, error):
    print("Error: " + str(error))
    error = (error)
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    def run(*args):

        data = {
                "type": "subscribe",
                "symbols": ["FIL-USD"],
                "channels": ["ticker"]
                }
        send_message(ws, data)
        #ws.close()
        print("thread terminating...")

    t = threading.Thread(target=run, args=())
    t.start()


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        "wss://trade-api.coinlist.co",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()

