# coding=utf-8
from flask import Blueprint, render_template, request, flash, redirect, url_for, abort

from mainapp import db
from model import User, Article, Tag, Category
from utils import FormatArticle
from flask_login import login_user, current_user

main = Blueprint('main', __name__)


@main.route('/')
def v_index():
    return render_template('index.html')


@main.route('/test')
def v_test():
    abort(404)
    return


@main.route('/archive')
def v_archive():
    article_list = Article.query.with_entities(Article.title, Article.publish_time, Article.personal_flag)\
        .order_by(Article.publish_time.desc()).all()
    year_list, article_dict = FormatArticle().process(article_list)
    return render_template('archive.html', year_list=year_list, article_dict=article_dict)


@main.route('/category')
def v_category():
    category_list = Category.query.with_entities(Category.category_name).all()
    return render_template('category.html', category_list=category_list)


@main.route('/category/<name>')
def v_ca_archive(name):
    category = Category.query.filter_by(category_name=name).first()
    article_list = category.articles
    return render_template('ca_tag_archive.html', name=name, article_list=article_list)


@main.route('/tag')
def v_tag():
    tag_list = Tag.query.with_entities(Tag.tag_name).all()
    return render_template('tag.html', tag_list=tag_list)


@main.route('/tag/<name>')
def v_tag_archive(name):
    tag = Tag.query.filter_by(tag_name=name).first()
    article_list = tag.articles
    return render_template('ca_tag_archive.html', name=name, article_list=article_list)


@main.app_template_filter('date_format')
def format_date(dt):
    dt_tuple = FormatArticle().format_date(dt)
    return '-'.join(dt_tuple)


@main.route('/detail/<title>')
def v_detail(title):
    article = Article.query.filter_by(title=title).first()
    user = current_user  # 获取当前 user
    if article.personal_flag == 1:  # 判断该article为私有文章
        if current_user:
            article.see_times += 1  # 访问次数加1
            db.session.commit()
            return render_template('detail.html', article=article, user=user)
        else:
            return redirect(url_for('main.v_login'))
    else:
        article.see_times += 1  # 访问次数加1
        db.session.commit()
        return render_template('detail.html', article=article, user=user)


@main.route('/aboutme')
def v_aboutme():
    return render_template('about_me.html')


@main.route('/login', methods=['GET', 'POST'])
def v_login():
    if request.method == 'POST':
        try:
            email = request.form.get('email')
            password = request.form.get('password')
            user = User.query.filter_by(email=email).first()
            if user:
                if user.allow_times > 5:
                    flash('The user has been locked !')
                    return redirect(url_for('main.v_index'))
                else:
                    if user.check_password(password):
                        login_user(user)  # 将user绑定到session上
                        next = request.args.get('next')
                        return redirect(url_for(next or 'auth.v_manage'))
                    else:
                        user.allow_times += 1
                        db.session.commit()
                        flash('You username or password error !')
            else:
                flash('You email not exist !')
                raise Exception
        except Exception, e:
            print e
            abort(404)
    return render_template('login.html')
