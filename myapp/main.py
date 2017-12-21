# coding=utf-8
from flask import Blueprint, render_template

main = Blueprint('main', __name__)


@main.route('/')
def v_index():
    return render_template('index.html')


@main.route('/article')
def v_article():
    return render_template('article.html')


@main.route('/directory')
def v_category():
    return render_template('directory.html')


@main.route('/tag')
def v_tag():
    return render_template('tag.html')