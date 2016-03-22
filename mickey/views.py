from mickey import app
from flask import render_template, request
from flask_wtf import Form
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from mickey.models import DailyRecord
from wtforms import SelectField, IntegerField, validators
from wtforms.validators import DataRequired, NumberRange

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
    days = SelectField(u'How many days back?',choices=[(1,'1'),(3,'3'),(5,'5'),(10,'10')],validators=[DataRequired()])
    turnover_threshold = IntegerField('Minimum Turnover',validators=[DataRequired(),NumberRange(min=0,max=100,message='Must be between 0 and 100')])
    buysellratio_threshold = IntegerField('Minimum Buy/Sell Ratio',validators=[DataRequired(),NumberRange(min=0,max=100,message='Must be between 0 and 100')])

@app.route('/')
def index():
    last_updated = s.query(DailyRecord).order_by(DailyRecord.date.desc()).first().date
    todaytop = s.query(DailyRecord).filter(DailyRecord.buysell_ratio > 0.5, DailyRecord.turnover >= 3000000, DailyRecord.date == last_updated).all()
    return render_template('dashboard.html',todaytop=todaytop,last_updated=last_updated)

@app.route('/custom', methods=('GET','POST'))
def custom():
    form = CustomSearch(csrf_enabled=False)
    if form.validate_on_submit():
        posted = True
    else:
        posted = False
    return render_template('custom.html',form=form,posted=posted)
