from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand, Config
from rest_api.models import User
from rest_api import create_app, db

app = create_app('config')
manager = Manager(app)  # 创建脚本的管理对象
Migrate(app, db)  # 让迁移和app和db建立管理
manager.add_command('db', MigrateCommand)  # 将数据库的迁移脚本添加到manager

if __name__ == '__main__':

    manager.run()
