from datetime import datetime
from flask import Flask, jsonify, redirect, render_template, request
from app import app
from app.models.mymodel import Administrator
from flask_user import login_required, roles_required, current_user, UserManager, UserMixin
import pdb

@app.route("/")
def index():
    if current_user:
        return render_template("admins/index.html")
    else:
        flask.flash("로그인이 필요합니다.")
        return render_template("admins/login.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if not current_user:
        if request.method == "GET":
            return render_template("admins/login.html")
        elif request.method == "POST":
            # 로그인 처리
            input_username = request.args.get("input-username")
            pass
    else:
        return render_template("admins/index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if not current_user:
        if request.method == "GET":
            return render_template("admins/register.html")
        elif request.method == "POST":
            # 등록신청 처리
            input_username = request.args.get("input-username")
            pass
    else:
        return render_template("admins/index.html")

@app.route("/is-unique-username", methods=["POST"])
def is_unique_username():
    input_username = request.args.get("inputUsername")
    result = False
    if Administrator.query.filter_by(username=input_username).exists():
        result = True
    return jsonify(isunique=result)

@app.route("/hello")
def hello():
    sample = Administrator.query.first()

    return jsonify(
        status=200,
        msg="Hello world",
        sample=sample.to_dict()
    )