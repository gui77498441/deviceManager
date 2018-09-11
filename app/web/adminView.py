from . import web
from flask import request,session,render_template,redirect,url_for,flash,jsonify
from app.models import db,User,Device
from sqlalchemy import and_,or_
from flask_mail import Message
from app import mail
import json


#管理员 设备管理(包括转借)
@web.route('/admin/device',methods=['GET','POST'])
def admin_device_manager():
    if session.get('email'):
        print(session.get('email'))
    else:
        return render_template('login.html')
    dbSession = db.session()
    if(request.method == 'GET'):
        deviceList = dbSession.query(Device).all()
        return render_template('admin_deviceManager.html',deviceList = deviceList)
    if(request.method == 'POST'):
        keyword = request.form.get('keyword')
        if(keyword):
            deviceList = dbSession.query(Device).filter(or_(Device.sn.like('%%'+keyword+'%%'),\
                Device.type.like('%%'+keyword+'%%'),Device.user.like('%%'+keyword+'%%'))).all()
            return jsonify(deviceList = [device.get_serialize() for device in deviceList])
        else:
            deviceList = dbSession.query(Device).all() 
            return jsonify(deviceList = [device.get_serialize() for device in deviceList])

#管理员 设备添加
@web.route('/admin/device/add',methods=['GET','POST'])
def admin_device_manager_add():
    if request.method == 'GET':
        return render_template('device-add.html')
    else:
        deviceType = json.loads(request.form.get('type'))
        devicename = request.form.get('devicename')     
        sn = request.form.get('sn')
        pn = request.form.get('pn')
        rack = str(json.loads(request.form.get('rack')))
        u_number = request.form.get('u_number')
        user = request.form.get('user')
        isuse = json.loads(request.form.get('isuse'))
        dbSession = db.session()
        device = Device(type=deviceType,devicename=devicename,sn=sn,pn=pn,rack=int(rack),u_number=u_number,\
            user=user,isgood=isuse)
        dbSession.add(device)
        dbSession.commit()
        return jsonify({'res':'插入成功'})

#管理员 设备添加
@web.route('/admin/device/delete',methods=['POST'])
def admin_device_manager_delete():
    if request.method == 'POST':
        idList = json.loads(request.form.get('data'))
        dbSession = db.session()
        deviceList = dbSession.query(Device).filter(Device.id.in_(idList)).all()
        for device in deviceList:
            dbSession.delete(device)
        dbSession.commit()

        return jsonify({'res':'删除成功'})

#管理员 设备修改
@web.route('/admin/device/update',methods=['POST'])
def admin_device_manager_update():
    if request.method == 'POST':
        id = json.loads(request.form.get('id'))
        deviceType = request.form.get('type')
        devicename = request.form.get('devicename')     
        sn = request.form.get('sn')
        pn = request.form.get('pn')
        rack = json.loads(request.form.get('rack'))
        u_number = request.form.get('u_number')
        user = request.form.get('user')
        isgood = json.loads(request.form.get('isgood'))

        dbSession = db.session()
        device = dbSession.query(Device).filter(Device.id == id).first()
        device.type = deviceType
        device.devicename = devicename
        device.sn = sn
        device.pn = pn
        device.rack = rack
        device.u_number = u_number
        device.user = user
        device.isgood = isgood
        dbSession.commit()
        return jsonify({'res':'更新成功'})

#管理员 散件管理(包括转借)
@web.route('/admin/sparepart',methods=['GET','POST'])
def admin_sparepart_manager():
    return render_template('admin_sparepartManager.html')

#管理员 用户管理
@web.route('/admin/user',methods=['GET'])
def admin_user_manager():
    #查询所有用户信息
    dbSession = db.session()
    userList = dbSession.query(User).all()    
    return render_template('admin_userManager.html',userList=userList)

#管理员 用户管理
@web.route('/admin/user/delete',methods=['POST'])
def admin_user_manager_delete():
    userid = json.loads(request.form.get('id'))
    #根据ID删除用户
    dbSession = db.session()
    user = dbSession.query(User).filter(User.id == userid).first() 
    if user:
        dbSession.delete(user)
        dbSession.commit()
        return jsonify({'result':"删除成功"})
    else:
        return  jsonify({'result':"用户不存在"})

#管理员 用户搜索
@web.route('/admin/user/search',methods=['POST'])
def admin_user_manager_search():
    keyword = json.loads(request.form.get("keyword"))
    dbSession = db.session();
    userList = dbSession.query(User).filter(or_(User.name.like('%%'+keyword+'%%'),User.email.like('%%'+keyword+'%%'))).all()
    res = []
    for user in userList:
        temp={}
        temp['id'] = user.id
        temp['name'] =user.name
        temp['email'] = user.email
        temp['isadmin']=user.isadmin
        res.append(temp)
    return jsonify(res = res)



#管理员 待办事项
@web.route('/admin/todolist',methods=['GET','POST'])
def admin_todo():
    return render_template('admin_todolist.html')




#管理员界面
@web.route('/admin/',methods=['GET','POST'])
def admin():
    return render_template('admin.html',role='管理员',name='superuser')