import os, io, sys, datetime, codecs, requests, re, datetime
from mickey import app
from mickey import models
from mickey.scripts.daily import grab_dbpower
from mickey.models import DailyRecord, Base
from lxml import html
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

if __name__ == '__main__':
    app.config.from_object('config')
    engine = create_engine(app.config['DATABASE'])
    Base.metadata.bind = engine
    _Session = sessionmaker(bind=engine)
    Session = _Session()
    if(len(sys.argv) > 1):
        datafile = sys.argv.pop()
        if os.path.isfile(datafile):
            print("Working with datafile %s" % datafile)
            grab_dbpower(Session,datafile)
        else:
            print("Working WITHOUT datafile %s" % datafile)
            grab_dbpower(Session)
    else:
        print("Working with URL")
        grab_dbpower(Session)
