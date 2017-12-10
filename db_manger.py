# coding=utf-8

# 创建一个db的命名行

from flask_script import Manager

from myapp.mainapp import db
from myapp.model import People, Info  # create 和 drop 必须导入model

db_manager = Manager()


@db_manager.command
def db_init():
    db.create_all()
    print 'db init'
    return


@db_manager.command
def db_drop():
    choice = int(raw_input('are sure to drop db?\n1.no\n2.yes'))
    if choice == 2:
        db.drop_all()
        print 'db drop'
    else:
        print 'nothing doing'
    return
