# coding=utf-8

from myapp.model import Article, Tag, Category
from myapp.mainapp import app, db

with app.app_context():
    a = Article(title='hahahah', content='1234356', user_id=1)
    t = Tag.query.filter_by(id=1).first()
    c = Category.query.filter_by(id=1).first()
    a.tag_back.append(t)
    a.category_back.append(c)
    db.session.add(a)
    db.session.commit()




