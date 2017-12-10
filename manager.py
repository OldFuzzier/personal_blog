# coding=utf-8

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from myapp.mainapp import app
from myapp.db_middle import db
from myapp.model import User, Info  # 需要将需要的model导入，以便MigrateCommand调用

manager = Manager(app)

# 1 先将app和db绑定
migrate = Migrate(app, db)

# 把 MigrateCommand 命令添加到 manager 中
# db_manager 和 MigrateCommand 道理一样
manager.add_command('db', MigrateCommand)


@manager.command
def runserver():
    app.run(host='127.0.0.1', debug=True)


# 调用runserver命令行 python manager.py runserver
# 调用db的命令行 python manager.py db db_init


if __name__ == '__main__':
    manager.run()
