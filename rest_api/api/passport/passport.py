# @Time    : 2020-11-12 22:34
# @Author  : 老赵
# @File    : passport.py
import re

from flask import jsonify, request
from flask_restful import Resource

from rest_api import db
from rest_api.models import User


class LoginViews(Resource):

    def post(self):
        data_dict = request.json
        mobile = data_dict.get('mobile')
        password = data_dict.get('password')

        if not [mobile, password]:
            return jsonify(code=400, msg="参数不完整")

        if not re.match('1[3456789]\\d{9}', mobile):
            return jsonify(code=400, msg="手机不正确")
        try:
            user = User.query.filter(User.mobile == mobile).first()
        except Exception as e:
            return jsonify(code=400, msg='数据库查询失败')

        if not user:
            return jsonify(code=400, msg="用户手机号不存在")

        if password != user.password:
            return jsonify(code=400, msg="密码不正确")

        return jsonify(code=200, msg='登陆成功')


class RegViews(Resource):

    def post(self):
        data_dict = request.json
        mobile = data_dict.get('mobile')
        nickname = data_dict.get('nickname')
        password = data_dict.get('password')

        if not [mobile, password]:
            return jsonify(code=400, msg="参数不完整")

        if not re.match('1[3456789]\\d{9}', mobile):
            return jsonify(code=400, msg="手机不正确")

        user = User()
        user.mobile = mobile
        user.nickname = nickname
        user.password = password

        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            return jsonify(code=400, msg='数据创建失败')

        return jsonify(code=200, msg='注册成功')
