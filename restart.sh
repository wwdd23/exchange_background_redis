#!/bin/bash
###################
# Author:  wudi
# Mail: programmerwudi@gmail.com 
# Description: 
# Created Time: 2020-07-06 00:58:00
###################

echo "show pid:"
ps aux | grep -ie python | grep -E 'okex|huobi|binance|bitmex' 

ps aux | grep -ie python | grep -E 'okex|huobi|binance|bitmex' |awk '{print  $2}' |xargs kill -9

python3 binance.py > /dev/null 2>&1 &
python3 okex.py > /dev/null 2>&1 &
python3 bitmex.py > /dev/null 2>&1 &
python3 huobi.py > /dev/null 2>&1 &
