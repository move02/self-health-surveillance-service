from datetime import datetime
from sqlalchemy import ForeignKey
import time
from app import db, bcrypt
from sqlalchemy import inspect

#db t_user_info_m01
class userInfo(db.Model):
    __tablename__ = 't_user_info_m01'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    sn = db.Column('SN', db.Integer, primary_key=True, nullable=False, autoincrement=True)
    resideArea = db.Column('RESIDE_AREA', db.String(10))
    sexdstn = db.Column('SEXDSTN', db.String(1))
    telno = db.Column('TELNO', db.String(15))
    password = db.Column('PASSWORD', db.String(255))
    deleteAt = db.Column('DELETE_AT', db.String(1))
    email = db.Column('EMAIL', db.String(50))
    agrde = db.Column('AGRDE', db.String(10))
    registDate = db.Column('REGIST_DATE', db.DateTime, default=datetime.now())

    schedules = db.relationship("userSchdul", backref="user", lazy=True)

    def __init__(self, resideArea=None, sexdstn=None, telno=None, password=None, deleteAt=None, email=None, agrde=None):
        self.resideArea = resideArea
        self.sexdstn = sexdstn
        self.telno = telno
        self.password = password
        self.deleteAt = deleteAt
        self.email = email
        self.agrde = agrde

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password, 10).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

#db t_user_schdul_m01
class userSchdul(db.Model):
    __tablename__ = 't_user_schdul_m01'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    sn = db.Column('SN', db.Integer, primary_key=True, nullable=False, autoincrement=True)
    userSn = db.Column('USER_SN', db.Integer, ForeignKey(userInfo.sn), nullable=False)
    stdde = db.Column('STDDE', db.DateTime, default=datetime.fromtimestamp(time.time()))
    registDate = db.Column('REGIST_DATE', db.DateTime, default=datetime.now())

    locations = db.relationship("userLocation", backref="schedule", lazy=True)

    def __init__(self, userSn=None, stdde=None):
        self.userSn = userSn
        self.stdde = stdde

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }


#db t_user_location_d01
class userLocation(db.Model):
    __tablename__ = 't_user_location_d01'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    sn = db.Column('SN', db.Integer, primary_key=True, nullable=False, autoincrement=True)
    schdulSn = db.Column('SCHDUL_SN', db.Integer, ForeignKey(userSchdul.sn))
    deOrdr = db.Column('DE_ORDR', db.Integer)
    visitTime = db.Column('VISIT_TIME', db.String(5))
    visitDate = db.Column('VISIT_DATE', db.DateTime)
    placeId = db.Column('PLACE_ID', db.String(20))
    coursOrdr = db.Column('COURS_ORDR', db.Integer)
    registDate = db.Column('REGIST_DATE', db.DateTime, default=datetime.now())

    def __init__(self, schdulSn, deOrdr, visitTime, visitDate, placeId, coursOrdr):
        self.schdulSn = schdulSn
        self.deOrdr = deOrdr
        self.visitTime = visitTime
        self.visitDate = visitDate
        self.placeId = placeId
        self.coursOrdr = coursOrdr

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }