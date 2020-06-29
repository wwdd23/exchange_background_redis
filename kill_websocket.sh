#!/bin/bash
###################
# Author:  wudi
# Mail: programmerwudi@gmail.com 
# Description: 
# Created Time: 2020-06-29 03:52:07
###################

ps aux | grep -ie python |awk '{print  $2}' |xargs kill -9
