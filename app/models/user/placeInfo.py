from datetime import datetime
import time
from app import db
from sqlalchemy import inspect

#db t_search_kwrd_h01
class searchKeword(db.Model):
    __tablename__ = 't_search_kwrd_h01'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    sn = db.Column('SN', db.Integer, primary_key=True, nullable=False, autoincrement=True)
    searchTy = db.Column('SEARCH_TY', db.String(10))
    searchKwrd = db.Column('SEARCH_KWRD', db.String(100))
    registDate = db.Column('REGIST_DATE', db.DateTime, default=datetime.now(), nullable=False)

    def __init__(self, searchTy=None, searchKwrd=None):
        self.searchTy = searchTy
        self.searchKwrd = searchKwrd

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

#db t_pick_place_h01
class pickPlace(db.Model):
    __tablename__ = 't_pick_place_h01'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    sn = db.Column('SN', db.Integer, primary_key=True, nullable=False, autoincrement=True)
    placeId = db.Column('PLACE_ID', db.String(20))
    placeNm = db.Column('PLACE_NM', db.String(100))
    placeAdres = db.Column('PLACE_ADRES', db.String(500))
    placeRnAdres = db.Column('PLACE_RN_ADRES', db.String(500))
    la = db.Column('LA', db.String(30))
    lo = db.Column('LO', db.String(30))
    placeCtprvn = db.Column('PLACE_CTPRVN', db.String(10))
    placeSigngu = db.Column('PLACE_SIGNGU', db.String(20))
    registDate = db.Column('REGIST_DATE', db.DateTime, default=datetime.now(), nullable=False)

    def __init__(self, placeId=None, placeNm=None, placeAdres=None, placeRnAdres=None, la=None, lo=None, placeCtprvn=None, placeSigngu=None):
        self.placeId = placeId
        self.placeNm = placeNm
        self.placeAdres = placeAdres
        self.placeRnAdres = placeRnAdres
        self.placeCtprvn = placeCtprvn
        self.placeSigngu = placeSigngu
        self.la = la
        self.lo = lo

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

#db t_place_info_m01
class placeInfo(db.Model):
    __tablename__ = 't_place_info_m01'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    placeId = db.Column('PLACE_ID', db.String(20), primary_key=True, nullable=False)
    placeNm = db.Column('PLACE_NM', db.String(100))
    placeAdres = db.Column('PLACE_ADRES', db.String(500))
    placeRnAdres = db.Column('PLACE_RN_ADRES', db.String(500))
    la = db.Column('LA', db.String(30))
    lo = db.Column('LO', db.String(30))
    placeCtprvn = db.Column('PLACE_CTPRVN', db.String(10))
    placeSigngu = db.Column('PLACE_SIGNGU', db.String(20))
    registDate = db.Column('REGIST_DATE', db.DateTime, default=datetime.now(), nullable=False)

    def __init__(self, placeId=None, placeNm=None, placeAdres=None, placeRnAdres=None, la=None, lo=None, placeCtprvn=None, placeSigngu=None):
        self.placeId = placeId
        self.placeNm = placeNm
        self.placeAdres = placeAdres
        self.placeRnAdres = placeRnAdres
        self.placeCtprvn = placeCtprvn
        self.placeSigngu = placeSigngu
        self.la = la
        self.lo = lo

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }