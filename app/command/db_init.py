import datetime

from flask import current_app
from flask_script import Command

from app import db, create_app
from app.models.admin_models import Administrator
from app.models.common_models import CommonCode
from sqlalchemy import func
from config import *

import pdb

import json

class InitDbCommand(Command):
    def run(self):
        init_db()
        print('DB initialized')
        
    
def init_db():
    db.drop_all()
    db.create_all()
    seeding()
    create_users()


def create_users():
    db.create_all()
    user = find_or_create_user(u'move02', u'move02@daumsoft.com', '1234', u'이동영', "010-2222-2222", is_confirmed=True, authority="ALL", charge_area="00", institution="Daumsoft", department="TSC")

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

def seeding():
    from dotenv import load_dotenv

    current_env = os.environ.get("CURRENT_ENV")
    with current_app.app_context():
        if current_env != "Product": 
            if len(CommonCode.query.all()) < 1:
                group_code = "AREA_CODE"
                standard_codes = {
                    "전국" : "00", 
                    "서울특별시" : "11", 
                    "부산광역시" : "21", 
                    "대구광역시" : "22", 
                    "인천광역시" : "23", 
                    "광주광역시" : "24", 
                    "대전광역시" : "25", 
                    "울산광역시" : "26", 
                    "세종특별자치시" : "29", 
                    "경기도" : "31", 
                    "강원도" : "32", 
                    "충청북도" : "33", 
                    "충청남도" : "34", 
                    "전라북도" : "35", 
                    "전라남도" : "36", 
                    "경상북도" : "37", 
                    "경상남도" : "38", 
                    "제주특별자치도" : "39"
                }

                for k,v in standard_codes.items():
                    code_obj = CommonCode(group_code=group_code, code=str(v), code_value=k)
                    db.session.add(code_obj)
                db.session.commit()

            if len(Administrator.query.all()) < 2:
                with open("seeds.json", "r") as seed_file:
                    seed_data = json.load(seed_file)
                    for obj in seed_data["datas"]:
                        random_charge_area=CommonCode.query.order_by(func.random()).first().code
                        sample = Administrator(username=obj["username"], 
                            email=obj["email"], 
                            password=str(obj["password"]),
                            realname=obj["realname"],
                            tel=obj["tel"], 
                            charge_area=random_charge_area,
                            institution=obj["institution"],
                            department=obj["department"]
                        )

                        db.session.add(sample)
                    db.session.commit()

if __name__ == "__main__":
    app = create_app(TestConfig)

    app_context = app.app_context()
    app_context.push()
    init_db()