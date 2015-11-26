#coding:utf-8
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class EditArticleForm(Form):
    subject = StringField(u'标题：',validators=[Length(1,120,message=u'标题不为空或太长')])
    body = TextAreaField(u'正文：',validators=[Length(1,50000,message=u'正文不为空或太长')])
    digest = TextAreaField(u'摘要：',validators=[Length(0,200,message=u'摘要太长')])
    submit = SubmitField(u'保存')


class CommentForm(Form):
    comment = StringField(u'评论：',validators=[Length(1,280,message=u'评论不为空或太长')])
    submit = SubmitField(u'提交评论')
    
