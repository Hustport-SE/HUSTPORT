#encoding: utf-8

import os

DEBUG = True


SECRET_KEY = os.urandom(24)

HOSTNAME = '#######'
PORT     = '#######'
DATABASE = '#######'
USERNAME = '#######'
PASSWORD = '#######'
DB_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = False
# Errno 32 = False

# 邮箱配置
MAIL_SERVER = '#######'
MAIL_PORT = '#######'
MAIL_USE_TLS ='#######'
MAIL_USERNAME = '#######'
MAIL_PASSWORD = '#######'#生成的授权码
MAIL_DEFAULT_SENDER = '#######'

    # 任务列表
JOBS = [  
 
    {  # 第二个任务，每隔5S执行一次
        'id': 'job2',
        'func': '__main__:send_email_1', # 方法名
        'args': (), # 入参
        'trigger': 'interval', # interval表示循环任务
        'seconds': 10,
    }
]
