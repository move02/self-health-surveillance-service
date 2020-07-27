from datetime import datetime
from flask import Flask, jsonify, redirect, render_template
from app import app
from app.models.mymodel import MyModel

@app.route("/")
def index():
    return render_template("admins/index.html")

@app.route("/hello")
def hello():
    sample = MyModel.query.first()
    return jsonify(
        status=200,
        msg="Hello world",
        sample=sample.to_dict()
    )