# coding=utf-8

from db_middle import db



class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    users_attr = db.relationship('Role', backref=db.backref('users'))

    def __str__(self):
        return '%s, %s' % (self.id, self.username)


class Info(db.Model):
    __tablename__ = 'info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), unique=True)
    content = db.Column(db.String(500))
    # 外键连接 一个User对应多个Info, 其中 'user.id ' 中的 user 是表名
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # backref 是定义反向引用，可以通过 User 的 instance.infos 访问这个模型所写的所有info
    infos_attr = db.relationship('User', backref=db.backref('infos'))

    def __str__(self):
        return '%s, %s, %s' % (self.id, self.title, self.content)


# 中间表
role_permission = db.Table('role_permission',
                           db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True),
                           db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'), primary_key=True)

)


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(100), unique=True)
    # backref 反向引用，注意 secondary 是中间表的参数
    permissions_attr = db.relationship('Permission', secondary=role_permission, backref=db.backref('permissions'))


class Permission(db.Model):
    __tablename__ = 'permission'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    level = db.Column(db.String(100), unique=True)

    permissions_attr = db.relationship('Role', secondary=role_permission, backref=db.backref('roles'))



