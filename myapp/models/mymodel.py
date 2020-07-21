from datetime import datetime, timedelta
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, url_for
from myapp import db

class MyModel(db.Model):
    __tablename__="mytable"
    __table_args__={'mysql_collate': 'utf8_general_ci'}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    incharge_region = db.Column(db.String(140))
    last_login = db.Column(db.DateTime, default=datetime.utcnow)

    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email

        self.set_password(password)
    
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)