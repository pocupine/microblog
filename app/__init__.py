from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
'''Flask-Migrate通过 flask 命令暴露来它的子命令。 Flask-Migrate添加了 flask db 子命令来管理与数据库迁移相关的所有事情。 
运行 flask db init 来创建microblog的迁移存储库'''
import logging
from logging.handlers import RotatingFileHandler, SMTPHandler
import os

app=Flask(__name__)
app.config.from_object(Config)
db=SQLAlchemy(app)
migrate =Migrate(app,db)
login=LoginManager(app)
login.login_view='login'
from app import routes, models,errors

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler=RotatingFileHandler('logs/microblog.log',maxBytes=10240,backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog,startup')