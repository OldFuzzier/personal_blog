# coding=utf-8
import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flaskext.markdown import Markdown
from flask_login import LoginManager


# 加载外目录中的配置文件
dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(dir_path)
from config import SECRET_KEY, PERMANENT_SESSION_LIFETIME, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS,\
    SESSION_PROTECTION, LOGIN_VIEW

app = Flask(__name__)

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS  # 不写这句总是警告
db = SQLAlchemy()
db.init_app(app)  # 应用中间件初始化

#init markdown
Markdown(app, output_format='html5')

# 配置session
app.secret_key = SECRET_KEY  # secret_key需要24个字符的字符串
app.config['PERMANENT_SESSION_LIFETIME'] = PERMANENT_SESSION_LIFETIME

# init flask_login
login_manager = LoginManager()
login_manager.session_protection = SESSION_PROTECTION
login_manager.login_view = LOGIN_VIEW
login_manager.init_app(app)


# 注册auth蓝图
from main import main as main_blueprint
app.register_blueprint(main_blueprint)
from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')

# 处理请求error
from error import ErrorHandler
ErrorHandler(app)





