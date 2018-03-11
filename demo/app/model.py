#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from flask_login import UserMixin
from flask import current_app
from werkzeug.security import generate_password_hash,check_password_hash


from temper_web import db

class Temperature(db.Model):
    __tablename__ = 'temperatures'
    id=db.Column(db.BigInteger(),primary_key = True,autoincrement = True)
    time = db.Column(db.DATETIME,default = datetime.now())
    temp1 = db.Column(db.String(64), nullable = False)
    temp2 = db.Column(db.String(64), nullable = False)
    temp3 = db.Column(db.String(64), nullable = False)

    def __repr__(self):
        return "<temper {},{},{}>".format(self.temp1,self.temp2,self.temp3)

class Role(db.Model):
    __tablename__='roles'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = ('Normal', 'Admin')
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key = True, autoincrement = True)
    username = db.Column(db.String(64), unique = True, index = True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        # 新添加的用户，初始其角色为普通用户。
        if self.role is None:
            self.role = Role.query.filter_by(name='Normal').first()

    def __repr__(self):
        return '<User %r>' % self.username

    # 初次运行程序时生成初始管理员的静态方法
    @staticmethod
    def generate_admin():
        admin = Role.query.filter_by(name='Admin').first()
        u = User.query.filter_by(role=admin).first()
        if u is None:
            u = User(username='admin', \
                     password=current_app.config['AdminPassword'], \
                     role=Role.query.filter_by(name='Admin').first())
            db.session.add(u)
        db.session.commit()

    @property
    def password(self):
        # raise AttributeError('password is not a readable attribute')
        pass

    @password.setter
    def password(self, password):
        if password == '':
            password = '123456'
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


