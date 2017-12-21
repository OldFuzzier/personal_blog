# coding=utf-8
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from db_middle import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    allow = db.Column(db.Integer)  # 判断用户是否被禁

    role_back = db.relationship('Role', backref=db.backref('users'))

    # 目的是在User对象初始化的时候进行操作
    def __init__(self, *args, **kwargs):
        self._id = kwargs.get('email')
        self._username = kwargs.get('username')
        self._passwrod = generate_password_hash(kwargs.get('password'))  # 对密码部分进行hash加密
        self._allow = kwargs.get('allow')
        self._role_id = kwargs.get('role_id')

    # 检查密码的函数
    def check_password(self, password):
        return check_password_hash(self._passwrod, password)

    def __str__(self):
        return '%s, %s' % (self.id, self.username)


# Article_Tag的中间表
article_tag = db.Table('article_tag',
              db.Column('article_id', db.Integer, db.ForeignKey('article.id'), primary_key=True),
              db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
              )


# Article_Category的中间表
article_category = db.Table('article_category',
                   db.Column('article_id', db.Integer, db.ForeignKey('article.id'), primary_key=True),
                   db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
                   )


# 用户发布的文章
class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    publish_time = db.Column(db.DateTime, default=datetime.now)
    # 外键连接 一个User对应多个Info, 其中 'user.id ' 中的 user 是表名
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # backref 是定义反向引用，可以通过 User 的 instance.infos 访问这个模型所写的所有info
    user_back = db.relationship('User', backref=db.backref('articles'))
    tag_back = db.relationship('Tag', secondary=article_tag, backref=db.backref('articles'))
    category = db.relationship('Category', secondary=article_category, backref=db.backref('articles'))

    def __str__(self):
        return '%s, %s, %s' % (self.id, self.title, self.content)


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user_back = db.relationship('User', backref=db.backref('tags'))
    article_back = db.relationship('Article', secondary=article_tag, backref=db.backref('tags'))


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    directory_id = db.Column(db.Integer, db.ForeignKey('directory.id'), nullable=False)

    user_back = db.relationship('User', backref=db.backref('categorys'))
    directory_back = db.relationship('directoty', backref=db.backref('categotys'))
    article_back = db.relationship('Article', secondary=article_category, backref=db.backref('categorys'))


class Directory(db.Model):
    __tablename__ = 'directory'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    directory_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)




