from datetime import datetime
from flask import Flask, jsonify, redirect, render_template
from app import app
from app.models.mymodel import Administrators
from flask_user import login_required, roles_required, current_user, UserManager, UserMixin
import pdb

@app.route("/")
def index():
    # 
    return render_template("admins/index.html")

@app.route("/hello")
def hello():
    sample = Administrators.query.first()

    return jsonify(
        status=200,
        msg="Hello world",
        sample=sample.to_dict()
    )