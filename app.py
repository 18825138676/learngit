import re

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand

from converter.converter import MobileConverter


class Config:
    DEBUG=True
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:123@localhost:3306/assignment'
    SQLALCHEMY_TRACK_MODIFICATIONS=False


app=Flask(__name__)
app.config.from_object(Config)
db=SQLAlchemy(app)

class User(db.Model):
    __tablename__='user'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    mobile=db.Column(db.String(16),unique=True,nullable=False)
    nickname=db.Column(db.String(64),unique=True)
    password=db.Column(db.String(128),nullable=False)

class Books(db.Model):
    __tablename__='books'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(64),unique=True,nullable=False)
    category=db.Column(db.String(64),unique=True)
    price=db.Column(db.Float)
    user_id=db.Column(db.Float)
    status=db.Column(db.Enum('0','1'),default='1')

    def to_dict(self):
        return{
            'name':self.name,
            'category':self.category,
            'price': self.price
        }
manager=Manager(app)  #创建脚本的管理对象
Migrate(app,db) #迁移app和db建立管理
manager.add_command('db',MigrateCommand)#将数据库的迁移脚本添加到manager

@app.route('/')
def helloworld():
    return 'Helloworld'
@app.route('/passport/register',methods=['POST'])
def register():
    data_dict=request.json
    mobile=data_dict.get('mobile')
    nickname=data_dict.get('nickname')
    password=data_dict.get('password')
    if not [mobile,password]:
        return jsonify(code=400,msg='参数不完整')
    if not re.match('1[3456789]\\d{9}',mobile):
        return jsonify(code=400,msg='手机号码格式不正确')

    user=User()
    user.mobile= mobile
    user.nickname= nickname
    user.password= password

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as er:
        return jsonify(code=400,msg='数据库创建失败')
    return jsonify(code=200,msg='注册成功')
@app.route('/passport/login',methods=['POST'])
def login():
    data_dict=request.json
    mobile=data_dict.get('mobile')
    password=data_dict.get('password')
    if not [mobile,password]:
        return jsonify(code=400,msg='参数不完整')
    if not re.match('1[3456789]\\d{9}',mobile):
        return jsonify(code=400,msg='手机号码格式不正确')
    try:
        user=User.query.filter(User.mobile==mobile).first()
    except Exception as er:
        return jsonify(code=400,msg='数据库创建失败')
    if not user:
        return jsonify(code=400,msg='用户手机号不存在')
    if password !=user.password:
        return jsonify(code=400,msg='密码不正确')
    return jsonify(code=200,msg='登陆成功')


@app.route('/books',methods=['GET','POST'])
def books():
    if request.method=='GET':
        books=Books.query.filter(Books.status=='1').all()
        # books_list=[]
        # for i in books:
        #     book={'name': i.name,
        #           'category':i.category,
        #           'price': i.price }
        #     books_list.append(book)
        return jsonify(code=200,msg='获取列表成功',data=[i.to_dict() for i in books])
    data_dict=request.json

    name=data_dict.get("name")
    category=data_dict.get('category')
    price=data_dict.get('price')

    book=Books()
    book.name = name
    book.category=category
    book.price=price

    try:
        db.session.add(book)
        db.session.commit()
    except Exception as er:
        return jsonify(code=400,msg='数据更新失败')

    return jsonify(code=200,msg='添加成功',data=book.to_dict())


@app.route('/books/<int:book_id>',methods=['POST','DELETE'])
def book_info(book_id):
    if request.method=='DELETE':
        book=Books.query.get(book_id)
        if not book:
            return jsonify(code=400,msg='查无此书')
        if book.status=='0':
            return jsonify(code=400,msg='此书已删除')
        book.status='0'
        try:
            db.session.add(book)
            db.session.commit()
        except Exception as er:
            return jsonify(code=200,msg='删除成功')
    data_dict=request.json
    book=Books.query.get(book_id)
    if not book:
        return jsonify(code=400,msg="查无此书")
    if book.status==0:
        return jsonify(code=400,msg='此书已删除')
    book.category=data_dict.get('category')
    book.price=data_dict.get('price')
    try:
        db.session.add(book)
        db.session.commit()
    except Exception as e:
        return jsonify(code=400,msg='数据更新失败')
    return jsonify(code=200,msg='修改成功',data=book.to_dict())

#将自定义转换器添加到转换器字典中
app.url_map.converters['mobile']=MobileConverter

@app.route('/send/<mobile:mobile_num>')
def send_sms(mobile_num):
    return 'send to %s' %mobile_num

if __name__=='__main__':
    manager.run()