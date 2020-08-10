from functools import wraps
from flask import request, redirect, url_for
from flask_login import current_user

def confirm_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not (current_user != None and current_user.is_confirmed):
            return redirect(url_for('wait', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
