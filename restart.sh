#!/bin/bash
###################
# Author:  wudi
# Mail: programmerwudi@gmail.com 
# Description: 
# Created Time: 2020-07-06 00:58:00
###################


file_path=`dirname $0`
echo $file_path
echo "show pid:"
ps aux | grep -ie python | grep -E 'okex|huobi|binance|bitmex' 

echo "git pull start..."

cd $file_path
git pull;


echo "kill ws pid"
ps aux | grep -ie python | grep -E 'okex|huobi|binance|bitmex' |awk '{print  $2}' |xargs kill -9

echo "restart ws python script"
python3 $file_path/binance.py > /dev/null 2>&1 &
python3 $file_path/binance-d.py > /dev/null 2>&1 &
python3 $file_path/okex.py > /dev/null 2>&1 &
python3 $file_path/bitmex.py > /dev/null 2>&1 &
python3 $file_path/huobi.py > /dev/null 2>&1 &

echo "restart ws end"
