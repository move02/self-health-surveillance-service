from datetime import datetime, timedelta
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, url_for
from app import db
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from flask_login import UserMixin
from .common_models import CommonCode
from functools import wraps

from dotenv import load_dotenv

import pdb

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env_code'))

class Administrator(db.Model, SerializerMixin, UserMixin):
    __tablename__="t_admin_info_m01"
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
    is_deleted = db.Column("DELETE_AT", db.Boolean, default=False)
    deleted_user = db.Column("DELETE_ID", db.String(30))
    deleted_date = db.Column("DELETE_DATE", db.DateTime)
    last_login = db.Column("LAST_LOGIN", db.DateTime)
    authority = db.Column("AUTHOR", db.String(20))
    charge_area = db.Column("JURANG", db.String(20))
    email = db.Column("EMAIL", db.String(50), index=True, unique=True, nullable=False)
    institution = db.Column("INSTT_NM", db.String(100))
    department = db.Column("DEPT_NM", db.String(100))
    
    def __init__(self, username, email, password, realname, tel=None, is_confirmed=False, authority=None, charge_area=None, institution=None, department=None):
        self.username = username
        self.email = email
        self.realname = realname
        self.tel = tel
        self.is_confirmed = is_confirmed
        self.authority = authority
        self.charge_area = charge_area
        self.institution = institution
        self.department = department
        
        self.set_password(password)

    def __repr__(self):
        return '<User {} / name : {}>'.format(self.username, self.realname)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # UserMixin 클래스 메소드 오버라이드
    def get_id(self):
        return self.sn

    # 시스템 관리자(상위관리자 기능)
    def confirm_user(self, target_user):
        if self.authority == "ALL":
            target_user.is_confirmed = True
            target_user.confirmed_user = self.username
            target_user.confirmed_date = datetime.now()
            db.session.add(target_user)
            db.session.commit()
            return target_user
        else:
            return None

    def delete_user(self, target_user):
        if self.authority == "ALL":
            target_user.is_deleted = True
            target_user.deleted_user = self.username
            target_user.deleted_date = datetime.now()
            db.session.add(target_user)
            db.session.commit()
            return target_user
        else:
            return None

    # 정보 업데이트
    def update(self, **kwargs):
        for k, v in kwargs:
            exec("self.{} = v".format(k))
        return self

    # NotNull Decorator
    def not_null(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            if not args[-1]:
                raise AssertionError("{} is not nullable".format(args[1]))
            return func(*args, **kwargs)
        return decorator
        
    # Length Decorator
    def length(limit):
        def wrapper(func):
            @wraps(func)
            def decorator(*args, **kwargs):
                if len(args[-1]) > limit:
                    raise AssertionError("{} 필드 길이제한 : {}".format(args[1], limit))
                return func(*args, **kwargs)
            return decorator
        return wrapper

    # Validators
    @validates('username')
    @not_null
    @length(30)
    def validate_username(self, key, username):
        if Administrator.query.filter(Administrator.username == username).first():
            raise AssertionError("Username is already in use")

        return username
    
    @validates('realname')
    @not_null
    @length(100)
    def validate_realname(self, key, realname):        
        return realname
    
    @validates('email')
    @not_null
    @length(30)
    def validate_email(self, key, email):
        if Administrator.query.filter(Administrator.email == email).first():
            raise AssertionError("Email is already in use")

        return email

    @validates('tel')
    @length(15)
    def validate_tel(self, key, tel):        
        return tel

    @validates('charge_area')
    @not_null
    @length(15)
    def validate_charge_area(self, key, charge_area):
        area_group_code = os.environ.get("AREA_GROUP_CODE")
        if CommonCode.query.filter_by(group_code=area_group_code, code=charge_area).count() < 1:
            raise AssertionError("There is no area code like {}.{}".format(area_group_code, charge_area))

        return charge_area

    @validates('institution')
    @length(100)
    def validate_institution(self, key, institution):
        return institution

    @validates('deptartment')
    @length(100)
    def validate_institution(self, key, department):
        return department
        
