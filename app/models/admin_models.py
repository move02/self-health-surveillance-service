from datetime import datetime, timedelta
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, url_for
from app import db
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin

class Administrator(db.Model, SerializerMixin, UserMixin):
    __tablename__="T_ADMIN_INFO_M01"
    __table_args__={'mysql_collate': 'utf8_general_ci'}

    serialize_rules = ('-password_hash')

    sn = db.Column("SN", db.Integer, primary_key=True, autoincrement=True)
    username = db.Column("ID", db.String(30), index=True, unique=True, nullable=False)
    realname = db.Column("NM", db.String(100), index=True, nullable=False)
    password_hash = db.Column("PASSWORD", db.String(255), nullable=False)
    tel = db.Column("TELNO", db.String(15))
    is_confirmed = db.Column("CONFM_AT", db.Boolean, nullable=False, default=False)
    confirmed_user = db.Column("CONFM_ID", db.String(30))
    confirmed_date = db.Column("CONFM_DATE", db.DateTime)
    registered_date = db.Column("REGIST_DATE", db.DateTime, server_default=db.func.now())
    updated_id = db.Column("UPDT_ID", db.String(30))
    updated_date = db.Column("UPDT_DATE", db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    is_deleted = db.Column("DELETE_AT", db.Boolean, nullable=False, default=False)
    deleted_user = db.Column("DELETE_ID", db.String(30))
    deleted_date = db.Column("DELETE_DATE", db.DateTime)
    last_login = db.Column("LAST_LOGIN", db.DateTime)
    authority = db.Column("AUTHOR", db.String(20))
    charge_region = db.Column("JURANG", db.String(20))
    email = db.Column("EMAIL", db.String(50), index=True, unique=True, nullable=False)
    institution = db.Column("INSTT_NM", db.String(100))
    department = db.Column("DEPT_NM", db.String(100))
    
    def __init__(self, username, email, password, realname, tel=None, is_confirmed=False, authority=None, charge_region=None, institution=None, department=None):
        self.username = username
        self.email = email
        self.realname = realname
        self.tel = tel
        self.is_confirmed = is_confirmed
        self.authority = authority
        self.charge_region = charge_region
        self.institution = institution
        self.department = department

        self.set_password(password)
    
    def __repr__(self):
        return '<User {} / name : {}>'.format(self.username, self.realname)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 시스템 관리자(상위관리자 기능)
    def confirm_user(self, target_user):
        target_user.is_confirmed = True
        target_user.confirmed_user = self
        target_user.confirmed_date = datetime.now()
        return target_user

    def delete_user(self, target_user):
        target_user.is_deleted = True
        target_user.deleted_user = self
        target_user.deleted_date = datetime.now()
        return target_user

    # 정보 업데이트
    def update(self, **kwargs):
        for k, v in kwargs:
            exec("self.{} = v".format(k))
        return self

    @staticmethod
    def check_unique_email(email):
        return Administrator.query.filter_by(email=email).count() == 0