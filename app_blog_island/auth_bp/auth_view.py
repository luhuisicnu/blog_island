#coding:utf-8
import os
from urllib import quote
from flask import flash, url_for, redirect, render_template, request,\
     current_app, session, make_response
from flask.ext.login import login_user,logout_user, login_required,\
     current_user
from . import auth
from .auth_form import LoginForm, RegisterForm, ResetUsernameForm, \
    ResetEmailForm, ResetPasswordForm, ForgetPasswordForm
from ..models import User, Role, User_Role_Relation, db, Follow
from ..email import send_email
from ..decorators import permission_required


@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            flash(u'不存在的用户名，请确认输入正确或注册新用户')
            return render_template('auth/login.html',form=form)
        if not user.verify_password(form.password.data):
            flash(u'错误的密码，请重新输入')
            return render_template('auth/login.html',form=form)
        login_user(user,form.remember_me.data)
        flash(u'登录成功')
        response = make_response(redirect(request.args.get('next') or url_for('main.index')))
        response.set_cookie('user_id',str(user.id))
        return response
    return render_template('auth/login.html',form=form)
        
            
@auth.route('/logout',methods=['GET'])
@login_required
def logout():
    logout_user()
    flash(u'退出登录成功')
    response = make_response(redirect(url_for('main.index')))
    response.delete_cookie('user_id')
    return response


@auth.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.name.data,
                       email=form.email.data,
                       password=form.password.data)    
        db.session.add(user)
        db.session.commit()
        if form.email.data == os.environ['BLOG_ISLAND_MAIL_USERNAME']:
            ship = User_Role_Relation(user_id=user.id,
                role_id=Role.query.filter_by(rolename='Administrator').first().id,operate_id=user.id)
        else:
            ship = User_Role_Relation(user_id=user.id,
                role_id=Role.query.filter_by(rolename='User').first().id,operate_id=user.id)
        db.session.add(ship)
        fans = Follow(star_id=user.id,fans_id=user.id)
        db.session.add(fans)
        token = user.generate_confirmation_token()
        send_email(form.email.data,u'新账户邮件认证','auth/email/confirm',user=user,token=token)
        flash(u'注册已完成，已发送一封认证邮件到您的邮箱中')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html',form=form)


@auth.before_app_request
def keep_live():
    user_id = request.cookies.get('user_id',None)
    if not current_user.is_authenticated and user_id is not None:
        login_user(User.query.get(int(user_id)))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.active()
        if not current_user.confirmed \
            and request.endpoint[:5] != 'auth.': 
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed',methods=['GET'])
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('home.homepage',id=current_user.id))
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm',methods=['GET'])
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, u'新账户邮件认证',
               'auth/email/confirm', user=current_user, token=token)
    flash(u'一封新的认证邮件已经发送到您的邮箱')
    return redirect(url_for('main.index'))
    

@auth.route('/confirm/<token>',methods=['GET'])
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash(u'认证成功')
    else:
        flash(u'过期或无效的认证链接')
    login_user(current_user)
    return redirect(url_for('main.index'))


@auth.route('/reset_username',methods=['GET','POST'])
@login_required
@permission_required(Role.User)
def reset_username():
    form = ResetUsernameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is not None:
            if user.username != current_user.username:
                flash(u'用户名已被占用')
            else:
                flash(u'新用户名不能和原来的用户名相同，否则，请放弃修改')
            return redirect(url_for('auth.reset_username'))
        current_user.username = form.name.data
        db.session.add(current_user)
        return redirect(url_for('home.homepage',id=current_user.id))
    form.name.data = current_user.username
    return render_template('auth/reset_username.html',form=form)


@auth.route('/reset_email',methods=['GET','POST'])
@login_required
@permission_required(Role.User)
def reset_email():
    form = ResetEmailForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.email.data).first()
        if user is not None:
            if user.username != current_user.username:
                flash(u'邮箱已被占用')
            else:
                flash(u'新邮箱不能和原来的邮箱相同，否则，请放弃修改')
            return redirect(url_for('auth.reset_email'))
        token = current_user.generate_reset_token(form.email.data)
        send_email(form.email.data,u'重置邮箱确认',
                  'auth/email/confirm_reset_email',user=current_user,token=token)
        flash(u'已发送一封修改邮箱确认邮件到您的邮箱')
        return redirect(url_for('home.homepage',id=current_user.id))
    form.email.data = current_user.email
    return render_template('auth/reset_email.html',form=form)


@auth.route('/confirm_reset_email/<token>',methods=['GET'])
@login_required
@permission_required(Role.User)
def confirm_reset_email(token):
    if current_user.confirm_email(token):
        flash(u'修改邮箱成功')
    else:
        flash(u'过期或者无效的链接')
    return redirect(url_for('home.homepage',id=current_user.id))
    

@auth.route('/reset_password',methods=['GET','POST'])
@login_required
@permission_required(Role.User)
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        if not current_user.verify_password(form.password.data):
            flash(u'密码错误')
            return redirect(url_for('auth.reset_password'))
        current_user.password = form.password1.data
        db.session.add(current_user)
        flash(u'修改密码成功')
        return redirect(url_for('home.homepage',id=current_user.id))
    return render_template('auth/reset_password.html',form=form)


@auth.route('/forget_password_sendemail',methods=['GET','POST'])
def forget_password_sendemail():
    form = ForgetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash(u'不存在的注册邮箱')
            return redirect(url_for('auth.forget_password_sendemail'))
        token = user.generate_reset_token(form.email.data,password=form.password.data)
        send_email(form.email.data,u'忘记密码确认',
                   'auth/email/forget_password',user=user,token=token)
        flash(u'已发送一封忘记密码确认邮件到您的邮箱')
        return redirect(url_for('main.index'))
    return render_template('auth/forget_password_sendemail.html',form=form)


@auth.route('/forget_password_newpassword/<token>',methods=['GET','POST'])
def forget_password_newpassword(token):
    if not User.confirm_reset_email(token):
        flash(u'过期或者无效的链接')
    else:
        flash(u'修改密码成功')
    return redirect(url_for('main.index'))
        
        
@auth.route('/ask_for_lift_ban')
@login_required
def ask_for_lift_ban():
    send_email(current_app.config['BLOG_ISLAND_MAIL_SENDER'],u'申请解封用户',
              'auth/email/ask_for_lift_ban',user=current_user,sub=quote('回复：[博客岛] 申请解封用户'))
    flash(u'申请解封成功，三个工作日内将处理，请耐心等待，超出日期未处理，请到投诉反馈区提出意见')
    current_user.ask_for_lift_ban = True
    db.session.add(current_user)
    return redirect(url_for('home.homepage',id=current_user.id))
