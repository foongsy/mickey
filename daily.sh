#!/bin/bash
TODAY=`date +"%Y%m%d"`
URL="http://www.dbpower.com.hk/ch/news/mmi"
# Modify this to suit your path
MICKEY_PATH="/home/user/projects/mickey"
# Modify this to suit your virtualenv/conda
VENV_PATH="/home/user/.virtualenvs/mickey/bin"
wget -q ${URL} -O ${MICKEY_PATH}/mickey/powerticker/${TODAY}.html
cd ${MICKEY_PATH}  
${VENV_PATH}/python ${MICKEY_PATH}/dailyscript.py
