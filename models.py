#encoding:utf-8

from exts import db


### 班级表
class Grade(db.Model):
    __tablename__ = 'grade'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    gradename = db.Column(db.String(40),nullable=False)
    stunumber = db.Column(db.Integer)
    # 引入外键user.id 班级管理者必须先存在于用户表中
    # manage_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    manage_id = db.Column(db.Integer)


### 学生表
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    mailaddr = db.Column(db.String(30),nullable=False)
    username = db.Column(db.String(50),nullable=False)
    stuid = db.Column(db.String(11), nullable=False)
    password = db.Column(db.String(100),nullable=False)
    # 引入外键grade.id
    grade_id = db.Column(db.Integer,db.ForeignKey('grade.id'))
    # 班级-学生一对多关系
    grade = db.relationship('Grade',backref=db.backref('users'), foreign_keys=[grade_id])#grade_id被指定为多个外键，建立关系时要指明foreign_keys


### 学生-作业多对多关系中间表
tb_user_task = db.Table('tb_user_task',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('task_id', db.Integer, db.ForeignKey('task.id'))
    )


### 作业（发布）表
class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    taskname = db.Column(db.String(40), nullable=False)
    deadline = db.Column(db.String(40), nullable=False)
    # 标志是否将该任务的所有提交打包后发送给学委，默认无
    issend = db.Column(db.Boolean,default=False)
    # 引入外键grade.id
    grade_id = db.Column(db.Integer,db.ForeignKey('grade.id'))
    # 班级-任务一对多关系
    grade = db.relationship('Grade',backref=db.backref('tasks'), foreign_keys=[grade_id])
    # 学生-任务多对多关系
    users = db.relationship('User', secondary=tb_user_task, # 中间表名字定义在前面
                                    backref='tasks', 
                                    lazy='dynamic')
                                    

### 作业（提交）表
class Present(db.Model):
    __tablename__ = 'present'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 引入外键task.id
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    # 引入外键user.id
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # 学生-作业（提交）一对多关系
    user = db.relationship('User', backref=db.backref('presents'))
    # 作业发布-作业提交一对多关系
    task = db.relationship('Task', backref=db.backref('presents'))
    # 提交作业的扩展名
    present_type = db.Column(db.String(10),nullable=False) 


    