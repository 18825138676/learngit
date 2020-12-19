from flask import request, jsonify

from api import db
from api.models import Books
from api.modules.books import books_blu


@books_blu.route('/books',methods=['GET','POST'])
def books():
    '''
    获取书籍列表 GET
    增加一本书 POST
    :return:
    '''
    if request.method=='GET':
        books=Books.query.filter(Books.status=='1').all()

        return jsonify(code=200,msg='获取列表成功',data=[i.to_dict() for i in books])


    data_dict=request.json
    name=data_dict.get('name')
    category=data_dict.get('category')
    price=data_dict.get('price')

    book=Books()
    book.name=name
    book.category=category
    book.price=price


    try:
        db.session.add(book)
        db.session.commit()

    except Exception as e:
        return jsonify(code=400,msg='数据更新失败')

    return jsonify(code=200,msg='获取列表成功', data=book.to_dict())

@books_blu.route('/books/<int:book_id>',methods=['POST','DELETE'])
def book(book_id):
    '''
    POST 更新指定书籍信息
    DELETE 删除指定书籍

    :param book_id:
    :return:
    '''

    if request.method=='DELETE':
        book=Books.query.get(book_id)
        if not book:
            return jsonify(code=400,msg='查无此书')
        if book.status=='0':
            return jsonify(code=400,msg='此书已删除')
        book.status=0

        try:
            db.session.add(book)
            db.session.commit()
        except Exception as e:
            return jsonify(code=400, msg='数据更新失败')

        return jsonify(code=200,msg='删除成功')

    data_dict=request.json
    book=Books.query.get(book_id)

    if not book:
        return jsonify(code=400,msg='查无此书')
    if book.status=='0':
        return jsonify(code=400,msg='此书已删除')

    book.category=data_dict.get('category')
    book.price=data_dict.get('price')

    try:
        db.session.add(book)
        db.session.commit()
    except Exception as e:
        return jsonify(code=400,msg='数据更新失败')
    return jsonify(code=200,msg='更新成功',data=book.to_dict())





