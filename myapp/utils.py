# coding=utf-8

from collections import defaultdict

# 格式化articles
class FormatArticle(object):
    # 最后的格式为: {
    #     2017: [title, personal_flag, (day, month, year)],
    #     2018: [title, personal_flag, (day, month, year)],
    #     ...
    # }
    # 和提取全部年份格式 [..., 2018, 2017]

    def __init__(self):
        self.month_dict = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun',
                    7:'July', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}

    # 返回格式为tuple
    def format_date(self, date):
        date_tuple = (str(date.day), self.month_dict[date.month], str(date.year))
        return date_tuple

    def process(self, article_list):
        total_dict = defaultdict(list)
        year_set = set()
        for article_tuple in article_list:
            title = article_tuple[0]
            date = article_tuple[1]
            personal_flag = article_tuple[2]
            total_dict[date.year].append([title, personal_flag, self.format_date(date)])
            # 提取年份
            year_set.add(date.year)
        year_list = sorted(year_set, reverse=True)
        return year_list, total_dict


class PostArticle(object):

    def __init__(self, db, **kwargs):
        self._db = db
        self._article = kwargs.get('Article')
        self._user_id = kwargs.get('user_id')
        self._category = kwargs.get('Category')
        self._tag = kwargs.get('Tag')
        self.title = kwargs.get('title')
        self.content = kwargs.get('content')
        self.category_options = kwargs.get('category_options')
        self.tags_string = kwargs.get('tags_string')
        self.personal_flag = kwargs.get('personal_flag')

    def format_tags(self):
        tag_list = self.tags_string.split(';')
        return tag_list

    def add_tag(self, choice_tag):
        # 创建tag
        tag = self._tag(tag_name=choice_tag, user_id=self._user_id)  # 创建一个tag
        self._db.session.add(tag)
        self._db.session.commit()

    def post(self):
        if self.personal_flag:
            # 如果需要锁住文章
            article = self._article(title=self.title, content=self.content, user_id=self._user_id, personal_flag=1)
        else:
            # 不需要锁住文章
            article = self._article(title=self.title, content=self.content, user_id=self._user_id)
        if self.tags_string:
            # 如果有tag
            tag_list = self.format_tags()  # 将 string 的tags 变成序列
            tags_name_all = map(lambda tuple: tuple[0], self._tag.query.with_entities(self._tag.tag_name).all())
            for choice_tag in tag_list:
                if choice_tag not in tags_name_all:
                    # 判断这个tag在tag数据表中是否存在
                    # 如果不存在, 则先创建一个tag
                    self.add_tag(choice_tag)
                tagID = self._tag.query.filter_by(tag_name=choice_tag).first()
                article.tag_back.append(tagID)
        if self.category_options:
            # 如果有category
            for category_name in self.category_options:
                categoryID = self._category.query.filter_by(category_name=category_name).first()
                categoryID.article_back.append(article)
        # 最后将 article 添加, 并在数据库中存储
        self._db.session.add(article)
        self._db.session.commit()

    def clear_list(self, article, lst, flag=None):
        if flag == 'tag':
            for name in lst:
                tag_delete = self._tag.query.filter_by(tag_name=name).first()
                article.tag_back.remove(tag_delete)
        if flag == 'category':
            for name in lst:
                category_delete = self._category.query.filter_by(category_name=name).first()
                article.category_back.remove(category_delete)

    def edit(self, article_name):
        article = self._article.query.filter_by(title=article_name).first()
        article_have_tags = map(lambda tag: tag.tag_name, article.tags)  # 取出article的所有tag
        article_have_category = map(lambda category: category.category_name, article.categorys)

        if self.tags_string:
            # 如果有tag
            get_tag_list = self.format_tags()  # 将 string 的tags 变成序列
            tags_name_all = map(lambda tuple: tuple[0], self._tag.query.with_entities(self._tag.tag_name).all())
            for chosen_tag in get_tag_list:
                if chosen_tag not in tags_name_all:
                    # 判断这个tag在tag数据表中是否存在
                    # 如果不存在, 则先创建一个tag
                    self.add_tag(chosen_tag)
                if chosen_tag not in article_have_tags:
                    # 判读这个article的tag是否已经存在
                    tagID = self._tag.query.filter_by(tag_name=chosen_tag).first()
                    article.tag_back.append(tagID)
                else:
                    # 如果过chosen_tag已存在，就将这个tag从have_tag中删除
                    article_have_tags.remove(chosen_tag)
            if len(article_have_tags) > 0:
                # 判断是否还存在需要删除的tag
                for delete_tag in article_have_tags:
                    tagID = self._tag.query.filter_by(tag_name=delete_tag).first()
                    article.tag_back.remove(tagID)
        else:
            # 如果没有chosen_tag
            if len(article_have_tags) > 0:
                self.clear_list(article, article_have_tags, flag='tag')

        if self.category_options:
            # 如果有category
            for chosen_category in self.category_options:
                if chosen_category not in article_have_category:
                    categoryID = self._category.query.filter_by(category_name=chosen_category).first()
                    categoryID.article_back.append(article)
                else:
                    # 如果过chosen_category已存在，就将这个category从have_category中删除
                    article_have_category.remove(chosen_category)
            if len(article_have_category) > 0:
                # 判断是否还存在需要删除的category
                for delete_category in article_have_category:
                    categoryID = self._category.query.filter_by(category_name=delete_category).first()
                    categoryID.article_back.remove(article)
        else:
            # 如果没有chosen_category
            if len(article_have_category) > 0:
                self.clear_list(article, article_have_category, flag='category')

        if self.personal_flag:
            article.personal_flag = 1
        else:
            article.personal_flag = 0

        # 将article 的 tag 和 category 更新
        article.title = self.title
        article.content = self.content
        # 最后将 article 添加, 并在数据库中存储
        self._db.session.commit()


class DeleteContent(object):

    @staticmethod
    def article_clear(article):
        tag_length = len(article.tags)
        category_length = len(article.categorys)
        if tag_length > 0:
            for _ in range(tag_length):
                article.tags.pop()
        if category_length > 0:
            for _ in range(category_length):
                article.categorys.pop()
        del article.user_back

    @staticmethod
    def tag_clear(tag):
        article_length = len(tag.articles)
        if article_length > 0:
            for _ in range(article_length):
                tag.articles.pop()
        del tag.user_back

    @staticmethod
    def category_clear(category):
        article_length = len(category.articles)
        if article_length > 0:
            for _ in range(article_length):
                category.articles.pop()
        del category.user_back


# 计算 see_times 的次数
def count_see(article_list):
    count = 0
    for article in article_list:
        count += article.see_times
    return count




