#coding:utf-8
import os
from app_blog_island.models import Permission


class config(object):
    SQLALCHEMY_DATABASE_URI = "mysql://blog:l315474244@localhost/blog_island"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True   #do "db.session.commit()" after every request
    SECRET_KEY = "blog island's secret key"
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USERNAME = os.environ['BLOG_ISLAND_MAIL_USERNAME']
    MAIL_PASSWORD = os.environ['BLOG_ISLAND_MAIL_PASSWORD']
    BLOG_ISLAND_MAIL_SUBJECT_PREFIX = '[博客岛]'
    BLOG_ISLAND_MAIL_SENDER = os.environ['BLOG_ISLAND_MAIL_SENDER']
    
jinja_environment = {'str':str,'Permission':Permission}
