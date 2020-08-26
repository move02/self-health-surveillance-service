import datetime

from flask import current_app
from flask_script import Command

from app import db, create_app
from app.models.admin_models import Administrator
from app.models.common_models import CommonCode
from sqlalchemy import func
from config import *

import json
import sys

class InitDbCommand(Command):
    def run(self):
        init_db()
        print('DB initialized')
        
    
def init_db(app):
    if app.__class__ == TestConfig:
        db.drop_all()
        db.create_all()
    create_users()


def create_users():
    user = find_or_create_user(u'move02', u'move02@daumsoft.com', '1234', u'이동영', "010-2222-2222", is_confirmed=True, authority="ALL", charge_area="SIDO_01", institution="Daumsoft", department="TSC")

    db.session.commit()


# def find_or_create_role(name):
#     role = Role.query.filter(Role.name == name).first()
#     if not role:
#         role = Role(name=name)
#         db.session.add(role)
#     return role


def find_or_create_user(username, email, password, realname, tel, is_confirmed=False, authority=None, charge_area=None, institution=None, department=None):
    user = Administrator.query.filter(Administrator.username == username).first()
    if not user:
        user = Administrator(username=username, 
            email=email, 
            password=str(password),
            realname=realname,
            tel=tel, 
            is_confirmed=is_confirmed, 
            authority=authority, 
            charge_area=charge_area, 
            institution=institution, 
            department=department
        )

        user.set_password(password)

    db.session.add(user)
    return user

if __name__ == "__main__":
    if sys.argv[1] == "product":
        app = create_app(ProductConfig)
    else:
        app = create_app(TestConfig)

    app_context = app.app_context()
    app_context.push()
    init_db(app)