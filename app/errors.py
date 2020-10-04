from app import app,db
from flask import render_template

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'),500
'''500错误的错误处理程序应当在引发数据库错误后调用，而上面的用户名重复实际上就是这种情况。 为了确保任何失败的数据库会话不会干扰模板触发的其他
数据库访问，我执行会话回滚来将会话重置 为干净的状态。'''