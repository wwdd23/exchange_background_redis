#!/bin/bash
###################
# Author:  wudi
# Mail: programmerwudi@gmail.com 
# Description: 
# Created Time: 2020-06-29 03:52:07
###################


echo "show pid:"
ps aux | grep -ie python | grep -E 'okex|huobi|binance|bitmex' 

ps aux | grep -ie python | grep -E 'okex|huobi|binance|bitmex' |awk '{print  $2}' |xargs kill -9
