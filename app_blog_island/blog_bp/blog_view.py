from datetime import datetime
from flask import flash, url_for, redirect, render_template, request,\
     current_app, session, make_response, abort
from flask.ext.login import login_user,logout_user, login_required,\
     current_user
from . import blog
from ..models import Permission, User, Article, Role, db
from ..decorators import permission_required
from .blog_form import EditArticleForm


@blog.route('/new_article',methods=['GET','POST'])
@login_required
@permission_required(Permission.WRITE_ARTICLES)
def new_article():
    form = EditArticleForm()
    if form.validate_on_submit():
        article = Article(user_id=current_user.id,subject=form.subject.data,body=form.body.data,
                          digest=form.digest.data)
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
    return render_template('blog/show_article.html',article=article)


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
    
        
             

