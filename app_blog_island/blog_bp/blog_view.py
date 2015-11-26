#coding:utf-8
from datetime import datetime
from flask import flash, url_for, redirect, render_template, request,\
     current_app, session, make_response, abort
from flask.ext.login import login_user,logout_user, login_required,\
     current_user
from . import blog
from ..models import Permission, User, Article, Role, db, Comment
from ..decorators import permission_required
from .blog_form import EditArticleForm, CommentForm


@blog.route('/new_article',methods=['GET','POST'])
@login_required
@permission_required(Permission.WRITE_ARTICLES)
def new_article():
    form = EditArticleForm()
    if form.validate_on_submit():
        digest = ''
        if form.digest.data == '':
            digests = form.body.data[:150]
        article = Article(user_id=current_user.id,subject=form.subject.data,body=form.body.data,
                          digest=digests)
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('blog.show_article',username=article.user.username,id=article.id))
    return render_template('blog/new_article.html',form=form)
        
    
@blog.route('/<username>/<id>',methods=['GET','POST'])
def show_article(username,id):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    article = Article.query.get(int(id))
    if article is None:
        abort(404)
    if current_user.is_authenticated and  current_user.id != user.id:
        article.page_view += 1
        db.session.add(article)
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.filter_by(article_id=article.id).order_by(Comment.timesamp.desc()).paginate(
        page, per_page=current_app.config['BLOG_ISLAND_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items

    form = CommentForm() 
    if form.validate_on_submit():
        new_comment = Comment(user_id=current_user.id,article_id=article.id,
                               comment=form.comment.data)
        db.session.add(new_comment)
        return redirect(url_for('blog.show_article',username=user.username,id=article.id) + '#comment')
    return render_template('blog/show_article.html',article=article,comments=comments,
                           pagination=pagination,form=form)


@blog.route('/disable_article/<int:id>',methods=['GET'])
@login_required
@permission_required(Permission.MANAGE_ARTICLES)
def disable_article(id):
    article = Article.query.get_or_404(int(id))
    if article.disabled:
        flash(u'不能对已封禁的博文执行封禁操作')
        return redirect(url_for('blog.show_article',username=article.user.username,id=article.id))
    article.disabled = True
    db.session.add(article)
    return redirect(url_for('blog.show_article',username=article.user.username,id=article.id))
    

@blog.route('/able_article/<int:id>',methods=['GET'])
@login_required
@permission_required(Permission.MANAGE_ARTICLES)
def able_article(id):
    article = Article.query.get_or_404(int(id))
    if not article.disabled:
        flash(u'不能对未封禁的博文执行解封操作')
        return redirect(url_for('blog.show_article',username=article.user.username,id=article.id))
    article.disabled = False
    db.session.add(article)
    return redirect(url_for('blog.show_article',username=article.user.username,id=article.id))
    

@blog.route('/disable_comment/<int:id>',methods=['GET'])
@login_required
@permission_required(Permission.MANAGE_COMMENT)
def disable_comment(id):
    comment = Comment.query.get_or_404(int(id))
    if comment.disabled:
        flash(u'不能对已封禁的评论执行封禁操作')
        return redirect(url_for('blog.show_article',username=comment.user.username,id=comment.article.id) + '#comment')
    comment.disabled = True
    db.session.add(comment)
    return redirect(url_for('blog.show_article',username=comment.user.username,id=comment.article.id) + '#comment')
    

@blog.route('/able_comment/<int:id>',methods=['GET'])
@login_required
@permission_required(Permission.MANAGE_COMMENT)
def able_comment(id):
    comment = Comment.query.get_or_404(int(id))
    if not comment.disabled:
        flash(u'不能对未封禁的评论执行解封操作')
        return redirect(url_for('blog.show_article',username=comment.user.username,id=comment.article.id) + '#comment')
    comment.disabled = False
    db.session.add(comment)
    return redirect(url_for('blog.show_article',username=comment.user.username,id=comment.article.id) + '#comment')
    

@blog.route('/all',methods=['GET'])
def show_articles():
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.publish_time.desc()).paginate(
        page, per_page=current_app.config['BLOG_ISLAND_ARTICLES_PER_PAGE'],
        error_out=False)
    articles = pagination.items
    return render_template('blog/show_articles.html', articles=articles,
            pagination=pagination)


@blog.route('/edit/<id>',methods=['GET','POST'])
@login_required
@permission_required(Permission.WRITE_ARTICLES)
def edit_article(id):
    form = EditArticleForm()
    article = Article.query.get(int(id))
    if article is None:
        abort(404)
    if form.validate_on_submit():
        article.subject = form.subject.data
        article.body = form.body.data
        article.digest = form.digest.data
        article.edit_time = datetime.utcnow()
        db.session.add(article)
        return redirect(url_for('blog.show_article',username=article.user.username,id=article.id))
    form.subject.data = article.subject
    form.body.data = article.body
    form.digest.data = article.digest
    return render_template('blog/edit_article.html',form=form)
    
        
             

