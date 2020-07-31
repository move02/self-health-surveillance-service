import datetime

from flask import current_app
from flask_script import Command

from app import db, create_app
from app.models.admin_models import *
from config import *

class InitDbCommand(Command):
    def run(self):
        init_db()
        print('DB initialized')
        
    
def init_db():
    db.drop_all()
    db.create_all()
    create_users()
    seeding()


def create_users():
    db.create_all()
    user = find_or_create_user(u'move02', u'move02@daumsoft.com', '1234', u'이동영', "010-2222-2222", is_confirmed=True, authority="ALL", institution="Daumsoft", department="TSC")

    db.session.commit()


# def find_or_create_role(name):
#     role = Role.query.filter(Role.name == name).first()
#     if not role:
#         role = Role(name=name)
#         db.session.add(role)
#     return role


def find_or_create_user(username, email, password, realname, tel, is_confirmed=False, authority=None, charge_region=None, institution=None, department=None):
    user = Administrator.query.filter(Administrator.username == username).first()
    if not user:
        user = Administrator(username=username, 
            email=email, 
            password=str(password),
            realname=realname,
            tel=tel, 
            is_confirmed=is_confirmed, 
            authority=authority, 
            charge_region=charge_region, 
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
        if len(Administrator.query.all()) < 2 and current_env != "Product":
            with open("seeds.json", "r") as seed_file:
                seed_data = json.load(seed_file)
                for obj in seed_data["datas"]:
                    sample = Administrator(username=obj["username"], 
                        email=obj["email"], 
                        password=str(obj["password"]),
                        realname=obj["realname"],
                        tel=obj["tel"], 
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