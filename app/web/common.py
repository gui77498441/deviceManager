from . import web
from flask import request,session,render_template,redirect,url_for,flash,jsonify
from app.models import db,User,Device
from sqlalchemy import and_,or_
from flask_mail import Message
from app import mail
import json



@web.route('/welcome',methods=['GET'])
def welcome():
    if request.method == 'GET':
        return render_template("welcome.html")
   







@web.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        data = request.form.to_dict()
        email = data.get('email',"").strip()
        password = data.get('password',"").strip()
        dbSession = db.session()
        user = dbSession.query(User).filter(and_(User.email == email,User.password == password)).first()
        if user :
            session['email'] = user.email
            session['name'] = user.name
            session['isadmin'] = user.isadmin
            session['id'] = user.id
            if user.isadmin == 0:
                return render_template('commonuser.html',role='普通用户',name=user.name,messagenum=100)
            else:
                return render_template('admin.html',role='管理员',name=user.name)
        else:
            flash('请检查用户名密码是否正确')
            return redirect(url_for('web.login'))#('login.html',result="用户名密码错误")


        
@web.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        data = request.form.to_dict()
        email = data.get('email',"").strip()
        name = data.get('name',"").strip()
        password = data.get('password',"").strip()
        verifyPassword = data.get('verifyPassword',"").strip()
        if(password == verifyPassword):
            #插入数据库
            dbSession = db.session()
            user = User(name=name,email=email,password=password,isadmin=0)
            dbSession.add(user)
            dbSession.commit()
            flash('注册成功，请登录')
            return redirect(url_for('web.login'))
        else:
            return redirect(url_for('web.register'))
        
@web.route('/changePwd',methods=['POST'])
def chanagePwd():
    data = request.form.to_dict()
    oldPassword = data.get('oldPassword',"").strip()
    newPassword = data.get('newPassword',"").strip()
    verifyPassword = data.get('verifyPassword',"").strip()
    userid = data.get('userId',0)

    #根据用户id查该用户是否存在
    dbSession = db.session()
    userList = dbSession.query(User).filter(User.id == userid).all()
    if len(userList) > 0:
        user = userList[0]
        if user:
            #如果用户存在，再判断用户传来的新密码和确认密码是否一致，这个放在前端处理吧

            #判断oldpassword和数据库中的是否一致
            currentPwd = user.password
            if currentPwd == oldPassword:
                user.password = newPassword
                dbSession.commit()
                print('change pwd success')
                return 'change pwd success'
            else:
                print('old password wrong')
                return 'old password wrong'

    else:
        print('user is not exist')
        return 'user is not exist'
   
@web.route('/admin/deleteUser',methods=['POST'])
def deleteUser():
    data = request.form.to_dict()
    userid = data.get('userId',0)
    dbSession = db.session()
    #1.根据id查看用户是否存在
    count = dbSession.query(User).filter(User.id == userid).count()
    if count > 0:
        user = dbSession.query(User).filter(User.id == userid).first()
        dbSession.delete(user)
        dbSession.commit()
        print('delete user success')
        return 'delete user success'
    else:
        print('user is not exist')
        return 'user is not exist'

@web.route('/admin/getUserList',methods=['GET'])
def getUserList():
    dbSession = db.session()
    userList = dbSession.query(User).all()
    for user in userList:
        print(str(user.id) + " " + user.name + " "+ user.email+ " "+ user.password+" "+str(user.isadmin))
    return 'list success'

@web.route('/admin/searchUser',methods=['GET'])
def searchUser():
    keyword = request.args.get('keyword')
    print(keyword)
    if keyword:
        dbSession = db.session()
        userList = dbSession.query(User).filter(or_(User.name.like('%%'+keyword+'%%'),User.email.like('%%'+keyword+'%%'))).all()
        print(str(dbSession.query(User).filter(or_(User.name.like('%%'+keyword+'%%'),User.email.like('%%'+keyword+'%%')))))
        if len(userList) >0:
            for user in userList:
                print(str(user.id) + " " + user.name + " "+ user.email+ " "+ user.password+" "+str(user.isadmin))
        return str(len(userList))

    else:
        print('parameter wrong')
        return 'parameter wrong'



@web.route('/mail',methods=['GET'])
def sendMail():
    msg = Message(subject="物料转移提醒，请处理",recipients=["zhubingyang@inspur.com"])
    msg.body = "testing"
    msg.html = "<b>testing</b>"
    mail.send(msg)
    return 'mail success'

