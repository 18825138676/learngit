import re
from flask import request, jsonify
from api.models import User
from api.modules.passport import passport_blu


@passport_blu.route('/login',methods=['POST'])

def login():
    data_dict = request.json
    mobile = data_dict.get('mobile')
    password = data_dict.get('password')
    if not [mobile, password]:
        return jsonify(code=400, msg='参数不完整')
    if not re.match('1[3456789]\\d{9}', mobile):
        return jsonify(code=400, msg='手机号码格式不正确')
    try:
        user = User.query.filter(User.mobile == mobile).first()
    except Exception as er:
        return jsonify(code=400, msg='数据库创建失败')
    if not user:
        return jsonify(code=400, msg='用户手机号不存在')
    if password != user.password:
        return jsonify(code=400, msg='密码不正确')
    return jsonify(code=200, msg='登陆成功')