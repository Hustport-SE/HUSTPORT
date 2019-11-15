#encoding: utf-8

from flask import Flask, render_template, request, redirect, url_for, jsonify, session, g
import config
import datetime,time
from models import User, Grade, Task, Present
from exts import db
from decorators import login_required   # 登陆限制

from flask_apscheduler import APScheduler # mail
from flask_mail import Mail,Message # mail
import logging  # mail
import zipfile  # mail
import os,sys   # mail
from werkzeug.utils import secure_filename  # mail

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

mail = Mail()   # mail
mail.init_app(app)  # mail


# 页面视图函数


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
            userAPI = url_for('api_users_id', userId= user.id)   
            hostURL = url_for('index')
            taskAPI = url_for('api_users_id_tasks', userId=user.id)

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

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/manage/')  # 需要已经登录、有班级且是学委才能访问此页面
def manage():
    if session.get('stuid'):
        # 已经登录
        user = User.query.filter(User.id==session.get('stuid')).first()
        if user.grade_id:
            # 已经登录且已经有班级
            if user.id == user.grade.manage_id:
                # 已经登录且有班级且是学委则返回管理页面
                userAPI = url_for('api_users_id', userId=user.id)
                hostURL = url_for('index')
                classAPI = url_for('api_classes_id_users', classId=user.grade_id)
                return render_template('manage.html', userAPI=userAPI, hostURL=hostURL, classAPI=classAPI)
            else:
                return redirect(url_for('home'))
        else:
            # 已经登录且没有班级
            return redirect(url_for('init'))
    else:
        # 没有登录
        return redirect(url_for('index'))

@app.route('/init/')  # 班级初始化页面视图函数
def init():
    if session.get('stuid'):
        # 已经登录
        user = User.query.filter(User.id==session.get('stuid')).first()
        if user.grade_id:
            # 已经登录且有班级则跳转至班级
            return redirect(url_for('home'))
        else:
            # 已经登录且没有班级则返回班级初始化页面
            userAPI = url_for('api_users_id', userId=user.id)

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
        pass_word = data['password']
        stu_id = data['studentId']
        user = User.query.filter(User.stuid==stu_id).first()
        if user and user.password==pass_word:
            session['stuid'] = user.id   #session维持登陆状态
            session.permanent = True    #保留31天
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

@app.route('/api/users/<int:userId>', methods=['GET', 'put'])   #home页面发送请求获取单个学生信息，或put方法修改信息
def api_users_id(userId):                                  
    user = User.query.filter(User.id == session.get('stuid')).first()
    if user.grade:  #已经加入班级
        dic = {
            "id": user.id,
            "name": user.username,
            "classId": user.grade.id,
            "className": user.grade.gradename,
            "mail": user.mailaddr,
            "studentId": user.stuid,
            "isManager": (user.id==user.grade.manage_id)
        }
    else:   #未加入班级
        dic = {
            "id": user.id,
            "name": user.username,
            "mail": user.mailaddr,
            "studentId": user.stuid,
        }
    if request.method == "GET": return jsonify(dic), 201
    elif request.method == "PUT":
        #更新用户信息
        data = request.get_json()
        user1 = User.query.filter(User.stuid==data.get('studentId')).first()
        if user1 and user1.id!=user.id:   # 学号重复
            return "fail", 201
        user2 = User.query.filter(User.mailaddr==data.get('mail')).first()
        if user2 and user2.id!=user.id:   # 邮件地址重复
            return "fail", 203
        if len(data.get('password'))==0:  
            user.username = data.get('name')
            user.stuid = data.get('studentId')
            user.mailaddr = data.get('mail')
        else:
            user.password = data.get('password')
        db.session.commit()
        return "success", 202   #修改成功


@app.route('/api/classes', methods=['GET', 'POST'])  # GET是注册时获取班级列表信息，POST是创建班级接口
def api_classes():
    classes = []
    grades =  Grade.query.all()
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
    if request.method == "GET": 
        return jsonify(dic), 201
    elif request.method == "POST": 
        data = request.get_json()
        grade_name = data.get('className')
        ######  暂时不考虑重复班名
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
    users = []
    users_info = User.query.filter(User.grade_id==classId).all()
    for user_info in users_info:
        user={
            "id": user_info.id,
            "name": user_info.username,
            "mail": user_info.mailaddr,
            "studentId": user_info.stuid,
        }
        users.append(user)
    dic = {"users": users}
    if request.method == "GET": return jsonify(dic), 201
    elif request.method == "POST": 
        user = User.query.filter(User.id == session.get('stuid')).first()
        gradeId = classId
        user.grade = Grade.query.filter(Grade.id==gradeId).first()
        db.session.commit()
        return "success", 201


@app.route('/api/tasks', methods=['POST'])  # 创建新作业
def api_tasks():
    taskInfo = request.get_json()
    gradeId = taskInfo.get('classId')
    taskName = taskInfo.get('taskName')
    deadline = taskInfo.get('deadline')
    
    deadline = deadline[:16]#获取前16个表示时间的字符
    
    task = Task(taskname=taskName,deadline=deadline,grade_id=gradeId)#
    db.session.add(task)    #多对多关系？对应的学生 完成 必须在学生全部加入后再布置作业
    db.session.commit()
    
    taskId = task.id 

    base_path = os.path.dirname(__file__)
        #进行新建文件夹
    file_path = os.path.join(base_path,'upload_file_dir',str(gradeId),str(taskId))
    folder = os.path.exists(file_path)
    if not folder:
        os.makedirs(file_path)

    users = User.query.filter(User.grade_id==gradeId).all()
    for user in users:
        user.tasks.append(task)
        task.users.append(user)
        db.session.commit()
        
        mailaddress=user.mailaddr

        message = Message(subject='HUSTPORT 新作业通知',recipients=[str(mailaddress)],
        body='同学,您有一份新的作业待提交，请注意及时登录网站查看！\nhttp://hustport.com:2333/')

        mail.send(message)
        

    return "success", 201

@app.route('/api/users/<int:userId>/tasks', methods=['GET'])  # home页面获取某用户作业列表
def api_users_id_tasks(userId):
    user = User.query.filter(User.id == session.get('stuid')).first()
    classId = user.grade_id
    userId = user.id
    tasks = []
    i = 1 #作业序号 
    for task in reversed(user.tasks):# 最新的放在最前面
        p = False #是否提交
        presents = Present.query.filter(Present.task_id==task.id).all()
        for present in presents:
            if present.user_id == user.id:
                p = True    #在所有提交的作业中找到对应的学生和任务
            break
        today = datetime.date.today()
        timenow = datetime.datetime.now() 
        new_time = str(timenow)
        exact_time =new_time[:16] 
        
        deadline_time=str(task.deadline)
        task_info = {
                "sequence": i,
                "taskId": task.id,  ## 作业id
                "taskName": task.taskname,
                "deadline": task.deadline,
                "isOutdated": deadline_time < exact_time,  ##当前时间大于任务截至时间，则截至
                "isSubmitted": p,
                "statusString": ""
            }
        i = i + 1
        tasks.append(task_info)

    dic = {
        "classId": classId,
        "userId": userId,
        "tasks": tasks,
    }
    return jsonify(dic), 201

## 作业提交和邮件发送和删除

#用户提交作业到服务器中
@app.route('/api/upload',methods=['POST'])      
def api_upload():
    if request.method=='POST':
        f = request.files['file']
        userId = request.form.get('userId')
        gradeId = request.form.get('classId')
        taskId = request.form.get('taskId')
        # print taskId
        user = User.query.filter(User.id==userId).first()
        stu_id = user.stuid
        stu_name=user.username
        grade = Grade.query.filter(Grade.id==gradeId).first()
        grade_name = grade.gradename
        task = Task.query.filter(Task.id==taskId).first()
        task_name = task.taskname
        base_path = os.path.dirname(__file__)
        #进行新建文件夹
        file_path = os.path.join(base_path,'upload_file_dir',str(gradeId),str(taskId))
        folder = os.path.exists(file_path)
        if not folder:
            os.makedirs(file_path)
        #进行文件重命名
        upload_path1 = os.path.join(base_path,'upload_file_dir',str(gradeId),str(taskId),secure_filename(f.filename))        
        upload_path1 = os.path.abspath(upload_path1)
        # print upload_path1
        (filepath1,tempfilename) = os.path.split(upload_path1)
        #获得文件扩展名
        (filename1,extension) = os.path.splitext(tempfilename)
        upload_path2 = os.path.join(base_path,'upload_file_dir',str(gradeId),str(taskId),str(grade_name) + "-" + str(stu_id) + "-" +str(stu_name) + "-" + str(task_name) +extension)        
        upload_path2 = os.path.abspath(upload_path2) 
        f.save(upload_path2)
        #更新数据库表单
        task = Task.query.filter(Task.id == taskId).first()
        # print task.id
        present = Present(present_type = extension, user = user, task = task)
        db.session.add(present)
        db.session.commit()
        # 处理 关系
        user.presents.append(present)
        task.presents.append(present) 
        db.session.commit()
        return u"success",201

@app.route('/api/upload/wrong',methods=['POST'])      #用户提交作业到服务器中
def api_upload_wrong():
    return u"success",201 

# 删除作业
@app.route('/api/users/<int:userId>/tasks/<int:taskId>', methods=['DELETE']) 
def api_users_id_tasks_id(userId, taskId):
    user = User.query.filter(User.id==userId).first()
    stu_id = user.stuid
    gradeId = user.grade_id
    stu_name=user.username
    grade = Grade.query.filter(Grade.id==gradeId).first()
    grade_name = grade.gradename
    task = Task.query.filter(Task.id==taskId).first()
    task_name = task.taskname
    present = Present.query.filter(Present.task_id==taskId and Present.user_id==userId).first()
    extension = present.present_type


    base_path = os.path.dirname(__file__)
    delete_path = os.path.join(base_path,'upload_file_dir',str(gradeId),str(taskId),str(grade_name) + "-" + str(stu_id) + "-" +str(stu_name) + "-" + str(task_name) +extension)
    delete_path = os.path.abspath(delete_path)
    if(os.path.exists(delete_path)):
        os.remove(delete_path)
    db.session.delete(present)
    db.session.commit()
    return "success", 201

# 发送邮件
def send_email_1():
    with app.app_context():
        tasks=Task.query.filter(Task.issend==False).all()
        for task in tasks:
            deadline_time =str(task.deadline)
            timenow = datetime.datetime.now() 
            new_time = str(timenow)
            exact_time =new_time[:16] 
            
            if deadline_time  == exact_time and task.issend == False:
                gradeId = task.grade_id
                taskId = task.id
                grade  = Grade.query.filter(Grade.id==gradeId).first()
                manageId = grade.manage_id
                manager = User.query.filter(User.id==manageId).first()
                mail_address = manager.mailaddr
                namefront=grade.gradename + "-" + task.taskname
                
                base_path = os.path.dirname(__file__)
                #进行新建文件夹

                #进行文件重命名
                upload_path1 = os.path.join(base_path,'upload_file_dir',str(gradeId),str(taskId))
                upload_path1 = os.path.abspath(upload_path1)
                #获得文件扩展名
                upload_path2 = os.path.join(base_path,'upload_file_dir',str(gradeId),str(taskId)+'.zip')
                upload_path2 = os.path.abspath(upload_path2)
                zipf = zipfile.ZipFile(upload_path2,'w')
                zipf.write(upload_path1,)
                src_dir = upload_path1
                zip_name = src_dir +'.zip'
                z = zipfile.ZipFile(zip_name,'w',zipfile.ZIP_DEFLATED)
                for dirpath, dirnames, filenames in os.walk(src_dir):
                    fpath = dirpath.replace(src_dir,'')
                    fpath = fpath and fpath + os.sep or ''
                    for filename in filenames:
                        z.write(os.path.join(dirpath, filename),fpath+filename)
                z.close()
                message = Message(subject= '作业汇总',recipients=[str(mail_address)],body='我是一个作业邮件')
                # message = Message(subject= '作业汇总',recipients=['1052503676@qq.com'],body='我是一个作业邮件')
                try:

                    with open(upload_path2,'rb') as fp:
                        message.attach( namefront +".zip", "zip/zip", fp.read())
                    mail.send(message)
                    task.issend=True
                    db.session.commit()
                except Exception as e:
                    print(e)



if __name__ == '__main__':
    scheduler=APScheduler()
    scheduler.init_app(app)
    scheduler._logger = logging
    scheduler.start()
    app.run()
