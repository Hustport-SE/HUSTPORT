#encoding: utf-8

# from flask import Flask, render_template, request, redirect, url_for, jsonify, session, g
# import config
# from models import User, Grade, Task, Present
# from exts import db
# from decorators import login_required   # 登陆限制
# # from utils import login_log


# app = Flask(__name__)
# app.config.from_object(config)
# db.init_app(app)


# @app.route('/') # 只是渲染登陆界面，数据提交到/api/login/
# def index():
#     # if g.user:  # 如果已经从cookie中获取登陆信息，直接重定向到home页面
#     #     return redirect('home')
#     # print session.get('stuid')    None
#     # stu_id = session.get('stuid')
#     # if stu_id: # 获取到session['stuid']
#     #     user = User.query.filter(User.stuid==stu_id).first()
#     #     if user:    # 可能后台删除了此stuid,或者重新启动服务器导致secret_key变化，使得从cookie中获得的session变化
#     #         return redirect('home')
#     return render_template('login.html')


# @app.route('/home/')# 先判断有无班级，无则调到/init
# # @login_required   #测试登陆限制 有效
# def home():
#     if session.get('stuid'):
#         userAPI = url_for('api_users_id', userId=1)
#         hostURL = url_for('index')
#         taskAPI = url_for('api_users_id_tasks', userId=1)
#         return render_template('home.html', 
#                                 userAPI=userAPI,
#                                 hostURL=hostURL,
#                                 taskAPI=taskAPI)
#     else:
#         # return jsonify({"hi":"hello"}), 202
#         return redirect(url_for('index'))
        

# @app.route('/register/')    ##渲染注册页面
# def register():
#          return render_template('register.html')



# @app.route('/api_users/', methods=['POST']) #注册提交至此
# def api_users():
#         data = request.get_json()
#         print data
#         mail_addr = data['mail']
#         user_name = data['name']
#         stu_id = data['studentId']
#         pass_word = data['password']# 班级未获取
#         user1 = User.query.filter(User.stuid==stu_id).first()
#         if user1:
#             return "iderror", 201
#         user2 = User.query.filter(User.mailaddr==mail_addr).first()
#         if user2:
#             return "mailerror",203
#         user = User(mailaddr=mail_addr, username=user_name, stuid=stu_id,password=pass_word)
#         db.session.add(user)
#         db.session.commit()
#         return "hello", 202


# @app.route('/api/login/', methods=['POST']) #登陆提交至此，比较返回状态码
# def api_login():
#     data = request.get_json()
#     # print(data)#
#     pass_word = data['password']
#     stu_id = data['studentId']
#     user = User.query.filter(User.stuid==stu_id).first()
#     if user and user.password==pass_word:
#         session['stuid'] = stu_id   #session维持登陆状态
#         session.permanent = True    #保留31天
#         # print session.get('stuid')
#         return "success", 202
#     else:
#         return "fail", 201
   


# @app.route('/manage')#只要点击超链接，需要进一步判断
# def manage():
#     userAPI = url_for('api_users_id', userId=1)
#     hostURL = url_for('index')
#     classAPI = url_for('api_users_id_tasks', userId=1)
#     return render_template('manage.html', userAPI=userAPI, hostURL=hostURL, classAPI=classAPI)


# @app.route('/api/users/<int:userId>', methods=['GET', 'PUT'])   #home页面发送请求获取单个学生信息，或put方法修改信息
# def api_users_id(userId):                                       #<int:userID>?
#     # print session.get('stuid') ok
#     user = User.query.filter(User.stuid == session.get('stuid'))
#     # print(type(jsonify(user)))
#     dic = {
#         "id": 1,
#         "name": "尚琛展",
#         "classId": 1,
#         "className": "CSIE1701",
#         "mail": "zhenbomy@foxmail.com",
#         "studentId": "U201716999888",
#         "isManager": True
#     }
#     if request.method == "GET": return jsonify(dic), 201
#     elif request.method == "PUT":
#         #更新用户信息
#         ## print(request.get_data())
	
#         # return "fail", 201
#         return "success", 202

# @app.route('/api/users/<int:userId>/tasks', methods=['GET'])#home页面获取某用户作业列表
# def api_users_id_tasks(userId):
#     dic = {
#         "classId": 1,
#         "userId": 1,
#         "tasks":[
#             {
#                 "sequence": 1,
#                 "taskId": 1,
#                 "taskName": "软工课设",
#                 "deadline": "2019-11-15",
#                 "isOutdated": False,  
#                 "isSubmitted": True,
#                 "statusString": ""
#             },
#             {
#                 "sequence": 2,
#                 "taskId": 2,
#                 "taskName": "计网课设",
#                 "deadline": "2019-11-14",
#                 "isOutdated": False,  
#                 "isSubmitted": False,
#                 "statusString": ""
#             },
#             {
#                 "sequence": 3,
#                 "taskId": 3,
#                 "taskName": "计组课设",
#                 "deadline": "2019-11-13",
#                 "isOutdated": True,  
#                 "isSubmitted": True,
#                 "statusString": ""
#             },
#         ]
#     }
#     return jsonify(dic), 201

# # app.before_request
# # def my_before_request():
# #     user_id = session.get('stuid')
# #     # print 1
# #     g.user = None   # 全局变量g默认为None
# #     if user_id: # 获取到session['stuid']
# #         user = User.query.filter(User.stuid==user_id).first()
# #         if user:    # 可能后台删除了此stuid,或者重新启动服务器导致secret_key变化，使得从cookie中获得的session变化
# #             # print 2
# #             g.user = user
# #             # print g.user
# @app.route('/api/tasks', methods=['POST'])
# def api_tasks():
#     taskInfo = request.get_json()
#     gradeId = taskInfo.get('classId')
#     taskName = taskInfo.get('taskName')
#     deadline = taskInfo.get('deadline')
#     task = Task(taskname=taskName,deadline=deadline)#,grade_id=gradeId)#
#     task.grade = Grade.query.filter(Grade.id==gradeId).first()
#     db.session.add(task)    #多对多关系？对应的学生
#     db.session.commit()
#     return "success", 201
    

# @app.route('/init')
# def init():
#     userAPI = url_for('api_users_id', userId=1)
#     classAPI = url_for('api_classes')
#     return render_template('init.html', userAPI=userAPI, classAPI=classAPI)

# @app.route('/about/')   ## 介绍
# def about():
#     return render_template('about.html')

# if __name__ == '__main__':
#     app.run()

# #encoding: utf-8

from flask import Flask, render_template, request, redirect, url_for, jsonify, session, g
import config
from models import User, Grade, Task, Present
from exts import db
from decorators import login_required   # 登陆限制
# from utils import login_log

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

# 页面视图函数

# if g.user:  # 如果已经从cookie中获取登陆信息，直接重定向到home页面
#     return redirect('home')
# print session.get('stuid')    None
# stu_id = session.get('stuid')
# if stu_id: # 获取到session['stuid']
#     user = User.query.filter(User.stuid==stu_id).first()
#     if user:    # 可能后台删除了此stuid,或者重新启动服务器导致secret_key变化，使得从cookie中获得的session变化
#         return redirect('home')

@app.route('/') # 只是渲染登陆界面，数据提交到/api/login/
def index():
    if session.get('stuid'):
        return redirect('home')
    else:
        return render_template('login.html')


@app.route('/home/')
def home():
    if session.get('stuid'):
        # 已经登录则获取登录用户信息
        user = User.query.filter(User.id==session.get('stuid')).first()
        if user.grade_id:
            # 已经登录且已经有班级则返回HOME页面
            userAPI = url_for('api_users_id', userId=1)
            hostURL = url_for('index')
            taskAPI = url_for('api_users_id_tasks', userId=1)
            return render_template('home.html', 
                                    userAPI=userAPI,
                                    hostURL=hostURL,
                                    taskAPI=taskAPI)
        else:
            # 已经登录且没有班级则跳转到init页面
            return redirect(url_for('init'))
    else:
        # 未登录则跳转到登录页面
        return redirect(url_for('index'))
        

@app.route('/register/')
def register():
    if session.get('stuid'):
        # 如果已经注册则跳转至HOME页面
        return redirect(url_for('home'))
    else:
        # 如果未注册则返回注册页面
        return render_template('register.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/manage')  # 需要已经登录、有班级且是学委才能访问此页面
def manage():
    if session.get('stuid'):
        # 已经登录
        user = User.query.filter(User.id==session.get('stuid')).first()
        if user.grade_id:
            # 已经登录且已经有班级
            if user.id == user.grade.manage_id:
                # 已经登录且有班级且是学委则返回管理页面
                userAPI = url_for('api_users_id', userId=1)
                hostURL = url_for('index')
                classAPI = url_for('api_users_id_tasks', userId=1)
                return render_template('manage.html', userAPI=userAPI, hostURL=hostURL, classAPI=classAPI)
            else:
                return redirect(url_for('home'))
        else:
            # 已经登录且没有班级
            return redirect(url_for('init'))
    else:
        # 没有登录
        return redirect(url_for('index'))

@app.route('/init')  # 班级初始化页面视图函数
def init():
    if session.get('stuid'):
        # 已经登录
        user = User.query.filter(User.id==session.get('stuid')).first()
        if user.grade_id:
            # 已经登录且有班级则跳转至班级
            return redirect(url_for('home'))
        else:
            # 已经登录且没有班级则返回班级初始化页面
            userAPI = url_for('api_users_id', userId=1)
            classAPI = url_for('api_classes')
            return render_template('init.html', userAPI=userAPI, classAPI=classAPI)
    else:
        # 没有登录
        return redirect(url_for('index'))



# API视图函数

@app.route('/api/login/', methods=['POST', 'DELETE']) # 登陆提交至此，比较返回状态码
def api_login():
    if request.method == "POST":
        data = request.get_json()
        # print(data)#
        pass_word = data['password']
        stu_id = data['studentId']
        user = User.query.filter(User.stuid==stu_id).first()
        if user and user.password==pass_word:
            session['stuid'] = user.id   #session维持登陆状态
            session.permanent = True    #保留31天
            # print session.get('stuid')
            return "success", 202
        else:
            return "fail", 201
    else:
        session.clear()
        return "logoutsuccess", 201


@app.route('/api/users/', methods=['POST']) # 注册提交至此
def api_users():
        data = request.get_json()
        mail_addr = data['mail']
        user_name = data['name']
        stu_id = data['studentId']
        pass_word = data['password']# 班级未获取
        user1 = User.query.filter(User.stuid==stu_id).first()
        if user1:
            return "iderror", 201
        user2 = User.query.filter(User.mailaddr==mail_addr).first()
        if user2:
            return "mailerror",203
        user = User(mailaddr=mail_addr, username=user_name, stuid=stu_id,password=pass_word)
        db.session.add(user)
        db.session.commit()
        return "hello", 202



# 以上视图函数均已完成
# 以下API接口大部分未完成

@app.route('/api/users/<int:userId>', methods=['GET', 'PUT'])   #home页面发送请求获取单个学生信息，或put方法修改信息
def api_users_id(userId):                                       #<int:userID>?
    # print session.get('stuid') ok
    user = User.query.filter(User.id == session.get('stuid'))
    # print(type(jsonify(user)))
    dic = {
        "id": 1,
        "name": "尚琛展",
        "classId": 1,
        "className": "CSIE1701",
        "mail": "zhenbomy@foxmail.com",
        "studentId": "U201716999888",
        "isManager": True
    }
    if request.method == "GET": return jsonify(dic), 201
    elif request.method == "PUT":
        #更新用户信息
        ## print(request.get_data())
	
        # return "fail", 201
        return "success", 202


@app.route('/api/classes', methods=['GET', 'POST'])  # GET是注册时获取班级列表信息，POST是创建班级接口
def api_classes():
    classes = []
    grades =  Grade.query.all()
    # print type(classes)
    # print classes
    for grade in grades:
        grade_id = grade.id
        class_name = grade.gradename
        stu_number = grade.stunumber
        manageId = grade.manage_id 
        grade_info = {
            "id": grade_id,
            "className": class_name,
            "studentNumber": stu_number,
            "manageId": manageId
        }
        classes.append(grade_info)
    dic = {
        "classes": classes}
    # dic = {
    #         "classes": [
    #             {
    #                 "id": 1,
    #                 "className": "CSIE1701",
    #                 "studentNumber": 36,
    #                 "manageId": 1
    #             },
    #             {
    #                 "id": 2,
    #                 "className": "CSIE1702",
    #                 "studentNumber": 36,
    #                 "manageId": 1
    #             },
    #             {
    #                 "id": 3,
    #                 "className": "CSIE1703",
    #                 "studentNumber": 36,
    #                 "manageId": 1
    #             },
    #         ]
    #     }
    if request.method == "GET": 
        return jsonify(dic), 201
    elif request.method == "POST": 
        # print(request.get_json())
        data = request.get_json()
        grade_name = data.get('className')
        ######  暂时不考虑重复班名
        # manageId = data.get('manageId')
        manageId = session.get('stuid')
        grade= Grade(gradename=grade_name, manage_id=manageId)
        db.session.add(grade)
        db.session.commit()
        manager = User.query.filter(User.id==manageId).first()
        manager.grade = grade
        db.session.commit()
        return "success", 201


@app.route('/api/classes/<int:classId>/users', methods=['GET', 'POST'])  # GET是学委面板获得本班学生列表，POST是新用户选择加入该班级
def api_classes_id_users(classId):
    dic = {
        "users":[
            {
                "id": 1,
                "name": "尚琛展",
                "mail": "zhenbomy@foxmail.com",
                "studentId": "U201716999"
            },
            {
                "id": 2,
                "name": "罗俊杰",
                "mail": "zhenbomy@foxmail.com",
                "studentId": "U201716999"
            },
            {
                "id": 3,
                "name": "郑霖",
                "mail": "zhenbomy@foxmail.com",
                "studentId": "U201710000"
            }
        ]
    }
    if request.method == "GET": return jsonify(dic), 201
    elif request.method == "POST": 
        return "success", 201


@app.route('/api/tasks', methods=['POST'])  # 创建新作业
def api_tasks():
    taskInfo = request.get_json()
    gradeId = taskInfo.get('classId')
    taskName = taskInfo.get('taskName')
    deadline = taskInfo.get('deadline')
    task = Task(taskname=taskName,deadline=deadline,grade_id=gradeId)#
    db.session.add(task)    #多对多关系？对应的学生
    db.session.commit()
    # print task
    # if task:
    return "success", 201

@app.route('/api/users/<int:userId>/tasks', methods=['GET'])  # home页面获取某用户作业列表
def api_users_id_tasks(userId):
    dic = {
        "classId": 1,
        "userId": 1,
        "tasks":[
            {
                "sequence": 1,
                "taskId": 1,
                "taskName": "软工课设",
                "deadline": "2019-11-15",
                "isOutdated": False,  
                "isSubmitted": True,
                "statusString": ""
            },
            {
                "sequence": 2,
                "taskId": 2,
                "taskName": "计网课设",
                "deadline": "2019-11-14",
                "isOutdated": False,  
                "isSubmitted": False,
                "statusString": ""
            },
            {
                "sequence": 3,
                "taskId": 3,
                "taskName": "计组课设",
                "deadline": "2019-11-13",
                "isOutdated": True,  
                "isSubmitted": True,
                "statusString": ""
            },
        ]
    }
    return jsonify(dic), 201

# app.before_request
# def my_before_request():
#     user_id = session.get('stuid')
#     # print 1
#     g.user = None   # 全局变量g默认为None
#     if user_id: # 获取到session['stuid']
#         user = User.query.filter(User.stuid==user_id).first()
#         if user:    # 可能后台删除了此stuid,或者重新启动服务器导致secret_key变化，使得从cookie中获得的session变化
#             # print 2
#             g.user = user
#             # print g.user

@app.route('/api/users/<int:userId>/tasks/<int:taskId>', methods=['DELETE'])  # 用户删除已经交的作业
def api_users_id_tasks_id(userId, taskId):
    print("hello")
    return "success", 201


if __name__ == '__main__':
    app.run(debug=True)
