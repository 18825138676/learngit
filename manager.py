from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from api.models import User
from api import create_api, db

app=create_api('config')
manager=Manager(app)
Migrate(app,db)
manager.add_command('db',MigrateCommand)

if __name__=='__main__':
   manager.run()