from mickey import app
from flask import render_template
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from mickey.models import DailyRecord

# connecting to DATABASE
engine = create_engine(app.config['DATABASE'])
Base = declarative_base()
Base.metadata.bind = engine
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)

@app.route('/')
def index():
    s = session()
    todaytop = s.query(DailyRecord).filter(DailyRecord.buysell_ratio>0.9)
    return render_template('dashboard.html',todaytop=todaytop)
