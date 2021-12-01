from flask import Flask, Blueprint, render_template, request, redirect, url_for,request_started, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.sql import func


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/sample'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'sangatrahasia'
db = SQLAlchemy(app)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(150), unique=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(180))
    password = db.Column(db.String(180))
    admin = db.Column(db.Boolean)


