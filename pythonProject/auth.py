from flask import Flask, render_template, request, redirect, url_for,request_started, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
import uuid



## Connection To Database ##

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/sample'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'sangatrahasia'
db = SQLAlchemy(app)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated




@app.route('/')
def Home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def Login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                token = jwt.encode(
                    {'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                    app.config['SECRET_KEY'])
                flash('Logged in successfully!', category='success')
                return redirect(url_for('Home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
            return redirect(url_for('Login'))

    return render_template("login.html")



@app.route('/signup', methods=['GET', 'POST'])
def Signup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        else:
            signup = User(public_id=str(uuid.uuid4()), email=email, name=name, password=generate_password_hash(
                password, method='sha256'))
            db.session.add(signup)
            db.session.commit()
            flash('Account created!', category='success')

            return redirect(url_for('Login'))

    return render_template("signup.html")


@app.route('/logout')
def logout():

    flash('Logout Success', category='success')
    return redirect(url_for('Home'))




@app.route('/user', methods=['GET'])
def user():

    if not User.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['email'] = user.email
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)

    return jsonify({'users' : output})
