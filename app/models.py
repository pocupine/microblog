from app import db
from datetime import datetime
'''User类继承自db.Model，它是Flask-SQLAlchemy中所有模型的基类。 这个类将表的 字段定义为类属性，字段被创建为 db.Column 类的实例，
它传入字段类型以及其他可选参数.该类的 __repr__ 方法用于在调试时打印用户实例'''
'''user_id 字段被初始化为 user.id 的外键，这意味着它引用了来自用户表的 id 值。本处 的 user 是数据库表的名称，Flask-SQLAlchemy自动设置
类名为小写来作为对应表的名称。 User 类有一个新的 posts 字段，用 db.relationship 初始化。这不是实际的数据库字段，而是用 户和其动态之间关系
的高级视图，因此它不在数据库图表中。对于一对多关系， db.relationship 字 段通常在“一”的这边定义，并用作访问“多”的便捷方式。因此，如果我有一个
用户实例 u ，表达 式 u.posts 将运行一个数据库查询，返回该用户发表过的所有动态。 db.relationship 的第一个参 数表示代表关系“多”的类。 
backref 参数定义了代表“多”的类的实例反向调用“一”的时候的属性 名称。这将会为用户动态添加一个属性 post.author ，调用它将返回给该用户动态的用
户实例。 lazy 参数定义了这种关系调用的数据库查询是如何执行的'''
class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(64),index=True,unique=True)
    email=db.Column(db.String(64),index=True,unique=True)
    password_hash = db.Column(db.String(128))
    posts=db.relationship('Post',backref='author',lazy='dynamic')
    
    def __repr__(self):
        return '<User{}>'.format(self.username)

class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    def __repr__(self):
        return '<Post {}>'.format(self.body)

    '''对数据库的更改是在会话的上下文中完成的，你可以通过 db.session 进行访问验证。 允许在会话中 累积多个更改，一旦所有更改都被注册，你可以发出一个
    指令 db.session.commit() 来以原子方式写 入所有更改。 如果在会话执行的任何时候出现错误，调用 db.session.rollback() 会中止会话并删除 存储
    在其中的所有更改。 要记住的重要一点是，只有在调用 db.session.commit() 时才会将更改写入 数据库。'''