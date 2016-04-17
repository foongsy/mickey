import os, io, sys, datetime, codecs, requests, re, datetime
from mickey import app
from mickey import models
from mickey.scripts.sfc import grab_sfcshortsell
from mickey.models import WeeklyShortSell, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

if __name__ == '__main__':
    app.config.from_object('config')
    engine = create_engine(app.config['DATABASE'])
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    _Session = sessionmaker(bind=engine)
    Session = _Session()
    for i in range(2,54):
        grab_sfcshortsell(Session,i)
