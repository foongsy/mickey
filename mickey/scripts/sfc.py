#!/usr/bin/env python
# coding=UTF-8
import os, io, sys, datetime, codecs, requests, re, csv
from dateutil.relativedelta import *
from mickey.models import WeeklyShortSell, Base

def grab_sfcshortsell(sess,numofweeks=1):
    url = 'http://www.sfc.hk/web/EN/pdf/spr/%s/%s/%s/Short_Position_Reporting_Aggregated_Data_%s.csv'
    today = datetime.date.today()
    # get last Friday's data
    lastfri = today + relativedelta(weekday=FR(-1*numofweeks))
    recordcount = sess.query(WeeklyShortSell).filter(WeeklyShortSell.date == lastfri).count()
    if(recordcount>1):
        print "data already exists"
        return False
    csvurl = url % (lastfri.strftime('%Y'), lastfri.strftime('%m'), lastfri.strftime('%d'), lastfri.strftime('%Y%m%d'))
    print "getting "+csvurl
    csvfile = requests.get(csvurl)
    if csvfile.status_code == 200:
        csvpt = csvfile.iter_lines()
        c = csv.reader(csvpt)
        for r in c:
            if r[0] != 'Date':
                wss = WeeklyShortSell()
                wss.date = lastfri
                wss.ticker = '{:0>5}'.format(r[1])
                wss.volume = int(r[3])
                wss.turnover = int(r[4])
                sess.add(wss)
        sess.commit()
    else:
        print "error getting csv file"
