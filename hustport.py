#encoding: utf-8
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

@app.route('/api/users/<int:userId>', methods=['GET', 'PUT'])   #home页面发送请求获取单个学生信息，或put方法修改信息
def api_users_id(userId):
        return "success", 202


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
        return "success", 201


@app.route('/api/tasks', methods=['POST'])  # 创建新作业
def api_tasks():
    taskInfo = request.get_json()
    gradeId = taskInfo.get('classId')
    taskName = taskInfo.get('taskName')
    deadline = taskInfo.get('deadline')
    task = Task(taskname=taskName,deadline=deadline,grade_id=gradeId)#
    db.session.add(task)
    db.session.commit()
    return "success", 201

@app.route('/api/users/<int:userId>/tasks', methods=['GET'])  # home页面获取某用户作业列表
def api_users_id_tasks(userId):
    return "success", 201

@app.route('/api/users/<int:userId>/tasks/<int:taskId>', methods=['DELETE'])  # 用户删除已经交的作业
def api_users_id_tasks_id(userId, taskId):
    return "success", 201

@app.route('/api/upload',methods=['POST'])      #用户提交作业到服务器中
def api_upload():
    if request.method=='POST':
        f = request.files['file']
        userId = request.form.get('userId')
        gradeId = request.form.get('classId')
        taskId = request.form.get('taskId')
        # data=request.get_json()
        # f = data.get('file')
        # user_id = data.get('user_id')
        # grade_id = data.get('grade_id')
        user = User.query.filter(User.id==userId).first()
        stu_id = user.stuid
        # gradeId=user.grade_id
        base_path = os.path.dirname(__file__)
        #进行新建文件夹
        file_path = os.path.join(base_path,'upload_file_dir',gradeId,taskId)
        folder = os.path.exists(file_path)
        if not folder:
            os.makedirs(file_path)
        #进行文件重命名
        upload_path1 = os.path.join(base_path,'upload_file_dir',gradeId,taskId,secure_filename(f.filename))
        upload_path1 = os.path.abspath(upload_path1)
        (filepath1,tempfilename) = os.path.split(upload_path1)
        #获得文件扩展名
        (filename1,extension) = os.path.splitext(tempfilename)
        upload_path2 = os.path.join(base_path,'upload_file_dir',gradeId,taskId,stu_id +extension)
        upload_path2 = os.path.abspath(upload_path2)
        print upload_path2
        try:
            os.rename(upload_path1,upload_path2)
        except Exception as e:
            print e
            print 'rename file fail\r\n' 
        f.save(upload_path2)
        #更新数据库表单
        present = Present(task_id=taskId,user_id=userId,present_type=extension)
        db.session.add(present)
        db.session.commit()
        return u"success",201
if __name__ == '__main__':
    app.run(debug=True)
