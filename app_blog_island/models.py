from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin, AnonymousUserMixin
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from . import db, login_manager


class Permission(object):
    INIT = 0x00             #00000000
    FOLLOW = 0x01           #00000001
    COMMENT = 0x02          #00000010
    WRITE_ARTICLES = 0x04   #00000100
    MANAGE_COMMENT = 0x08   #00001000
    MANAGE_ARTICLES = 0x10  #00010000
    MANAGE_HOMEPAGE = 0x20  #00100000
    MANAGE_AUTH = 0x40      #01000000
    ADMINISTRATOR = 0x80    #10000000 


class User_Role_Relation(db.Model):
    __tablename__ = 'user_role_relation'
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),
                    primary_key=True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'),
                    primary_key=True)
    operate_id = db.Column(db.Integer,db.ForeignKey('users.id'),
                    nullable=True)
    operate_time = db.Column(db.DateTime,default=datetime.utcnow,index=True)


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    subject = db.Column(db.String(128),nullable=False)
    body =  db.Column(db.UnicodeText,nullable=False)
    digest = db.Column(db.UnicodeText,nullable=False)
    disabled = db.Column(db.Boolean,default=False)
    publish_time = db.Column(db.DateTime,default=datetime.utcnow,index=True)
    edit_time = db.Column(db.DateTime,default=datetime.utcnow)


class User(db.Model,UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(50),unique=True,nullable=False)
    email = db.Column(db.String(80),unique=True,nullable=False)
    password_hash = db.Column(db.String(100),nullable=False)
    picture_url = db.Column(db.String(120))
    picture_disabled = db.Column(db.Boolean,default=False)
    about_me = db.Column(db.UnicodeText)
    about_me_disabled = db.Column(db.Boolean,default=False)
    confirmed = db.Column(db.Boolean,default=False)
    register_time = db.Column(db.DateTime(),default=datetime.utcnow)
    last_login_time = db.Column(db.DateTime(),default=datetime.utcnow)
    user_role_relation = db.relationship('User_Role_Relation',backref='user',
        lazy='dynamic',foreign_keys=[User_Role_Relation.user_id])
    operate_role_relation = db.relationship('User_Role_Relation',backref='operater',
        lazy='dynamic',foreign_keys=[User_Role_Relation.operate_id])
    article = db.relationship('Article',backref='user',
        lazy='dynamic',foreign_keys=[Article.user_id])
    banned = db.Column(db.Boolean,default=False)
    ask_for_lift_ban = db.Column(db.Boolean,default=False)

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self,expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm':self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except Exception:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def active(self):
        self.last_login_time = datetime.utcnow()
        db.session.add(self)

    def generate_reset_token(self,email,password=None,expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'email':email,'id':self.id,'password':password})

    def confirm_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except Exception:
            return False
        if data.get('id') != self.id:
            return False
        self.email = data.get('email')
        db.session.add(self)
        return True

    @staticmethod
    def confirm_reset_email(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except Exception:
            return False
        user = User.query.filter_by(email=data.get('email')).first()
        if user is None:
            return False
        user.password = data.get('password')
        db.session.add(user)
        return True

    def verify_permission(self,permission=Permission.ADMINISTRATOR):
        rows = User_Role_Relation.query.filter_by(user_id=self.id).all()
        self_permission = Permission.INIT
        for row in rows:
            self_permission |= row.role.permissions
        if (self_permission & permission) == permission:
            can = True
        else:
            can = False
        if self.banned:
            can = False
        if (self_permission & Permission.ADMINISTRATOR) == Permission.ADMINISTRATOR:
            can = True
        return can

    def __repr__(self):
        return '<User %r>' % self.username


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    rolename = db.Column(db.String(60),unique=True)
    permissions = db.Column(db.Integer)
    role_user_relation = db.relationship('User_Role_Relation',backref='role',
        lazy='dynamic',foreign_keys=[User_Role_Relation.role_id])
    User = (Permission.FOLLOW | Permission.COMMENT |
            Permission.WRITE_ARTICLES)
    Manager = (Permission.MANAGE_COMMENT |
               Permission.MANAGE_ARTICLES |
               Permission.MANAGE_HOMEPAGE)
    S_Manager = (Permission.MANAGE_COMMENT |
                 Permission.MANAGE_ARTICLES |
                 Permission.MANAGE_HOMEPAGE |
                 Permission.MANAGE_AUTH)
    Administrator = Permission.ADMINISTRATOR

    @staticmethod
    def init_roles():
        roles = {
            'User': Role.User,
            'Manager': Role.Manager,
            'S_Manager': Role.S_Manager,
            'Administrator': Permission.ADMINISTRATOR
        }
        for role in roles:
            r = Role.query.filter_by(rolename=role).first()
            if r is None:
                r = Role(rolename=role)
            r.permissions = roles[role]
            db.session.add(r)
        db.session.commit()
    
    def __repr__(self):
        return '<Role %r>' % self.rolename


class AnonymousUser(AnonymousUserMixin):
    def verify_permission(self,permission=0x00):
        return False
    def is_active():
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


def init_db():
    if not Role.query.all():
        Role.init_roles()
    else:
        raise RuntimeError('Some Data Is In Table <User_Role_Relation>')
