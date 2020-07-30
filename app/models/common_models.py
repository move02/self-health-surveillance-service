from datetime import datetime, timedelta
import json
import os
from flask import current_app, url_for
from app import db
from sqlalchemy_serializer import SerializerMixin

class CommonCode(db.Model):
    pass