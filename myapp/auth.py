# coding=utf-8

from flask import Blueprint, redirect, url_for, render_template, abort, request, flash
from flask_login import login_required, logout_user, current_user

from mainapp import db
from model import Category, Tag, User, Article
from utils import PostArticle, DeleteContent, count_see

auth = Blueprint('auth', __name__)


@auth.route('/post', methods=['GET', 'POST'])
@login_required
def v_post():
    if request.method == 'POST':
        try:
            title = request.form.get('title')
            content = request.form.get('content')
            category_options = request.form.getlist('option_list')
            tags_string = request.form.get('tag')
            personal_flag = request.form.get('personal_flag')
            user_id = current_user.id
            # 测试post获取到的数据
            # print 'title:%s\ncontent:%s\ncategory_options:%s\ntag_options:%s\npersonal_flag:%s' % \
            #        (title, content, category_options, tags_string, personal_flag)
            pa = PostArticle(db, title=title, content=content, category_options=category_options,
                             tags_string=tags_string,personal_flag=personal_flag,
                             Tag=Tag, Category=Category, Article=Article, user_id=user_id)
            pa.post()
            flash('Post Success!')
        except Exception as e:
            print e
            flash('Post Failed !')
        return redirect(url_for('main.v_index'))
    category_list = Category.query.with_entities(Category.category_name).all()  # 取出所有分类名
    return render_template('post.html', category_list=category_list)


@auth.route('/editaticle/<name>', methods=['GET', 'POST'])
@login_required
def v_editarticle(name):
    if request.method == 'POST':
        try:
            title = request.form.get('title')
            content = request.form.get('content')
            category_options = request.form.getlist('option_list')
            tags_string = request.form.get('tag')
            personal_flag = request.form.get('personal_flag')
            user_id = current_user.id
            pa = PostArticle(db, title=title, content=content, category_options=category_options,
                             tags_string=tags_string,personal_flag=personal_flag,
                             Tag=Tag, Category=Category, Article=Article, user_id=user_id)
            pa.edit(name)
            flash('Edit Success!')
        except Exception as e:
            print e
            flash('Edit Failed !')
        return redirect(url_for('main.v_index'))
    article = Article.query.filter_by(title=name).first()  # 取出指定的article
    category_list = Category.query.with_entities(Category.category_name).all()  # 取出全部category
    article_tags_list = map(lambda tag: tag.tag_name, article.tags)
    article_categorys_list = map(lambda category: category.category_name, article.categorys)
    return render_template('edit_article.html', article=article, category_list=category_list,
                           article_tags_list=article_tags_list, article_categorys_list=article_categorys_list)


@auth.route('/delete/<name>')
@login_required
def v_delete(name):
    try:
        flag = request.args.get('flag')
        if flag == 'Article':
            obj = Article.query.filter_by(title=name).first()
            DeleteContent.article_clear(obj)
        elif flag == 'Tag':
            obj = Tag.query.filter_by(tag_name=name).first()
            DeleteContent.tag_clear(obj)
        elif flag == 'Category':
            obj = Category.query.filter_by(category_name=name).first()
            DeleteContent.category_clear(obj)
        else:
            raise Exception
        db.session.delete(obj)
        db.session.commit()
        flash('Delete %s success!' % flag)
        print flag
        return redirect(url_for('auth.v_arrange', flag=flag))
    except Exception as e:
        print e
        flash('Delete fail!')
        abort(404)


@auth.route('/management')
@login_required
def v_manage():
    user_id = current_user.id
    article_list = Article.query.filter_by(user_id=user_id).all()
    count = count_see(article_list)  # 计算出 see_times 的总数
    return render_template('management.html', total_see=count)


@auth.route('/management/<flag>')
@login_required
def v_arrange(flag):
    if flag == 'Tag':
        tag_list = Tag.query.all()
        new_tag_list = map(lambda tag: (tag.tag_name, len(tag.articles)), tag_list)
        return render_template('manage_tag.html', choice=flag, tag_list=new_tag_list)
    elif flag == 'Category':
        category_list = Category.query.all()
        new_category_list = map(lambda category: (category.category_name, len(category.articles)), category_list)
        return render_template('manage_category.html', choice=flag, category_list=new_category_list)
    elif flag == 'Article':
        user_id = current_user.id
        article_list = Article.query.with_entities(Article.title, Article.publish_time).\
            filter_by(user_id=user_id).all()
        return render_template('manage_archive.html', choice=flag, article_list=article_list)
    else:
        return abort(404)


@auth.route('/add_category', methods=['POST'])
@login_required
def v_add_ca():
    try:
        new_name = request.form.get('name')
        user_id = current_user.id
        ca = Category(category_name=new_name, user_id=user_id)
        db.session.add(ca)
        db.session.commit()
        return redirect(url_for('auth.v_arrange', flag='Category'))
    except Exception, e:
        print e
        abort(404)


@auth.route('/edit_ca_tag/<name>', methods=['GET', 'POST'])
@login_required
def v_edit_ca_tag(name):
    flag = request.args.get('flag')
    if request.method == 'POST':
        try:
            new_name = request.form.get('change')
            if flag == 'Category':
                ca = Category.query.filter_by(category_name=name).first()
                ca.category_name = new_name
            elif flag == 'Tag':
                tag = Tag.query.filter_by(tag_name=name).first()
                tag.tag_name = new_name
            else:
                raise Exception
            db.session.commit()
            flash('Edit %s success!' % flag)
            return redirect(url_for('auth.v_arrange', flag=flag))
        except Exception, e:
            print e
            flash('Edit %s failed' % flag)
            abort(404)
    return render_template('edit_ca_tag.html', name=name, choice=flag)


@auth.route('/logout')
@login_required
def v_logout():
    logout_user()
    return redirect(url_for('main.v_index'))

