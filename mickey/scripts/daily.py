#!/usr/bin/env python
# coding=UTF-8
import os, io, sys, datetime, codecs, requests, re
from lxml import html
from mickey.models import DailyRecord, Base
from sqlalchemy import func

def grab_dbpower(sess,datafile=''):
    if(os.path.isfile(datafile)):
        f = open(datafile,'r')
        tree = html.fromstring(f.read())
        f.close()
        table_xpath = '//*[@id="column_left"]/article/div/div[1]/table/tbody'
        table = tree.xpath(table_xpath)
    else:
        url = "http://www.dbpower.com.hk/ch/news/mmi"
        page = requests.get(url)
        tree = html.fromstring(page.content)
        table_xpath = '//*[@id="column_left"]/article/div/div[1]/table/tbody'
        table = tree.xpath(table_xpath)
    date_xpath = '//*[@id="column_left"]/article/div/div[2]/div/text()'
    last_updated = re.sub('^[^0-9]+','',tree.xpath(date_xpath).pop())
    last_updated = datetime.datetime.strptime(last_updated,"%Y-%m-%d %H:%M")
    # Get if the data date is already in database
    recordcount = sess.query(DailyRecord).filter(DailyRecord.date == last_updated.date()).count()
    if(recordcount>1):
        return False
    else:
        for i in range(1,len(table[0])+1):
            dr = DailyRecord()
            dr.date = last_updated.date()
            dr.ticker = tree.xpath('//*[@id="column_left"]/article/div/div[1]/table/tbody/tr[%d]/td[1]/a/text()' % i).pop()
            dr_name = tree.xpath('//*[@id="column_left"]/article/div/div[1]/table/tbody/tr[%d]/td[2]/text()' % i)
            if(len(dr_name)>0):
                dr.name = dr_name.pop()
            else:
                dr.name = ''
            dr.volume = int(float(tree.xpath('//*[@id="column_left"]/article/div/div[1]/table/tbody/tr[%d]/td[3]/text()' % i).pop())*1000000)
            dr.turnover = int(float(tree.xpath('//*[@id="column_left"]/article/div/div[1]/table/tbody/tr[%d]/td[4]/text()' % i).pop())*1000000)
            dr.buy_volume = int(float(tree.xpath('//*[@id="column_left"]/article/div/div[1]/table/tbody/tr[%d]/td[5]/text()' % i).pop())*1000000)
            dr.buy_turnover = int(float(tree.xpath('//*[@id="column_left"]/article/div/div[1]/table/tbody/tr[%d]/td[6]/text()' % i).pop())*1000000)
            dr.sell_volume = int(float(tree.xpath('//*[@id="column_left"]/article/div/div[1]/table/tbody/tr[%d]/td[7]/text()' % i).pop())*1000000)
            dr.sell_turnover = int(float(tree.xpath('//*[@id="column_left"]/article/div/div[1]/table/tbody/tr[%d]/td[8]/text()' % i).pop())*1000000)
            dr.spec_volume = int(float(tree.xpath('//*[@id="column_left"]/article/div/div[1]/table/tbody/tr[%d]/td[9]/text()' % i).pop())*1000000)
            dr.spec_turnover = int(float(tree.xpath('//*[@id="column_left"]/article/div/div[1]/table/tbody/tr[%d]/td[10]/text()' % i).pop())*1000000)
            if(dr.buy_turnover > 0 or dr.sell_turnover > 0):
                dr.buysell_ratio = dr.buy_turnover*1.0 / (dr.buy_turnover*1.0 + dr.sell_turnover*1.0)
            sess.add(dr)
        sess.commit()
        return True
