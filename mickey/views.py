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
    todaytop = s.query(DailyRecord).filter(DailyRecord.buysell_ratio > 0.5, DailyRecord.turnover >= 3000000, DailyRecord.date == last_updated).all()
    return render_template('dashboard.html',todaytop=todaytop,last_updated=last_updated)

@app.route('/custom', methods=['GET','POST'])
def custom():
    last_updated = s.query(DailyRecord).order_by(DailyRecord.date.desc()).first().date
    form = CustomSearch(request.form)
    if form.validate_on_submit():
        # Asks for single day data
        if form.days.data == 1:
            buysell_ratio = form.buysellratio_threshold.data / 100.0
            turnover = form.turnover_threshold.data * 1000000
            tabledata = s.query(DailyRecord).filter(DailyRecord.buysell_ratio > buysell_ratio, DailyRecord.turnover >= turnover, DailyRecord.date == last_updated).all()
            multipledays=False
            return render_template('custom.html',form=form,multipledays=multipledays,tabledata=tabledata,last_updated=last_updated)
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
                DailyRecord.name,DailyRecord.ticker,
                func.sum(DailyRecord.volume).label("total_volume"),
                func.sum(DailyRecord.turnover).label("total_turnover"),
                func.sum(DailyRecord.buy_turnover).label("total_buyturnover"),
                func.sum(DailyRecord.sell_turnover).label("total_sellturnover")).filter(
                DailyRecord.date.between(dates[len(dates)-1],dates[0])).group_by(
                DailyRecord.ticker).having(
                '(total_buyturnover*1.0 / total_turnover*1.0) >= %f' % buysell_ratio).having(
                'total_turnover >= %d*%d' % (numofdays,turnover)
            )
            tabledata = q.all()
            multipledays=True
            return render_template('custom.html',form=form,multipledays=multipledays,tabledata=tabledata,last_updated=last_updated,numofdays=numofdays,turnover=turnover,buysell_ratio=buysell_ratio)
    else:
        for e in form.errors:
            print "FORM:" + e
        for e in form.days.errors:
            print "days:" + e
        for e in form.turnover_threshold.errors:
            print "turnover_threshold: "+e
        for e in form.buysellratio_threshold.errors:
            print "buysellratio_threshold: "+e
        return render_template('custom.html',form=form,last_updated=last_updated)
