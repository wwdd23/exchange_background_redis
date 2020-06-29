#!/bin/bash
###################
# Author:  wudi
# Mail: programmerwudi@gmail.com 
# Description: 
# Created Time: 2020-06-29 03:42:56
###################

python3 binance.py > /dev/null 2>&1 &
python3 okex.py > /dev/null 2>&1 &
python3 bitmex.py > /dev/null 2>&1 &
python3 huobi.py > /dev/null 2>&1 &
