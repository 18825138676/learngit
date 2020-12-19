# @Time    : 2020-11-12 22:23
# @Author  : 老赵
# @File    : resource.py
from flask_restful import Api

from rest_api.api.books.books import BooksViews, BookViews
from rest_api.api.passport.passport import LoginViews, RegViews

api = Api()

api.add_resource(BooksViews, '/v1/books')
api.add_resource(BookViews, '/v1/books/<int:book_id>')

api.add_resource(LoginViews, '/v1/passport/login')
api.add_resource(RegViews, '/v1/passport/register')