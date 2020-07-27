from datetime import datetime, timedelta
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, url_for
from app import db
from sqlalchemy_serializer import SerializerMixin
from flask_user import UserMixin

class Administrator(db.Model, SerializerMixin, UserMixin):
    __tablename__="administrators"
    __table_args__={'mysql_collate': 'utf8_general_ci'}

    serialize_only = ('id', 'username', 'realname', 'email', 'region', 'last_login', 'roles')

    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
    username = db.Column(db.String(128), index=True, unique=True, nullable=False)
    realname = db.Column(db.String(64), index=True, nullable=True)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    region_id = db.Column(db.Integer, db.ForeignKey("regions.id"))

    # relations
    roles = db.relationship('Role', secondary='user_roles')
    region = db.relationship('Region', back_populates="administrators")
    
    def __init__(self, username, email, password, realname=None, active=False, email_confirmed_at=None):
        self.username = username
        self.email = email
        self.realname=realname
        self.active = active
        self.email_confirmed_at = email_confirmed_at

        self.set_password(password)
    
    def __repr__(self):
        return '<User {} / mail : {}>'.format(self.username, self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Role(db.Model, SerializerMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    
    def __repr__(self):
        return '<id : {}, name : {}>'.format(self.id, self.name)


class UserRoles(db.Model, SerializerMixin):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('administrators.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

class Region(db.Model, SerializerMixin):
    __tablename__ = "regions"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    
    # relationships
    administrators = db.relationship('Administrator', back_populates="region", order_by="Administrator.id")

    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return '<id : {}, name : {}>'.format(self.id, self.name)
