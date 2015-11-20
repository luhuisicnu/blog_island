#coding:utf-8
import os, os.path
from flask import flash, url_for, redirect, render_template, abort,\
        request, current_app
from flask.ext.login import login_required, current_user
from . import home
from .home_form import FileUploadForm
from ..models import User, Role, Permission, db
from ..decorators import permission_required
from ..functions import random_str


@home.route('/<id>')
def homepage(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        abort(404)
    return render_template('home/homepage.html',user=user)


@home.route('/upload_picture',methods=['GET','POST'])
@login_required
@permission_required(Role.User)
def upload_picture():
    form = FileUploadForm()
    if form.validate_on_submit():
        picture_path = '/root/blog_island/app_blog_island/static/picture/'
        static_path = '/root/blog_island/app_blog_island/static/'
        format = ['png','jpg','jpeg','gif']
        file = request.files['file']    #key 'file' is defined in FileUploadForm
        if file and '.' in file.filename and file.filename.rsplit('.', 1)[1] in format:
            newfilename = random_str(32) + '.' + file.filename.rsplit('.', 1)[1]
            while os.path.exists(picture_path + newfilename):
                newfilename = random_str(32) + '.' + file.filename.rsplit('.', 1)[1]
            file.save(picture_path +  newfilename)
            if os.path.exists(static_path + str(current_user.picture_url)):
                os.remove(static_path + current_user.picture_url)
            current_user.picture_url = 'picture/' + newfilename
            db.session.add(current_user)
            flash(u'上传照片成功')
            return redirect(url_for('home.homepage',id=current_user.id))
        else:
            flash(u'上传照片失败，请检查图片路径是否正确或图片格式是否是png,jpg,jpeg,gif其中之一')
            return redirect(url_for('home.upload_picture'))
    return render_template('home/upload_picture.html',user=current_user,form=form)


@home.route('/disable_picture/<id>',methods=['GET'])
@login_required
@permission_required(Role.Manager)
def disable_picture(id):
    user = User.query.get(int(id))
    if user is None:
        flash(u'不存在的用户')
        return redirect(url_for('home.homepage',id=current_user.id))
    if current_user.id == user.id:
        flash(u'只能禁用其他用户的头像')
        return redirect(url_for('home.homepage',id=current_user.id))
    if user.verify_permission():
        flash(u'不能管理员的头像')
        return redirect(url_for('home.homepage',id=user.id))
    if not user.picture_disabled:
        user.picture_disabled = True
        db.session.add(user)
    return redirect(url_for('home.homepage',id=user.id))
        
        
@home.route('/able_picture/<id>',methods=['GET'])
@login_required
@permission_required(Role.Manager)
def able_picture(id):
    user = User.query.get(int(id))
    if user is None:
        flash(u'不存在的用户')
        return redirect(url_for('home.homepage',id=current_user.id))
    if current_user.id == user.id:
        flash(u'只能启用其他用户的头像')
        return redirect(url_for('home.homepage',id=current_user.id))
    if user.picture_disabled:
        user.picture_disabled = False
        db.session.add(user)
    return redirect(url_for('home.homepage',id=user.id))
    
