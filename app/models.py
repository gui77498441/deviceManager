from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,Integer,String
import datetime
import decimal


db = SQLAlchemy()

#用来序列化flask-sqlalchemy的查询结果集
class AutoSerialize(object):
    '''
    Mixin for retrieving public fields of model in json-compatible format
    '''
    __allowed_in_json__ = None

    def get_serialize(self, exclude=()):
        '''Returns model's PUBLIC data for jsonify'''
        data = {}
        keys = self._sa_class_manager.mapper.mapped_table.columns
        public = self.__allowed_in_json__
        for col in keys:
            if public is not None:
                if col.name not in public:
                    continue
            if col.name in exclude:
                continue
            data[col.name] = self._serialize(getattr(self, col.name))
        return data

    @classmethod
    def _serialize(cls, value):
        if type(value) in (int, float, bool):
            ret = str(value)
        elif isinstance(value, datetime.date):
            ret = value.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(value, datetime.time) or isinstance(value, datetime.datetime):
            ret = value.isoformat()
        elif isinstance(value, decimal.Decimal):
            ret = str(value)
        else:
            ret = value

        return ret



#用户表
class User(db.Model,AutoSerialize):
    __tablename__ = 'user'
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(32),nullable=False)
    email = Column(String(128),nullable=False)
    password = Column(String(32),nullable=False)
    isadmin = Column(Integer,nullable=False)

#整机表
class Device(db.Model,AutoSerialize):
    __tablename__ = 'device'
    id = Column(Integer,primary_key=True,autoincrement=True)
    type =  Column(Integer,nullable=False) #1服务器，2存储，3交换机
    devicename = Column(String(16),nullable=False) #设备名字 indigo oak
    sn =  Column(String(64),nullable=False) #序列号
    pn =  Column(String(16)) #pn号
    rack =  Column(Integer,nullable=False) #下拉列表(1-31)
    u_number = Column(String(16),nullable=False) #u数
    user = Column(String(128),nullable=False) #使用人，以邮箱标识，因为可能有重名
    isgood = Column(Integer,nullable=False) #是否可用
    comment = Column(String(256))#备注信息
   
#设备转移表
class DeviceTransfer(db.Model,AutoSerialize):
    __tablename__ = 'devicetransfer'
    id = Column(Integer,primary_key=True,autoincrement=True)
    type =  Column(String(16),nullable=False) #服务器，存储，交换机，内存，硬盘
    name =  Column(String(32),nullable=False) #具体名称
    sn = Column(String(64),nullable=False) #序列号
    fromuser = Column(String(128),nullable=False)#以邮箱标识
    touser = Column(String(128),nullable=False)
