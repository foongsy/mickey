from mickey import app
from mickey import models
import os, io, sys, datetime, codecs, requests, re, datetime
from lxml import html
from mickey.models import DailyRecord, Base, engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base.metadata.bind = engine
_Session = sessionmaker(bind=engine)
Session = _Session()
