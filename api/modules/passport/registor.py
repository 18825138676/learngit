import re

from flask import jsonify, request
from api import db
from api.models import User
from api.modules.passport import passport_blu


@passport_blu.route('/register',methods=['POST'])

def register():
    data_dict = request.json
    mobile = data_dict.get('mobile')
    nickname = data_dict.get('nickname')
    password = data_dict.get('password')
    if not [mobile, password]:
        return jsonify(code=400, msg='参数不完整')
    if not re.match('1[3456789]\\d{9}', mobile):
        return jsonify(code=400, msg='手机号码格式不正确')

    user = User()
    user.mobile = mobile
    user.nickname = nickname
    user.password = password


    db.session.add(user)
    db.session.commit()

    return jsonify(code=200, msg='注册成功')
