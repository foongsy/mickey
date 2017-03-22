#!/bin/bash
TODAY=`date +"%Y%m%d"`
URL="http://www.dbpower.com.hk/ch/news/mmi"
wget -q ${URL} -O /home/sim/Bench/mickey/powerticker/${TODAY}.html
cd /home/sim/Bench/mickey
/home/sim/.virtualenvs/mickey/bin/python /home/sim/Bench/mickey/dailyscript.py
