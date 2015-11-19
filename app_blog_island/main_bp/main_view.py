#coding:utf-8
from flask import render_template, redirect, url_for, session
from flask.ext.login import login_required
from . import main
from ..decorators import permission_required
from ..models import Permission, Role


@main.route('/',methods=['GET'])
def index():
    return render_template('index.html') 


@main.app_errorhandler(403)
def page_not_found(e):
    return render_template('403.html'),403


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404


@main.app_errorhandler(500)
def page_not_found(e):
    return render_template('500.html'),500


@main.route('/admin')
@login_required
@permission_required(Role.Administrator)
def for_admins_only():
    return "For administrators!"


@main.route('/user')
@login_required
@permission_required(Role.User)
def for_moderators_only():
    return "For user!"


@main.route('/session')
def ss():
    if 'username' in session:
        resp = 'Welcome %s!' % session['username']
    else:
        resp = 'no session'
    return str(session['_id'])
