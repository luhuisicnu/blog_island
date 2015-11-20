#coding:utf-8
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired, Email,EqualTo



class FileUploadForm(Form):
    file = FileField(u'照片路径：',validators=[DataRequired(message=u'照片路径不能为空')])
    submit = SubmitField(u'上传照片')
