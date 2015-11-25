#coding:utf-8
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bootstrap import Bootstrap
from flask.ext.login import LoginManager
from flask.ext.mail import Mail
from flask.ext.moment import Moment

db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
mail = Mail()
moment = Moment()

login_manager.login_view='auth.login'
login_manager.session_protection = 'strong'
login_manager.login_message = u'请先登录'


def create_app(config_name,jinja_environment):
    app = Flask(__name__)
    app.config.from_object(config_name)
    for key in jinja_environment.keys():
        app.jinja_env.globals[key] = jinja_environment[key]

    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    moment.init_app(app)

    from .main_bp import main
    app.register_blueprint(main)

    from .auth_bp import auth
    app.register_blueprint(auth,url_prefix='/auth')

    from .home_bp import home
    app.register_blueprint(home,url_prefix='/home')

    from .manage_bp import manage
    app.register_blueprint(manage,url_prefix='/manage')

    from .blog_bp import blog
    app.register_blueprint(blog,url_prefix='/blog')

    return app

