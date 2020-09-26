from app import app
from flask import render_template,flash,redirect,url_for
from app.forms import LoginForm
@app.route('/')
@app.route('/index')
def index():
    user={'username':'John'}
    posts=[
        {
            'author':{'username':'John'},
            'Body':'Beautiful day'
        },
        {
            'author':{'username':'Susan'},
            'Body':'Fantacy home.'
        },
        {
            'author': {'username': 'Jane'},
            'Body': 'What a surprise.'
        }
    ]
    return render_template('index.html',user=user,posts=posts)

'''form.validate_on_submit() 实例方法会执行form校验的工作。当浏览器发起 GET 请求的时候，它 返回 False ，这样视图函数就会跳过 if 块中的代码，
直接转到视图函数的最后一句来渲染模板。 当用户在浏览器点击提交按钮后，浏览器会发送 POST 请求。 form.validate_on_submit() 就会获取 到所有的
数据，运行字段各自的验证器，全部通过之后就会返回 True ，这表示数据有效。'''
@app.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        flash('Login request for user {},remember_me={}'.format(form.username.data,form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html',title='Sign in',form=form)