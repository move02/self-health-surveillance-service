from datetime import datetime
from flask import Flask, jsonify, redirect, render_template, request, flash, url_for, session, Blueprint
from app import login_manager, db
from ..models.admin_models import Administrator
from ..models.common_models import CommonCode
from flask_login import login_required, current_user, login_user, logout_user
from ..utils import is_safe_url, generate_random_salt, decode
from ..auth import confirm_required

main_view = Blueprint("main", __name__, template_folder="templates/admin", static_folder="static")

@main_view.route("/")
@main_view.route("/index")
@login_required
@confirm_required
def index():
    return render_template("/admin/index.html")

@main_view.route("/breakouts", methods=["GET"])
@login_required
@confirm_required
def breakouts():
    # 관할지역 발생현황 조회
    return render_template("/admin/breakouts.html")

@main_view.route("/suspecters", methods=["GET"])
@login_required
@confirm_required
def suspecters():
    # 감염 의심자 발생현황 조회
    return render_template("/admin/suspecters.html")

@main_view.route("/user-locations", methods=["GET"])
@login_required
@confirm_required
def user_locations():
    # 정보동의자 동선조회
    return render_template("/admin/user_locations.html")