from datetime import datetime
from flask import Flask, jsonify, redirect
from myapp import app

@app.route("/")
def red():
    return redirect("http://127.0.0.1:5000/index.html")

@app.route("/hello")
def hello():
    json_resp = jsonify(
        status=200,
        msg="Hello world"
    )
    return json_resp