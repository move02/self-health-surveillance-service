from datetime import datetime
from flask import Flask, jsonify, redirect, render_template, request, flash, url_for, session, Blueprint
from app import login_manager, db, area_group_code, sex_group_code, age_group_code, risk_group_code
from ..models.admin_models import Administrator
from ..models.common_models import CommonCode
from flask_login import login_required, current_user, login_user, logout_user
from ..utils import is_safe_url, generate_random_salt, decode
from ..auth import confirm_required

general_view = Blueprint("general", __name__, template_folder="templates/admin", static_folder="static")

@login_manager.user_loader
def admin_loader(sn):
    return Administrator.query.get(sn)

@general_view.route("/wait", methods=["GET"])
@login_required
def wait():
    user = current_user
    if user.is_confirmed:
        flash("잘못된 접근입니다.", "warning")
        return redirect(url_for(request.referrer))
    else:
        return render_template("/admin/wait.html")

##===============template filters===============

@general_view.app_template_filter()
def format_datetime(value, format='basic'):
    if value:
        delta = datetime.now() - value
        if delta.seconds < 3600:
            return "{}분 전".format(delta.seconds // 60)
        elif delta.seconds < 86399:
            return "{}시간 전".format(delta.seconds // 3600)
        else:
            format = "%Y. %m. %d %H:%M"
            return value.strftime(format)
    else:
        return ""


@general_view.app_template_filter()
def code_description(code):
    code_object = CommonCode.query.filter_by(code=code).first()
    if code_object:
        return code_object.code_desc
    else:
        return ""