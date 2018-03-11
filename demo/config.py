#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE_USER = 'root'
DATABASE_PASSWORD= 'qwe123456'
DATABASE_URL='localhost:3306'

secret = 'aGVswwr4gl29yb5p07-%*'

class Config(object):
    pass


class ProdConfig(Config):
    pass

class DevConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + DATABASE_USER + ':' + DATABASE_PASSWORD + '@' + DATABASE_URL + '/flask-test'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True