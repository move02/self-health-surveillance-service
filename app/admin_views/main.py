from datetime import datetime
from flask import Flask, jsonify, redirect, render_template, request, flash, url_for, session, Blueprint
from app import login_manager, db, area_group_code, sex_group_code, age_group_code, risk_group_code
from ..models.admin_models import Administrator
from ..models.common_models import CommonCode
from ..models.user.userInfo import *
from ..models.user.placeInfo import *
from sqlalchemy import cast, Date
from flask_login import login_required, current_user, login_user, logout_user
from ..utils import is_safe_url, generate_random_salt, decode
from ..auth import confirm_required

import pdb

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
    allowed_area = CommonCode.query.filter_by(group_code=area_group_code, code=current_user.charge_area).first()
    risk_levels = CommonCode.query.filter_by(group_code=risk_group_code).all()

    form_data = request.form

    result = db.session\
        .query(
            userInfo.resideArea, 
            userInfo.registDate, 
            db.func.sum(userInfo.sn).label('total')
        )\
        .filter(userInfo.resideArea == allowed_area.code)\
        .group_by(cast(userInfo.registDate, Date))

    date_criteria = form_data.get("date-search-criteria")
    search_start_date = form_data.get("input-search_date1") 
    search_end_date = form_data.get("input-search_date2") 

    date_format = None

    if date_criteria and (search_start_date or search_end_date):
        if date_criteria == "month":
            date_format = "%Y-%m"
        elif date_criteria == "year":
            date_format = "%Y"
        else:
            date_format = "%Y-%m-%d"

        search_start_date = datetime.strptime(search_start_date, date_format)
        search_end_date = datetime.strptime(search_end_date, date_format)

        if search_start_date:
            result = result.filter(cast(userInfo.registDate, Date) >= search_start_date)
        if search_end_date:
            result = result.filter(cast(userInfo.registDate, Date) <= search_end_date)

    return render_template("/admin/breakouts.html", result=result.all(), risk_levels=risk_levels)

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
    allowed_area = CommonCode.query.filter_by(group_code=area_group_code, code=current_user.charge_area).first()
    risk_levels = CommonCode.query.filter_by(group_code=risk_group_code).all()
    
    form_data = request.form

    result = userInfo.query.filter(userInfo.resideArea == allowed_area.code)
    
    risk_criteria = form_data.get("search-criteria")
    search_start_date = form_data.get("input-search_date1") 
    search_end_date = form_data.get("input-search_date2")

    date_format = None

    if risk_criteria != "null" and (search_start_date or search_end_date):
        date_format = "%Y-%m-%d"

        search_start_date = datetime.strptime(search_start_date, date_format)
        search_end_date = datetime.strptime(search_end_date, date_format)

        if search_start_date:
            result = result.filter(cast(userInfo.registDate, Date) >= search_start_date)
        if search_end_date:
            result = result.filter(cast(userInfo.registDate, Date) <= search_end_date)

    return render_template("/admin/user_locations.html", result=result.all(), risk_levels=risk_levels)