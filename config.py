#encoding: utf-8

import os

DEBUG = True
# THREADED = True

SECRET_KEY = os.urandom(24)

HOSTNAME = '127.0.0.1'
PORT     = '3306'
DATABASE = 'hustport'
USERNAME = 'root'
PASSWORD = '427399'
DB_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = False
# Errno 32 = False

# 邮箱
MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = "587"
MAIL_USE_TLS = True
MAIL_USERNAME = "1052503676@qq.com"
MAIL_PASSWORD = "limsndrbaakrbfhd" #生成的授权码
MAIL_DEFAULT_SENDER = "1052503676@qq.com"

# class Config(object):  # 创建配置，用类
    # 任务列表
JOBS = [  
    # {  # 第一个任务
    #     'id': 'job1',
    #     'func': '__main__:aps_test',
    #     'args': ('定时任务',),
    #     'trigger': 'cron', # cron表示定时任务
    #     # 'hour': 19,
    #     # 'minute': 27
    #     'second': 5,
    # }
    {  # 第二个任务，每隔5S执行一次
        'id': 'job2',
        'func': '__main__:send_email_1', # 方法名
        'args': (), # 入参
        'trigger': 'interval', # interval表示循环任务
        'seconds': 10,
    }
]
