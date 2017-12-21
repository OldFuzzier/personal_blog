# coding=utf-8
from functools import wraps

from flask import Blueprint, session, redirect, url_for, render_template, abort

auth = Blueprint('auth', __name__)


def login_require(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if session.get('name'):
            print 'im %s' % session.get('name')
            return func(*args, **kwargs)
        else:
            return abort(404)
    return inner


@auth.route('/management')
@login_require
def v_management():
    return render_template('management.html')



@auth.route('/login')
@login_require
def v_auth():
    return 'im auth'



@auth.before_request
def blue_br():
    print 'im blue br'