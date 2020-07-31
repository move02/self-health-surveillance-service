from datetime import datetime
from flask import Flask, jsonify, redirect, render_template, request, flash, url_for, session
from app import app, login_manager, db
from .models.admin_models import Administrator
from .models.common_models import CommonCode
from flask_login import login_required, current_user, login_user, logout_user
from .utils import is_safe_url, generate_random_salt, decode

import pdb

@login_manager.user_loader
def load_user(user_id):
    return Administrator.query.get(user_id)

#============================ 인덱스 ==============================
@app.route("/admin")
@app.route("/admin/index")
@login_required
def index():
    return render_template("admin/index.html")

@app.route("/admin/login", methods=["GET", "POST"])
def login():
    if not current_user.is_authenticated:
        if request.method == "GET":
            salt = generate_random_salt()
            session['salt'] = salt
            return render_template("admin/login.html", salt=salt)
        elif request.method == "POST":
            # 로그인 처리
            input_username = request.form["input-username"]
            input_password = request.form["input-password"]

            salt = session.get("salt")
            input_password = decode(input_password, salt)

            user = Administrator.query.filter_by(username=input_username).first()
            if user:
                if user.check_password(input_password):
                    login_user(user)
                    flash("안녕하세요 {} 님".format(user.realname), "success")

                    next = request.args.get('next')
                    if not is_safe_url(next, request):
                        return flask.abort(400)

                    return redirect(next or url_for('index'))
            
            flash("아이디 혹은 패스워드가 일치하지 않습니다.", "warning")
    return redirect("/")

#===============================회원가입=====================================

@app.route("/admin/register", methods=["GET", "POST"])
def register():
    if not current_user.is_authenticated:
        if request.method == "GET":
            areas = CommonCode.query.filter_by(group_code="AREA_CODE").all()

            salt = generate_random_salt()
            session['salt'] = salt

            return render_template("admin/register.html", areas=areas, salt=salt)
        elif request.method == "POST":
            # 등록신청 처리
            form_data = request.form

            # 사용자 정보들
            #     def __init__(self, username, email, password, realname, tel=None, is_confirmed=False, authority=None, charge_area=None, institution=None, department=None):
            input_area = form_data.get("input-area")
            input_username = form_data.get("input-username")
            input_email = form_data.get("input-email")
            input_password = form_data.get("input-password")
            input_password_confirm = form_data.get("input-password-confirm")
            input_institution = form_data.get("input-institution")
            input_department = form_data.get("input-department")
            input_realname = form_data.get("input-realname")
            input_tel = form_data.get("input-tel")
            
            salt = session.get("salt")
            input_password = decode(input_password, salt)
            input_password_confirm = decode(input_password_confirm, salt)

            if input_password == input_password_confirm:
                new_admin = Administrator(
                    username=username,
                    
                )

            flash("신청이 처리되었습니다.", "success")
            return redirect("/login")
    else:
        return redirect("/")

@app.route("/admin/check/username", methods=["POST"])
def check_unique_username():
    input_username = request.get_json().get("input-username")
    result = True

    if Administrator.query.filter_by(username=input_username).count() > 0:
        result = False
    return jsonify(isunique=result)

#=========================================ID/PW 찾기====================================

@app.route("/admin/find", methods=["GET"])
def find():
    if not current_user.is_authenticated:
        salt = generate_random_salt()
        session['salt'] = salt
        areas = CommonCode.query.filter_by(group_code="AREA_CODE").all()

        return render_template("admin/password.html", areas=areas, salt=salt)
    else:
        flash("올바른 접근이 아닙니다.", "warning")
        return redirect(url_for('index'))

@app.route("/admin/find/password", methods=["POST"])
def find_password():
    if not current_user.is_authenticated:
        form_data = request.get_json(force=True)
        input_area = form_data.get("input-area-2")
        input_username = form_data.get("input-username")
        input_email = form_data.get("input-email-address-2")
        
        print(input_area)
        
        if input_area != "":
            query_result = Administrator.query.filter_by(charge_area=input_area, username=input_username, email=input_email)
        else:
            query_result = Administrator.query.filter_by(username=input_username, email=input_email)
        if query_result.count() != 0:
            admin = query_result.first()
            return jsonify(status=200, is_authenticated=True, user_id=admin.sn)
        else:
            return jsonify(status=200, is_authenticated=False)
    else:
        flash("올바른 접근이 아닙니다.", "warning")
        return redirect(url_for('index'))

@app.route("/admin/find/username", methods=["POST"])
def find_username():
    if not current_user.is_authenticated:
        form_data = request.get_json(force=True)
        input_area = form_data.get("input-area-1")
        input_email = form_data.get("input-email-address-1")

        print(input_area)

        if input_area != "":
            query_result = Administrator.query.filter_by(charge_area=input_area, email=input_email)
        else:
            query_result = Administrator.query.filter_by(email=input_email)
        if query_result.count() != 0:
            admin = query_result.first()
            return jsonify(status=200, username=admin.username)
        else:
            return jsonify(status=200, username=None)
    else:
        flash("올바른 접근이 아닙니다.", "warning")
        return redirect(url_for('index'))

@app.route("/admin/change/password", methods=["POST"])
def change_password():
    form_data = request.get_json(force=True)
    admin_id = form_data.get("pw-change-user-id")
    new_password = form_data.get("input-new-password")
    new_password_confirm = form_data.get("input-new-password-confirm")

    salt = session.get("salt")
    new_password = decode(new_password, salt)
    new_password_confirm = decode(new_password_confirm, salt)

    if new_password == new_password_confirm:
        admin = Administrator.query.get(admin_id)
        admin.set_password(new_password)
        db.session.add(admin)
        db.session.commit()
        flash("성공적으로 변경되었습니다.", "info")
        return jsonify(status=201, message="success")    
    else:
        return jsonify(status=202, message="passwords are not same.")    

#==================================================

@app.route("/admin/logout", methods=["POST"])
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash("로그아웃 되었습니다.", "info")
        return redirect(url_for('login'))
    else:
        flash("올바른 접근이 아닙니다.", "warning")
        return redirect(url_for('login'))


@app.route("/hello")
def hello():
    sample = Administrator.query.first()

    return jsonify(
        status=200,
        msg="Hello world",
        sample=sample.to_dict()
    )