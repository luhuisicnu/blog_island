#coding:utf-8
import os, os.path
from flask import flash, url_for, redirect, render_template, abort,\
        request, current_app
from flask.ext.login import login_required, current_user
from . import home
from .home_form import FileUploadForm, AboutMeForm
from ..models import User, Role, Permission, db, Article, Follow
from ..decorators import permission_required
from ..functions import random_str


@home.route('/<id>')
def homepage(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        abort(404)
    page = request.args.get('page', 1, type=int)
    pagination = user.article.order_by(Article.publish_time.desc()).paginate(
        page, per_page=current_app.config['BLOG_ISLAND_ARTICLES_PER_PAGE'],
        error_out=False)
    articles = pagination.items
    return render_template('home/homepage.html', user=user, articles=articles,
            pagination=pagination)


@home.route('/upload_picture',methods=['GET','POST'])
@login_required
@permission_required(Role.User)
def upload_picture():
    form = FileUploadForm()
    if form.validate_on_submit():
        picture_path = os.path.join(current_app.root_path, 'static/picture/')
        static_path = current_app.static_folder
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
        flash(u'不能禁用管理员的头像')
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
    

@home.route('/edit_about_me',methods=['GET','POST'])
@login_required
@permission_required(Role.User)
def edit_about_me():
    form = AboutMeForm()
    if form.validate_on_submit():
        current_user.about_me = form.about_me.data
        return redirect(url_for('home.homepage',id=current_user.id))
    form.about_me.data = current_user.about_me
    return render_template('home/edit_about_me.html',user=current_user,form=form)


@home.route('/disable_about_me/<id>',methods=['GET'])
@login_required
@permission_required(Role.Manager)
def disable_about_me(id):
    user = User.query.get(int(id))
    if user is None:
        flash(u'不存在的用户')
        return redirect(url_for('home.homepage',id=current_user.id))
    if current_user.id == user.id:
        flash(u'只能禁用其他用户的个人简介')
        return redirect(url_for('home.homepage',id=current_user.id))
    if user.verify_permission():
        flash(u'不能禁用管理员的个人简介')
        return redirect(url_for('home.homepage',id=user.id))
    if not user.about_me_disabled:
        user.about_me_disabled = True
        db.session.add(user)
    return redirect(url_for('home.homepage',id=user.id))
        
        
@home.route('/able_about_me/<id>',methods=['GET'])
@login_required
@permission_required(Role.Manager)
def able_about_me(id):
    user = User.query.get(int(id))
    if user is None:
        flash(u'不存在的用户')
        return redirect(url_for('home.homepage',id=current_user.id))
    if current_user.id == user.id:
        flash(u'只能启用其他用户的个人简介')
        return redirect(url_for('home.homepage',id=current_user.id))
    if user.about_me_disabled:
        user.about_me_disabled = False
        db.session.add(user)
    return redirect(url_for('home.homepage',id=user.id))


@home.route('/follow/<int:id>',methods=['GET'])
@login_required
@permission_required(Permission.FOLLOW)
def follow(id):
    user = User.query.get_or_404(int(id))
    fans = Follow.query.filter_by(star_id=user.id).\
                        filter_by(fans_id=current_user.id).first()
    if fans is None:
        fans = Follow(star_id=user.id,fans_id=current_user.id)
        db.session.add(fans)
        flash(u'关注成功')
    else:
        flash(u'不能重复关注')
    return redirect(url_for('home.homepage',id=user.id))


@home.route('/unfollow/<int:id>',methods=['GET'])
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(id):
    user = User.query.get_or_404(int(id))
    fans = Follow.query.filter_by(star_id=user.id).\
                        filter_by(fans_id=current_user.id).first()
    if fans is not None:
        db.session.delete(fans)
        flash(u'取消关注成功')
    else:
        flash(u'不能对未关注的用户取消关注')
    return redirect(url_for('home.homepage',id=user.id))


@home.route('/<int:id>/stars',methods=['GET'])
def show_stars(id):
    user = User.query.get_or_404(int(id))
    stars = []
    for star_relationship in user.star_relation.all():
        star = star_relationship.star
        if user.id != star.id:
            stars.append(star)
    if not stars:
        flash(u'该用户未关注其他用户')
        return redirect(url_for('home.homepage',id=user.id))
    return render_template('home/follow.html',head=user.username + u'关注的人',follows=stars)


@home.route('/<int:id>/fans',methods=['GET'])
def show_fans(id):
    user = User.query.get_or_404(int(id))
    fans = []
    for fan_relationship in user.fans_relation.all():
        fan = fan_relationship.fans
        if user.id != fan.id:
            fans.append(fan)
    if fans == []:
        flash(u'该用户还没有被关注')
        return redirect(url_for('home.homepage',id=user.id))
    return render_template('home/follow.html',head=user.username + u'的粉丝',follows=fans)


