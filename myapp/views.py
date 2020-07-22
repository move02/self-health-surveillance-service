from datetime import datetime
from flask import Flask, jsonify, redirect, render_template
from myapp import app

@app.route("/")
def index():
    return render_template("admins/index.html")

@app.route("/hello")
def hello():
    json_resp = jsonify(
        status=200,
        msg="Hello world"
    )
    return json_resp