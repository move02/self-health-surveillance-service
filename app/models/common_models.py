from datetime import datetime, timedelta
import json
import os
from flask import current_app, url_for
from app import db
from sqlalchemy_serializer import SerializerMixin

class CommonCode(db.Model, SerializerMixin):
    __tablename__="T_COMCODE_M01"
    __table_args__={'mysql_collate': 'utf8_general_ci'}

    group_code = db.Column("GROUP_CODE", db.String(30), index=True, primary_key=True)
    code = db.Column("ID", db.String(30), index=True, unique=True, primary_key=True)
    code_value = db.Column("CODE_VALUE", db.String(30), nullable=False)
    regist_date = db.Column("REGIST_DATE", db.DateTime, server_default=db.func.now(), nullable=False)
    code_desc = db.Column("CODE_DC", db.String(1000))
    is_using = db.Column("USE_AT", db.Boolean, nullable=False, default=True)
    rm_1 = db.Column("RM_1", db.String(50))
    rm_2 = db.Column("RM_2", db.String(50))
    rm_3 = db.Column("RM_3", db.String(50))

    
    def __init__(self, group_code, code, code_value, code_desc=None, rm_1=None, rm_2=None, rm_3=None):
        self.group_code = group_code
        self.code = code
        self.code_value = code_value
        self.code_desc = code_desc
        self.rm_1 = rm_1
        self.rm_2 = rm_2
        self.rm_3 = rm_3

    def __repr__(self):
        return '<Group {} / Code : {} / Value : {}>'.format(self.group_code, self.code, self.code_value)
    