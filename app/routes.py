from app import app,db
from flask import render_template,flash,redirect,url_for,request
from app.forms import LoginForm,RegistrationForm,EditProfileForm
from flask_login import current_user,login_user,logout_user,login_required
from app.models import User
from werkzeug.urls import url_parse
from datetime import datetime

'''Flask中的 @before_request 装饰器注册在视图函数之前执行的函数'''
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/')
@app.route('/index')
# @login_required
def index():
    # user={'username':'John'}
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
    return render_template('index.html',title='Home page',posts=posts)

'''form.validate_on_submit() 实例方法会执行form校验的工作。当浏览器发起 GET 请求的时候，它 返回 False ，这样视图函数就会跳过 if 块中的代码，
直接转到视图函数的最后一句来渲染模板。 当用户在浏览器点击提交按钮后，浏览器会发送 POST 请求。 form.validate_on_submit() 就会获取 到所有的
数据，运行字段各自的验证器，全部通过之后就会返回 True ，这表示数据有效。'''
@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user,remember=form.remember_me.data)
        next_page=request.args.get('next')
        if not next_page or url_parse(next_page).netloc!='':
            next_page=url_for('index')
        return redirect(next_page)
        # return redirect(url_for('index'))
        # flash('Login request for user {},remember_me={}'.format(form.username.data,form.remember_me.data))
        # return redirect(url_for('index'))
    return render_template('login.html',title='Sign in',form=form)
'''在用户通过调用Flask-Login的 login_user() 函数登录后，应用获取了 next 查询字符串参数的 值。 Flask提供一个 request 变量，其中包含客户
端随请求发送的所有信息。 特别 是 request.args 属性，可用友好的字典格式暴露查询字符串的内容。 实际上有三种可能的情况需要 考虑，以确定成功登录后
重定向的位置： 如果登录URL中不含 next 参数，那么将会重定向到本应用的主页。 如果登录URL中包含 next 参数，其值是一个相对路径（换句话说，该URL不
含域名信息），那么 将会重定向到本应用的这个相对路径。 如果登录URL中包含 next 参数，其值是一个包含域名的完整URL，那么重定向到本应用的主页。
第三种情况是为了使应用更安全。 攻击者可以在 next 参数中插入一个指向 恶意站点的URL，因此应用仅在重定向URL是相对路径时才执行重定向，这可确保重定
向与应用保持在 同一站点中。 为了确定URL是相对的还是绝对的，我使用Werkzeug的 url_parse() 函数解析，然后 检查 netloc 属性是否被设置'''

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form=RegistrationForm()
    if form.validate_on_submit():
        user=User(username=form.username.data,email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratuations, you are now registered.')
        return redirect(url_for('index'))
    return render_template('register.html',title='Register',form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user=User.query.filter_by(username=username).first_or_404()
    posts=[
        {'author':user,'body':'test post 1'},
        {'author': user, 'body': 'test post 2'}
    ]
    return render_template('user.html',user=user,posts=posts)

@app.route('/edit_profile',methods=['GET','POST'])
@login_required
def edit_profile():
    form=EditProfileForm()
    if form.validate_on_submit():
        current_user.username=form.username.data
        current_user.about_me=form.about_me.data
        db.session.commit()
        flash('You changes had been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method=='GET':
        form.username.data=current_user.username
        form.about_me.data=current_user.about_me
    return render_template('edit_profile.html',title='Edit Profile',form=form)