#coding:utf-8
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email,EqualTo


class LoginForm(Form):
    name = StringField(u'用户名：',validators=[DataRequired(message=u'用户名不能为空')])
    password = PasswordField(u'密码',validators=[DataRequired(message=u'密码不能为空')])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登录')


class RegisterForm(Form):
    name = StringField(u'用户名：',validators=[DataRequired(message=u'用户名不能为空')])
    email = StringField(u'邮箱：',validators=[DataRequired(message=u'邮箱不能为空'),
                        Email(message=u'错误的邮箱格式')])
    password = PasswordField(u'密码：',validators=[DataRequired(message=u'密码不能为空'),
                        EqualTo('password2', message=u'两次输入密码必须一致')])
    password2 = PasswordField(u'确认密码：',validators=[DataRequired(message=u'确认密码不能为空')])
    submit = SubmitField(u'注册')


class ResetUsernameForm(Form):
    name = StringField(u'新的用户名：',validators=[DataRequired(message=u'新的用户名不能为空')])
    submit = SubmitField(u'修改')


class ResetEmailForm(Form):
    email = StringField(u'邮箱：',validators=[DataRequired(message=u'邮箱不能为空'),
                        Email(message=u'错误的邮箱格式'),EqualTo('email2',message=u'两次输入邮箱必须一致')])
    email2 = StringField(u'确认邮箱：',validators=[DataRequired(message=u'确认邮箱不能为空'),
                        Email(message=u'错误的邮箱格式')])
    submit = SubmitField(u'修改')


class ResetPasswordForm(Form):
    password = PasswordField(u'原密码：',validators=[DataRequired(message=u'确认密码不能为空')])
    password1 = PasswordField(u'新密码：',validators=[DataRequired(message=u'密码不能为空'),
                              EqualTo('password2', message=u'两次输入密码必须一致')])
    password2 = PasswordField(u'确认新密码：',validators=[DataRequired(message=u'确认密码不能为空')])
    submit = SubmitField(u'修改')


class ForgetPasswordForm(Form):
    email = StringField(u'邮箱：',validators=[DataRequired(message=u'邮箱不能为空'),
                        Email(message=u'错误的邮箱格式')])
    password = PasswordField(u'新密码：',validators=[DataRequired(message=u'密码不能为空'),
                              EqualTo('password2', message=u'两次输入密码必须一致')])
    password2 = PasswordField(u'确认新密码：',validators=[DataRequired(message=u'确认密码不能为空')])
    submit = SubmitField(u'发送邮件并修改')


