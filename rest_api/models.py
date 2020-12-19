# @Time    : 2020-11-12 22:18
# @Author  : 老赵
# @File    : models.py
from rest_api import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mobile = db.Column(db.String(16), unique=True, nullable=False)
    nickname = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128), nullable=False)


class Books(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    category = db.Column(db.String(64))
    price = db.Column(db.Float)
    user_id = db.Column(db.Integer)
    status = db.Column(db.Enum('0', '1'), default='1')

    def to_dict(self):
        return {
            'name': self.name,
            'category': self.category,
            'price': self.price,
        }
