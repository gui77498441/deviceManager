from . import web
from flask import request,session,render_template,redirect,url_for,flash,jsonify
from app.models import db,User,Device
from sqlalchemy import and_,or_
from flask_mail import Message
from app import mail
import json

#普通用户 整机查询
@web.route('/commonuser/device',methods=['GET','POST'])
def commonuser_device():
    deviceList = []
    return render_template('commonuser_device.html',deviceList = deviceList)

#普通用户 散件查询
@web.route('/commonuser/sparepart',methods=['GET','POST'])
def commonuser_sparepart():
    return render_template('commonuser_sparepart.html')

#普通用户 整机转让
@web.route('/commonuser/deviceTransfer',methods=['GET','POST'])
def commonuser_device_transfer():
    return render_template('commonuser_device_transfer.html')

#普通用户 整机转让
@web.route('/commonuser/sparepartTransfer',methods=['GET','POST'])
def commonuser_sparepart_transfer():
    return render_template('commonuser_sparepart_transfer.html')

#普通用户 待办事项
@web.route('/commonuser/todolist',methods=['GET','POST'])
def commonuser_todo():
    return render_template('commonuser_todolist.html')

#普通用户界面
@web.route('/commonuser/',methods=['GET','POST'])
def commonuser():
    return render_template('commonuser.html',role='普通用户',name='zby',messagenum=100)