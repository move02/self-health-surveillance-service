from datetime import datetime
from flask import Flask, jsonify, redirect, render_template, request, flash, url_for, session, Blueprint
from app import login_manager, db
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