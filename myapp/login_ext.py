# coding=utf-8

from functools import wraps
from flask import session, redirect, url_for


def login_require(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if session.get('user_id'):
            # print 'im %s' % session.get('user')
            return func(*args, **kwargs)
        else:
            return redirect(url_for('main.v_login'))
    return inner


def login_user(user):
    session['user_id'] = user.id
    return


def logout_user():
    session.pop('user_id')
    return
