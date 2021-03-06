# -*- coding: utf-8 -*-

from flask import url_for, abort

from leancloud import Object
from leancloud import Query
from leancloudbb.utils.helpers import slugify

__author__ = 'pan'

class Forum(Object):
    @property
    def category(self):
        return self.get("category").fetch()

    @property
    def title(self):
        return self.get("title")

    @property
    def description(self):
        return self.get("description")

    @property
    def position(self):
        return self.get("position")

    @property
    def locked(self):
        return self.get("locked")

    @property
    def show_moderators(self):
        return self.get("show_moderators")

    @property
    def external(self):
        return self.get("external")

    @property
    def post_count(self):
        return self.get("post_count")

    @property
    def topic_count(self):
        return self.get("topic_count")

    @property
    def last_post(self):
        return self.get("last_post").fetch()


class Category(Object):
    @property
    def title(self):
        return self.get("title")

    @property
    def description(self):
        return self.get("description")

    @property
    def position(self):
        return self.get("position")

    # Properties
    @property
    def slug(self):
        """Returns a slugified version from the category title"""
        return slugify(self.title)

    @property
    def url(self):
        """Returns the slugified url for the category"""
        return url_for("forum.view_category", category_id=self.id,
                       slug=self.slug)

    def delete(self, users=None):
        """Deletes a category. If a list with involved user objects is passed,
        it will also update their post counts

        :param users: A list with user objects
        """

        # and finally delete the category itself
        self.destroy()

        # Update the users post count
        # todo 等创建了post再来写这里
        # if users:
        #     for user in users:
        #         user.post_count = Post.query.filter_by(user_id=user.id).count()
        #         db.session.commit()
        return self

    # Methods
    def __repr__(self):
        return "<{} {}>".format(self.title, self.id)

    # Classmethods
    @classmethod
    def get_all(cls):
        """Get all categories with all associated forums.
        It returns a list with tuples. Those tuples are containing the category
        and their associated forums (whose are stored in a list).

        For example::

            [(<Category 1>, [(<Forum 2>, <ForumsRead>), (<Forum 1>, None)]),
             (<Category 2>, [(<Forum 3>, None), (<Forum 4>, None)])]

        :param user: The user object is needed to check if we also need their
                     forumsread object.
        """

        return Query(cls).find()
