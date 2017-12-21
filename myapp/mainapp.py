# coding=utf-8
import os
import sys

from flask import Flask, Blueprint, session, url_for, redirect
from flask_sqlalchemy import SQLAlchemy


# 加载外目录中的配置文件
dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(dir_path)
from config import SECRET_KEY, PERMANENT_SESSION_LIFETIME, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS

app = Flask(__name__)

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS  # 不写这句总是警告
db = SQLAlchemy()
db.init_app(app)  # 应用中间件初始化

# 配置session
app.secret_key = SECRET_KEY  # secret_key需要24个字符的字符串
app.config['PERMANENT_SESSION_LIFETIME'] = PERMANENT_SESSION_LIFETIME

# 注册auth蓝图
from main import main as main_blueprint
app.register_blueprint(main_blueprint)
from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')

# 处理请求error
from error import ErrorHandler
ErrorHandler(app)





