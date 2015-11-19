#coding:utf-8
from flask import redirect, url_for, render_template, flash
from flask.ext.login import login_required, current_user
from . import manage
from ..decorators import permission_required
from ..models import Permission, Role, User, User_Role_Relation, db
from .manage_form import UserSearchForm, UserModForm, \
         RoleChooseForm, RoleModForm


@manage.route('/user_search',methods=['GET','POST'])
@login_required
@permission_required(Role.S_Manager)
def user_search():
    form = UserSearchForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.input.data).first()
        if user is None:
            flash(u'找不到对应的用户，请确认输入正确')
            return redirect(url_for('manage.user_search'))
        if user.verify_permission():
            flash(u'不能对管理员执行该操作')
            return redirect(url_for('manage.user_search'))
        return redirect(url_for('manage.user_mod',id=user.id))
    return render_template('manage/user_search.html',form=form)


@manage.route('/user_mod/<id>',methods=['GET','POST'])
@login_required
@permission_required(Role.S_Manager)
def user_mod(id):
    form = UserModForm()
    user = User.query.get(int(id))
    role_user = Role.query.filter_by(rolename='User').first()
    role_manager = Role.query.filter_by(rolename='Manager').first()
    role_s_manager = Role.query.filter_by(rolename='S_Manager').first()
    row_user = User_Role_Relation.query.filter_by(user_id=user.id).\
                        filter_by(role_id=role_user.id).first()
    row_manager = User_Role_Relation.query.filter_by(user_id=user.id).\
                        filter_by(role_id=role_manager.id).first()
    row_s_manager = User_Role_Relation.query.filter_by(user_id=user.id).\
                        filter_by(role_id=role_s_manager.id).first()
    if form.validate_on_submit():
        if not form.user.data and not form.manager.data\
                 and not form.s_manager.data:
            flash(u'一个用户至少具有一个角色')
            return redirect(url_for('manage.user_mod',id=user.id))
        if form.user.data:
            if row_user is None:
                row_user = User_Role_Relation(user_id=user.id,role_id=role_user.id,
                                        operate_id=current_user.id)
                db.session.add(row_user)
        else:
            if row_user is not None:
                db.session.delete(row_user)
        #------------------------------------------
        if form.manager.data:
            if row_manager is None:
                row_manager = User_Role_Relation(user_id=user.id,role_id=role_manager.id,
                                        operate_id=current_user.id)
                db.session.add(row_manager)
        else:
            if row_manager is not None:
                db.session.delete(row_manager)
        #------------------------------------------
        if form.s_manager.data:
            if row_s_manager is None:
                row_s_manager = User_Role_Relation(user_id=user.id,role_id=role_s_manager.id,
                                        operate_id=current_user.id)
                db.session.add(row_s_manager)
        else:
            if row_s_manager is not None:
                db.session.delete(row_s_manager)
        #------------------------------------------
        user.banned = form.banned.data
        if not user.banned:
            user.ask_for_lift_ban = False
        db.session.add(user)
        flash(u'修改已生效')
        return redirect(url_for('manage.user_mod',id=user.id))
    form.banned.data = user.banned
    form.user.data = row_user is not None 
    form.manager.data = row_manager is not None
    form.s_manager.data = row_s_manager is not None
    return render_template('manage/user_mod.html',user=user,form=form)


@manage.route('/role_choose',methods=['GET','POST'])
@login_required
@permission_required(Role.S_Manager)
def role_choose():
    form = RoleChooseForm()
    if form.validate_on_submit():
        role = Role.query.filter_by(rolename=form.input.data).first()
        if role is None:
            flash(u'找不到对应的角色，请确认输入正确') 
            return redirect(url_for('manage.role_choose'))
        if (role.permissions & Permission.ADMINISTRATOR) == Permission.ADMINISTRATOR:
            flash(u'不能对管理员角色执行该操作')
            return redirect(url_for('manage.role_choose'))
        return redirect(url_for('manage.role_mod',id=role.id)) 
    roles = Role.query.filter(Role.rolename != 'Administrator').all()
    return render_template('manage/role_choose.html',form=form,roles=roles)


@manage.route('/role_mod/<id>',methods=['GET','POST'])
@login_required
@permission_required(Role.S_Manager)
def role_mod(id):
    form = RoleModForm()
    role = Role.query.get(int(id))
    if form.validate_on_submit():
        if not form.follow.data and not form.comment.data and not form.write_articles.data \
                    and not form.manage_comment.data and not form.manage_articles.data \
                    and not form.manage_homepage.data:
            flash(u'一个角色至少具有一项权限')
            return redirect(url_for('manage.role_mod',id=role.id))
        self_permission = Permission.INIT
        if form.follow.data:
            self_permission |= Permission.FOLLOW
        if form.comment.data:
            self_permission |= Permission.COMMENT
        if form.write_articles.data:
            self_permission |= Permission.WRITE_ARTICLES
        if form.manage_comment.data:
            self_permission |= Permission.MANAGE_COMMENT
        if form.manage_articles.data:
            self_permission |= Permission.MANAGE_ARTICLES
        if form.manage_homepage.data:
            self_permission |= Permission.MANAGE_HOMEPAGE
        role.permissions = self_permission
        db.session.add(role)
        flash(u'修改已生效')
        return redirect(url_for('manage.role_mod',id=role.id))
    form.follow.data = (role.permissions & Permission.FOLLOW) == Permission.FOLLOW
    form.comment.data = (role.permissions & Permission.COMMENT) == Permission.COMMENT
    form.write_articles.data = (role.permissions & Permission.WRITE_ARTICLES) == Permission.WRITE_ARTICLES
    form.manage_comment.data = (role.permissions & Permission.MANAGE_COMMENT) == Permission.MANAGE_COMMENT
    form.manage_articles.data = (role.permissions & Permission.MANAGE_ARTICLES) == Permission.MANAGE_ARTICLES
    form.manage_homepage.data = (role.permissions & Permission.MANAGE_HOMEPAGE) == Permission.MANAGE_HOMEPAGE
    return render_template('manage/role_mod.html',form=form,role=role)


