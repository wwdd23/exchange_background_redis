#!/bin/bash
###################
# Author:  wudi
# Mail: programmerwudi@gmail.com 
# Description: 
# Created Time: 2020-06-29 03:42:56
###################

file_path=`dirname $0`
echo $file_path
python3 $file_path/binance.py > /dev/null 2>&1 &
python3 $file_path/binance-d.py > /dev/null 2>&1 &
python3 $file_path/okex.py > /dev/null 2>&1 &
python3 $file_path/bitmex.py > /dev/null 2>&1 &
python3 $file_path/huobi.py > /dev/null 2>&1 &
