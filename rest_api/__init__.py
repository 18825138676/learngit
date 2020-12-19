# @Time    : 2020-11-12 22:17
# @Author  : 老赵
# @File    : __init__.py.py


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from Config.config import config_dict


db = SQLAlchemy()
from rest_api.api.resource import api

def create_app(config_name):
    app = Flask(__name__)
    config = config_dict[config_name]
    app.config.from_object(config)
    api.init_app(app)
    db.init_app(app)

    return app
