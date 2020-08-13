from datetime import datetime
from flask import Flask, jsonify, redirect, render_template, request, flash, url_for, session, Blueprint
from app import login_manager, db
from ..models.admin_models import Administrator
from ..models.common_models import CommonCode
from flask_login import login_required, current_user, login_user, logout_user
from ..utils import is_safe_url, generate_random_salt, decode
from ..auth import confirm_required

system_view = Blueprint("system", __name__, template_folder="templates/admin", static_folder="static")

#=========================================관리자 계정관리====================================
@system_view.route("/", methods=["GET"])
@login_required
@confirm_required
def administrators():
    # 관리자 계정 관리
    if current_user.authority == "ALL":
        administrators = Administrator.query.all()
        return render_template("/admin/administrators.html", administrators=administrators)
    else:
        flash("접근 권한이 없습니다.", "warning")
        return redirect(url_for("main/index"))