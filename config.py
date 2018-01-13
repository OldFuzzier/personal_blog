# coding=utf-8
import os
from datetime import timedelta

# debug
DEBUG = True


# 数据库先关配置
SQLALCHEMY_DATABASE_URI = 'mysql://root:wt322426@localhost/myblog?charset=utf8'
SQLALCHEMY_TRACK_MODIFICATIONS = True


# session 的相关配置
SECRET_KEY = os.urandom(24)
PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
# flask_login 的相关配置
SESSION_PROTECTION = 'strong'
LOGIN_VIEW = 'main.v_login'
LOGIN_MESSAGE = 'design for yourself'
LOGIN_MESSAGE_CATEGORY = 'info'