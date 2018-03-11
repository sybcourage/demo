#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask,render_template,redirect,flash,session,url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,login_required, login_user,logout_user,current_user
import config
from config import DevConfig
from app.form import *
from app.model import *


app = Flask(__name__)
app.config.from_object(DevConfig)
app.secret_key=config.secret
db = SQLAlchemy(app)
login_manager=LoginManager()
login_manager.session_protection='strong'
login_manager.login_view='auth.login'
login_manager.init_app(app)
bootstrap=Bootstrap(app)


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/show')
def show_data():
    return "flask+echarts+mysql"


@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            is_admin = (user.role == Role.query.filter_by(name='Admin').first())
            session['is_admin'] = is_admin
            return render_template('index.html', current_user=user)
        flash(u'用户名或密码错误！')
    return render_template('login.html', form=form)


if __name__=='__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)