#基本配置
class BaseConfig():
    MODE = 'default'
    USERNAME = 'defaultusername'
    PASSWORD = 'defaultpwd'
    FILENAME='config.py'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/deviceManager?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    HOST = '0.0.0.0'
    PORT = 8080
    SECRET_KEY = "AIJD1314"

    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_DEFAULT_SENDER = 'devicemanager@163.com'
    MAIL_USERNAME = 'devicemanager@163.com'
    MAIL_PASSWORD = '123456aA'



#开发模式下的配置
class DevelopConfig(BaseConfig):
    MODE = 'develop'
#生产环境下的配置
class ProductConfig(BaseConfig):
    MODE = 'product'
    
config ={ #将类写成字典的形式存储
   'dev':DevelopConfig,
   'pro':ProductConfig,
   'default':DevelopConfig
}