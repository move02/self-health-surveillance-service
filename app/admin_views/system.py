from datetime import datetime
from flask import Flask, jsonify, redirect, render_template, request, flash, url_for, session, Blueprint
from app import login_manager, db, area_group_code, sex_group_code, age_group_code, risk_group_code
from ..models.admin_models import Administrator
from ..models.common_models import CommonCode
from flask_login import login_required, current_user, login_user, logout_user
from ..utils import is_safe_url, generate_random_salt, decode
from ..auth import confirm_required

import pdb

system_view = Blueprint("system", __name__, template_folder="templates/admin", static_folder="static")

#=========================================관리자 계정관리====================================
@system_view.route("/", methods=["GET"])
@login_required
@confirm_required
def administrators():
    # 관리자 계정 관리
    if current_user.authority == "ALL":
        administrators = Administrator.query.order_by(Administrator.registered_date.desc()).all()
        return render_template("/admin/administrators.html", administrators=administrators)
    else:
        flash("접근 권한이 없습니다.", "warning")
        return redirect(url_for("main/index"))

@system_view.route("/approve", methods=["POST"])
@login_required
@confirm_required
def approve():
    # 관리자 계정 승인
    if current_user.authority == "ALL":
        form_data = request.form

        # 사용자 정보들
        method = form_data.get("_method")
        input_username = form_data.get("input-username")
        
        if method == "put":
            not_approved_admin = Administrator.query.filter_by(username=input_username).first()
            result = current_user.confirm_user(not_approved_admin)
            if result:
                flash("승인이 완료되었습니다.", "success")
                return redirect(url_for("system.administrators"))
            else:
                flash("권한이 없습니다", "warning")
                return redirect(url_for("main.index"))
        else:
            flash("잘못된 접근입니다.", "warning")
            return redirect(url_for("main.index"))
    else:
        flash("접근 권한이 없습니다.", "warning")
        return redirect(url_for("main.index"))



@system_view.route("/delete", methods=["POST"])
@login_required
@confirm_required
def delete():
    # 관리자 계정 삭제
    if current_user.authority == "ALL":
        form_data = request.form

        # 사용자 정보들
        method = form_data.get("_method")
        input_username = form_data.get("input-username")
        
        if method == "delete":
            to_be_deleted_admin = Administrator.query.filter_by(username=input_username).first()
            result = current_user.delete_user(to_be_deleted_admin)
            if result:
                flash("삭제처리가 완료되었습니다.", "success")
                return redirect(url_for("system.administrators"))
            else:
                flash("권한이 없습니다", "warning")
                return redirect(url_for("main.index"))
        else:
            flash("잘못된 접근입니다.", "warning")
            return redirect(url_for("main.index"))
    else:
        flash("접근 권한이 없습니다.", "warning")
        return redirect(url_for("main.index"))