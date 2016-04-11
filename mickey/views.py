from mickey import app
from flask import render_template, request
from flask_wtf import Form
from sqlalchemy import create_engine
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects import sqlite
from mickey.models import DailyRecord
from wtforms import SelectField, IntegerField, validators
from wtforms.validators import DataRequired, NumberRange
from datetime import date
import datetime

app.secret_key = "hafamily"

# connecting to DATABASE
engine = create_engine(app.config['DATABASE'])
Base = declarative_base()
Base.metadata.bind = engine
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)
s = session()

# Form for custom search
class CustomSearch(Form):
    days = SelectField(u'How many days back?',coerce=int,
        validators=[DataRequired('Days cannot be empty')],
        choices=[(1,'1'),(3,'3'),(5,'5'),(10,'10')]
    )
    turnover_threshold = IntegerField('Minimum Turnover',
        validators=[NumberRange(min=0,message=u'Cannot be empty or negative')]
    )
    buysellratio_threshold = IntegerField('Minimum Buy/Sell Ratio',
        validators=[NumberRange(min=0,max=100,message=u'Must be between 0 and 100')]
    )

@app.route('/')
def index():
    last_updated = s.query(DailyRecord).order_by(DailyRecord.date.desc()).first().date
    pt_table = s.query(DailyRecord).filter(DailyRecord.buysell_ratio > 0.5, DailyRecord.turnover >= 3000000, DailyRecord.date == last_updated).all()
    return render_template('index.html',request=request,pt_table=pt_table,last_updated=last_updated)

@app.route('/t/<ticker>')
def t(ticker):
    last_updated = s.query(DailyRecord).order_by(DailyRecord.date.desc()).first().date
    tickername = s.query(DailyRecord.name).filter(DailyRecord.ticker==ticker).order_by(DailyRecord.date.desc()).first()
    predates = s.query(DailyRecord.date).distinct(DailyRecord.date.name).order_by(DailyRecord.date.desc()).limit(10).all()
    dates=[]
    for row in predates:
        dates.append(row.date)
    pretickerinfo = s.query(DailyRecord).filter(DailyRecord.ticker==ticker,DailyRecord.date.between(dates[len(dates)-1],dates[0])).all()
    tickerinfo = {'date': [], 'buy_turnover': [], 'turnover': []}
    for ti in pretickerinfo:
        tickerinfo['date'].append(ti.date)
        tickerinfo['buy_turnover'].append(ti.buy_turnover)
        tickerinfo['turnover'].append(ti.turnover - ti.buy_turnover)
    return render_template('ticker.html',request=request,last_updated=last_updated,ticker=ticker,tickerinfo=tickerinfo,tickername=tickername,dates=dates)

@app.route('/custom', methods=['GET','POST'])
def custom():
    last_updated = s.query(DailyRecord).order_by(DailyRecord.date.desc()).first().date
    form = CustomSearch(request.form)
    if form.validate_on_submit():
        # Asks for single day data
        if form.days.data == 1:
            buysell_ratio = form.buysellratio_threshold.data / 100.0
            turnover = form.turnover_threshold.data * 1000000
            pt_table = s.query(DailyRecord).filter(DailyRecord.buysell_ratio > buysell_ratio, DailyRecord.turnover >= turnover, DailyRecord.date == last_updated).all()
            multipledays=False
            return render_template('custom.html',request=request,form=form,multipledays=multipledays,pt_table=pt_table,last_updated=last_updated)
        # Asks for multiple days data
        elif form.days.data > 1:
            numofdays = form.days.data
            predates = s.query(DailyRecord.date).distinct(DailyRecord.date.name).order_by(DailyRecord.date.desc()).limit(numofdays).all()
            dates=[]
            for row in predates:
                dates.append(row.date)
            buysell_ratio = form.buysellratio_threshold.data / 100.0
            turnover = form.turnover_threshold.data * 1000000
            q = s.query(
                DailyRecord.ticker,DailyRecord.name,DailyRecord.ticker,DailyRecord.buysell_ratio,
                func.sum(DailyRecord.volume).label("total_volume"),
                func.sum(DailyRecord.turnover).label("total_turnover"),
                func.sum(DailyRecord.buy_volume).label("total_buyvolume"),
                func.sum(DailyRecord.buy_turnover).label("total_buyturnover"),
                func.sum(DailyRecord.sell_volume).label("total_sellvolume"),
                func.sum(DailyRecord.sell_turnover).label("total_sellturnover")).filter(
                DailyRecord.date.between(dates[len(dates)-1],dates[0])).group_by(
                DailyRecord.ticker).having(
                '(total_buyturnover*1.0 / total_turnover*1.0) >= %f' % buysell_ratio).having(
                'total_turnover >= %d*%d' % (numofdays,turnover)
            )
            pt_table = q.all()
            multipledays=True
            return render_template('custom.html',request=request,form=form,multipledays=multipledays,pt_table=pt_table,last_updated=last_updated,numofdays=numofdays,turnover=turnover,buysell_ratio=buysell_ratio)
    else:
        for e in form.errors:
            print "FORM:" + e
        for e in form.days.errors:
            print "days:" + e
        for e in form.turnover_threshold.errors:
            print "turnover_threshold: "+e
        for e in form.buysellratio_threshold.errors:
            print "buysellratio_threshold: "+e
        return render_template('custom.html',request=request,form=form,last_updated=last_updated)

@app.route('/export')
def export():
    last_updated = s.query(DailyRecord).order_by(DailyRecord.date.desc()).first().date
    predates = s.query(DailyRecord.date).distinct(DailyRecord.date.name).order_by(DailyRecord.date.desc()).limit(10).all()
    dates=[]
    for row in predates:
        dates.append(row.date)
        results = s.query(
            DailyRecord.name,DailyRecord.ticker,DailyRecord.date,DailyRecord.buysell_ratio).filter(
            DailyRecord.date.between(dates[len(dates)-1],dates[0]),DailyRecord.buysell_ratio != None).all()
    pt_table = {}
    namelist = {}
    for r in results:
        #print "%s %s %s %s" % (r.ticker, r.name, r.date, r.buysell_ratio)
        if r.ticker in pt_table:
            pt_table[r.ticker].update({r.date:r.buysell_ratio*100})
        else:
            pt_table[r.ticker] = {r.date:r.buysell_ratio*100}
            namelist[r.ticker] = r.name
    return render_template('export.html',request=request,dates=dates,namelist=namelist,last_updated=last_updated,pt_table=pt_table)
