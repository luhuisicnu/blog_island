#coding:utf-8
from flask import render_template, redirect, url_for, session,\
                    flash
from flask.ext.login import login_required, current_user
from . import main
from ..decorators import permission_required
from ..models import Permission, Role, Follow, User, db, Article


@main.route('/',methods=['GET'])
def index():
    articles = Article.query.order_by(Article.publish_time.desc()).all()[:5]
    users = User.query.order_by(User.last_login_time.desc()).all()[:5]
    return render_template('index.html',articles=articles,users=users) 


@main.app_errorhandler(403)
def permission_denied(e):
    return render_template('403.html'),403


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404


@main.app_errorhandler(413)
def file_too_large(e):
    return render_template('413.html'),413


@main.app_errorhandler(500)
def server_error(e):
    return render_template('500.html'),500

