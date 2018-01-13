# coding=utf-8

from flask import render_template

# 这么写是为了避免相互导入
class ErrorHandler(object):

    def __init__(self, app):

        @app.errorhandler(404)
        def v_error(error):
            return render_template('error.html'), 404

