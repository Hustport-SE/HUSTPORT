#encoding: utf-8

import os

DEBUG = True
# THREADED = True

SECRET_KEY = os.urandom(24)

HOSTNAME = "localhost"
PORT     = '3306'
DATABASE = 'hustport'
USERNAME = 'root'
PASSWORD = ''
DB_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = False
# Errno 32 = False
