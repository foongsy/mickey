#from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Unicode, DateTime, Float
Base = declarative_base()

class DailyRecord(Base):
    __tablename__ = 'dailyrecord'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    ticker = Column(String(6), nullable=False)
    name = Column(Unicode(64), nullable=False)
    volume = Column(Integer, nullable=False)
    turnover = Column(Integer, nullable=False)
    buy_volume = Column(Integer, nullable=False)
    buy_turnover = Column(Integer, nullable=False)
    sell_volume = Column(Integer, nullable=False)
    sell_turnover = Column(Integer, nullable=False)
    spec_volume = Column(Integer, nullable=False)
    spec_turnover = Column(Integer, nullable=False)
    buysell_ratio = Column(Float, nullable=True)

class WeeklyShortSell(Base):
    __tablename__ = 'weeklyshortsell'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    ticker = Column(String(6), nullable=False)
    volume = Column(Integer, nullable=False)
    turnover = Column(Integer, nullable=False)

class UpdateLog(Base):
    __tablename__ = 'updatelog'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    last_updated = Column(DateTime, nullable=False)
    record_updated = Column(Integer, nullable=False)

class StockIndex(Base):
    __tablename__ = 'stockindex'
    id = Column(Integer, primary_key=True)
    ticker = Column(String(6), nullable=False)
    name = Column(Unicode(64),nullable=False)
    last_updated = Column(DateTime, nullable=False)
