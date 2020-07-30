from datetime import datetime
from flask import jsonify, redirect, render_template, request, url_for

def page_not_found(e):
    return render_template("error_pages/404.html"), 404

def internal_error(e):
    return render_template("error_pages/500.html"), 500
