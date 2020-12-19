from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from Config.config import config_dict


db=SQLAlchemy()
def create_api(config_name):
        api=Flask(__name__)
        config=config_dict[config_name]
        api.config.from_object(config)
        db.init_app(api)

        from api.modules.passport import passport_blu
        api.register_blueprint(passport_blu)

        from api.modules.books import books_blu
        api.register_blueprint(books_blu)

        return api