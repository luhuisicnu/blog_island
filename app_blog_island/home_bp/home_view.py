from flask import flash, url_for, redirect, render_template, abort
from . import home
from ..models import User

@home.route('/<id>')
def home(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        abort(404)
    return render_template('home/home.html',user=user)
