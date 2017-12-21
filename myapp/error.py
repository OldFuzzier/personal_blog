# coding=utf-8

# 这么写是为了避免相互导入
class ErrorHandler(object):

    def __init__(self, app):

        @app.errorhandler(404)
        def v_error(error):
            return 'im error', 404