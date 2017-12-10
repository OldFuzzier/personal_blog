# coding=utf-8
import os
import sys

from flask import Flask, make_response, session, g, Blueprint, url_for, redirect

from db_middle import db
from model import Role, Permission

# 加载外目录中的文件
dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(dir_path)
from config import SECRET_KEY, PERMANENT_SESSION_LIFETIME, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS

app = Flask(__name__)

auth = Blueprint('auth', __name__)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS  # 不写这句总是警告
db.init_app(app)  # 应用中间件初始化

app.secret_key = SECRET_KEY  # secret_key需要24个字符的字符串
app.config['PERMANENT_SESSION_LIFETIME'] = PERMANENT_SESSION_LIFETIME



@app.route('/')
def v_index():
    session['name'] = 'www'
    return 'im index'


@app.route('/db_test')
def v_kobe():
    role1 = Role(role_name='admin')
    role2 = Role(role_name='normal')
    permission1 = Permission(level='allow_read')
    permission2 = Permission(level='allow_edit')
    # 向中间表添加数据 append方法
    role1.permissions_attr.append(permission1)
    role1.permissions_attr.append(permission2)
    role2.permissions_attr.append(permission1)
    role2.permissions_attr.append(permission2)

    db.session.add_all([role1, role2, permission1, permission2])
    db.session.commit()
    return 'db finish'


def login_require(func):
    def inner(*args, **kwargs):
        if session.get('name'):
            print 'im %s' % session.get('name')
            return func(*args, **kwargs)
        else:
            return redirect(url_for('auth.v_error'))
    return inner


@auth.route('/login')
@login_require
def v_auth():
    return 'im auth'


@auth.route('/error')
def v_error():
    return 'im error'



@auth.before_request
def blue_br():
    print 'im blue br'



app.register_blueprint(auth, url_prefix='/auth')





