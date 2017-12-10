# coding=utf-8
import os
from datetime import timedelta

DEBUG = True

SECRET_KEY = os.urandom(24)
PERMANENT_SESSION_LIFETIME = timedelta(seconds=50)

SQLALCHEMY_DATABASE_URI = 'mysql://root:wt322426@localhost/infomation?charset=utf8'
SQLALCHEMY_TRACK_MODIFICATIONS = True