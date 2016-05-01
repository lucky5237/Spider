# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


# user表对应关系
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(25), nullable=False)
    webid = db.Column(db.Integer, db.ForeignKey('web.id'))
    web = db.relationship('Web', uselist=False)

    def __init__(self, username, password, webid):
        self.username = username;
        self.password = password;
        self.webid = webid;


class Web(db.Model):
    __tablename__ = 'web'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    website = db.Column(db.String(100), nullable=False)

    def __init__(self, name, website):
        self.name = name
        self.website = website


# 首页
@app.route('/')
def index():
    return render_template('index.html')


# 编辑用户页面
@app.route('/user/operate')
def operate():
    return render_template('userOperate.html')


# 添加用户页面
@app.route('/user/add')
def add():
    webList = Web.query.all()
    return render_template('userAdd.html', webList=webList)


# 添加用户
@app.route('/user/doAdd.do', methods=['GET', 'POST'])
def addUser():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        webid = request.form['website']
        print username, password, webid
        if username and password:
            userList = User.query.filter_by(username=username, webid=webid).all()
            if userList:
                return '该网站此用户名已存在,请勿重复添加'
            else:
                try:
                    user = User(username, password, webid)
                    db.session.add(user)
                    db.session.commit()
                    return '用户添加成功'
                except Exception as e:
                    db.session.rollback()
                    print '添加用户至数据库异常' + e.message
                    return '用户添加失败'
        else:
            print '用户名或者密码不能为空'


# 编辑用户界面
@app.route('/user/modify')
def modify():
    userList = User.query.all()
    for user in userList:
        print user.username, user.webid
    return render_template('userModify.html', userList=userList)


# 删除用户
@app.route('/user/doModify.do', methods=['GET', 'POST'])
def modifyUser():
    if request.method == 'POST':
        userId = request.form['userList']
        newPassword = request.form['password']
        if newPassword:
            user = User.query.filter_by(id=userId).first()
            if user:
                try:
                    user.password = newPassword
                    db.session.add(user)
                    db.session.commit();
                    return '用户密码修改成功'
                except Exception as e:
                    db.session.rollback()
                    return '修改用户密码出现异常' + e.message
        else:
            return '密码不能为空'


@app.route('/user/delete')
def delete():
    userList = User.query.all()
    for user in userList:
        print user.username, user.webid
    return render_template('userDelete.html', userList=userList)


# 删除用户
@app.route('/user/doDelete.do', methods=['GET', 'POST'])
def deleteUser():
    if request.method == 'POST':
        userId = request.form['userList']
        user = User.query.filter_by(id=userId).first()
        if user:
            try:
                db.session.delete(user)
                db.session.commit();
                return '用户删除成功'
            except Exception as e:
                db.session.rollback()
                return '删除用户出现异常' + e.message


# 选择用户登录界面
@app.route('/user/login')
def login():
    userList = User.query.all()
    for user in userList:
        print user.username, user.webid
    return render_template('userLogin.html', userList=userList)


# 用户登录
@app.route('/user/loginUser.do', methods=['GET', 'POST'])
def loginUser():
    if request.method == 'POST':
        id = request.form['userList']
        user = User.query.filter_by(id=id).first()
        username = user.username
        password = user.password
        webid = user.webid
        print username, password,webid
        if username and password:
            # 根据webid调用不同的方法,比如0-loginJD 等
            LoginJD(username, password)
            return '登录成功'
        else:
            return '该用户不存在'


def LoginJD(username, password):
    # 拿到用户名和密码模拟登陆
    print '登录成功'


if __name__ == '__main__':
    app.run(debug=True)
