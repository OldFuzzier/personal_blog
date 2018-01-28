# coding=utf-8
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from mainapp import db, login_manager


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    allow_times = db.Column(db.Integer, default=0, nullable=False)  # 容错率为5

    # 目的是在User对象初始化的时候进行操作
    def __init__(self, *args, **kwargs):
        self.email = kwargs.get('email')
        self.username = kwargs.get('username')
        self.password = generate_password_hash(kwargs.get('password'))  # 对密码部分进行hash加密

    # 检查密码的函数
    def check_password(self, password):
        return check_password_hash(self.password, password)


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
    content = db.Column(db.String(20000), nullable=False)
    publish_time = db.Column(db.DateTime, default=datetime.now, nullable=False)
    see_times = db.Column(db.Integer, default=1, nullable=False)
    # 个人隐私文章flag
    personal_flag = db.Column(db.Integer, default=0)
    # 外键连接 一个User对应多个Info, 其中 'user.id ' 中的 user 是表名
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # backref 是定义反向引用，可以通过 User 的 instance.infos 访问这个模型所写的所有info
    user_back = db.relationship('User', backref=db.backref('articles'))
    tag_back = db.relationship('Tag', secondary=article_tag, passive_deletes=True,
                               backref=db.backref('articles'))
    category_back = db.relationship('Category', secondary=article_category,
                                    # 其中 passive_delete 支持多对多表关联删除，否则会报错！
                                    passive_deletes=True, backref=db.backref('articles'))

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

    user_back = db.relationship('User', backref=db.backref('categorys'))
    article_back = db.relationship('Article', secondary=article_category, backref=db.backref('categorys'))


# 回调函数，返回user对象
@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


