#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,SelectField, IntegerField,BooleanField,ValidationError
from wtforms.validators import Required,EqualTo,Length,Regexp
from model import Role,User


class LoginForm(FlaskForm):
    username = StringField(u'用户名', validators=[Required()])
    password = PasswordField(u'密码', validators=[Required()])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登录')


class SearchForm(FlaskForm):
    username = StringField(u'用户名', validators=[Required()])
    submit = SubmitField(u'搜索')


class UserForm(FlaskForm):
    username = StringField(u'用户名', validators=[Required()])
    password = PasswordField(u'密码', default='123456', description=u'默认密码为123456')
    role = SelectField(u'身份', coerce=int)

    submit = SubmitField(u'添加')

    def __init__(self, *args, **kargs):
        super(UserForm, self).__init__(*args, **kargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'此用户已存在，请检查！')


class EditForm(FlaskForm):
    username = StringField(u'用户名', validators=[Required()])
    # password = PasswordField(u'密码', validators=[Required(), Length(1, 64), \
    #                                             Regexp('^[a-zA-Z0-9_.]*$', 0, \
    #                                                    u'密码由字母、数字和_.组成')])
    role = SelectField(u'身份', coerce=int)
    submit = SubmitField(u'修改')

    def __init__(self, user, *args, **kargs):
        super(EditForm, self).__init__(*args, **kargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(u'旧密码', validators=[Required(message=u'密码不能为空')])
    password = PasswordField(u'新密码', validators=[
        Required(message=u'密码不能为空'), EqualTo('password2', message=u'密码必须匹配。')])
    password2 = PasswordField(u'确认新密码', validators=[Required(message=u'密码不能为空')])
    submit = SubmitField(u'更改')
