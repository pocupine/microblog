from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
'''Flask-Migrate通过 flask 命令暴露来它的子命令。 Flask-Migrate添加了 flask db 子命令来管理与数据库迁移相关的所有事情。 
运行 flask db init 来创建microblog的迁移存储库'''

app=Flask(__name__)
app.config.from_object(Config)
db=SQLAlchemy(app)
migrate =Migrate(app,db)

from app import routes, models