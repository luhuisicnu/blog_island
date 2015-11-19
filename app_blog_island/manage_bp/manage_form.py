#coding:utf-8
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email,EqualTo



class UserSearchForm(Form):
    input = StringField(u'用户名：',validators=[DataRequired(message=u'用户名不能为空')])
    submit = SubmitField(u'查找')


class UserModForm(Form):
    banned = BooleanField(u'封禁该用户')
    submit = SubmitField(u'设置')


class RoleChooseForm(Form):
    input = StringField(u'角色名：',validators=[DataRequired(message=u'角色名不能为空')])
    submit = SubmitField(u'查找')


class RoleModForm(Form):
    follow = BooleanField(u'关注')
    comment = BooleanField(u'评论')
    write_articles = BooleanField(u'撰写博客')
    manage_comment = BooleanField(u'管理评论')
    manage_articles = BooleanField(u'管理博客')
    manage_homepage = BooleanField(u'管理个人主页')
    submit = SubmitField(u'设置')
