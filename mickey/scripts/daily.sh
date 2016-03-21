#!/bin/bash
TODAY=`date +"%Y%m%d"`
URL="http://www.dbpower.com.hk/ch/news/mmi"
wget -q ${URL} -O ~/powerticker/data/${TODAY}.html
