
from flask import jsonify, request
from flask_restful import Resource

from rest_api.models import Books


class BooksViews(Resource):
    def get(self):
        books = Books.query.filter(Books.status == '1').all()

        return jsonify(code=200, msg='获取列表成功', data=[i.to_dict() for i in books])

    def post(self):
        data_dict = request.json
        name = data_dict.get('name')
        category = data_dict.get('category')
        price = data_dict.get('price')

        book = Books()
        book.name = name
        book.category = category
        book.price = price
        from rest_api import db

        try:
            db.session.add(book)
            db.session.commit()
        except Exception as e:
            return jsonify(code=400, msg='数据跟新失败')

        return jsonify(code=200, msg='添加书籍成功', data=book.to_dict())


class BookViews(Resource):

    def get(self, book_id):

        book = Books.query.get(book_id)
        if not book:
            return jsonify(code=400, msg='CHAWUCISHU ')

        return jsonify(code=200, msg='查询书籍成功', data=book.to_dict())

    def put(self, book_id):
        data_dict = request.json
        book = Books.query.get(book_id)
        if not book:
            return jsonify(code=400, msg="查无此书")
        if book.status == '0':
            return jsonify(code=400, msg="此书已删除")
        book.category = data_dict.get('category')
        book.price = data_dict.get('price')
        from rest_api import db

        try:
            db.session.add(book)
            db.session.commit()
        except Exception as e:
            return jsonify(code=400, msg='数据跟新失败')
        return jsonify(code=200, msg='更新成功', data=book.to_dict())

    def delete(self, book_id):
        book = Books.query.get(book_id)
        if not book:
            return jsonify(code=400, msg="查无此书")
        if book.status == '0':
            return jsonify(code=400, msg="此书已删除")
        book.status = '0'
        from rest_api import db

        try:
            db.session.add(book)
            db.session.commit()
        except Exception as e:
            return jsonify(code=400, msg='数据跟新失败')
        return jsonify(code=200, msg='删除成功')
