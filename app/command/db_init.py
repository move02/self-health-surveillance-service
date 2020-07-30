import datetime

from flask import current_app
from flask_script import Command

from app import db
from app.models.admin_models import *

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

    admin_role = find_or_create_role('SysAdmin')

    user = find_or_create_user(u'move02', u'move02@daumsoft.com', '1234', u'move02', admin_role)

    db.session.commit()


def find_or_create_role(name):
    role = Role.query.filter(Role.name == name).first()
    if not role:
        role = Role(name=name)
        db.session.add(role)
    return role


def find_or_create_user(username, email, password, realname, role=None):
    user = Administrator.query.filter(Administrator.username == username).first()
    if not user:
        user = Administrator(username=username,
                    email=email,
                    password=password,
                    realname=realname,
                    active=True,
                    email_confirmed_at=datetime.utcnow())

        user.set_password(password)
    if role:
        user.roles.append(role)
        
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
                    sample = Administrator(username=obj["username"], email=obj["email"], password=str(obj["password"]))
                    db.session.add(sample)
                db.session.commit()

        if len(Region.query.all()) == 0 and current_env != "Product":
            region_names = ["서울", "인천", "대전", "대구", "광주", "부산", "울산", "경기", "강원", "충북", "충남", "경북", "경남", "전북", "전남", "제주"]
            for rn in region_names:
                new_region = Region(rn)
                db.session.add(new_region)
            db.session.commit()

if __name__ == "__main__":
    init_db()